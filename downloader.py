import requests
import threading
import log_util
import traceback
import os
import mysql_util
import datetime
import time
import config

global_get_ok = True


def Handler(start, end, url, filename, referer,dlid):

    headers = {'Range': 'bytes=%d-%d' % (start, end),
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
               'Referer': referer,
               }
    try:
        r = requests.get(url, headers=headers, stream=True, timeout=(5, 15))
        # 写入文件对应位置
        st = start
        with open(filename, "r+b") as fp:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    fp.seek(st)
                    fp.write(chunk)
                    st += len(chunk)
    except Exception:
        requestOK = False  # 失败重试
        for i in range(2):
            log_util.log_write_result("dlid = {}, chunk:{}-{} 第{}次重试".format(dlid, start, end, i+1))
            try:
                r = requests.get(url, headers=headers,
                                 stream=True, timeout=(10, 120))
                # 写入文件对应位置
                st = start
                with open(filename, "r+b") as fp:
                    for chunk in r.iter_content(chunk_size=512):
                        if chunk:
                            fp.seek(st)
                            fp.write(chunk)
                            st += len(chunk)
                requestOK = True
                break
            except Exception:
                log_util.log_write("发生异常 = " + traceback.format_exc())

        if not requestOK:
            # 多次尝试均失败，通知主进程
            global global_get_ok
            global_get_ok = False


def single_down(apk_url_info, url, file_path):
    dbhandler = mysql_util.MysqlUtil()
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
               'Referer': apk_url_info[5],
               }
    try:
        start_time = time.localtime(time.time())
        r = requests.get(url, headers=headers, stream=True, timeout=(5, 15))
        with open(file_path, "wb") as fp:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    fp.write(chunk)
    except Exception:
        requestOK = False  # 失败重试
        for i in range(2):
            start_time = time.localtime(time.time())
            log_util.log_write_result("dlid = {}, 第{}次重试".format(apk_url_info[0], i+1))
            try:
                r = requests.get(url, headers=headers,
                                 stream=True, timeout=(10, 120))
                with open(file_path, "wb") as fp:
                    for chunk in r.iter_content(chunk_size=512):
                        if chunk:
                            fp.write(chunk)
                requestOK = True
                break
            except Exception:
                log_util.log_write("发生异常 = " + traceback.format_exc())

        if requestOK:
            # 下载成功
            end_time = time.localtime(time.time())
            sql = '''
                UPDATE sp_random_download_task_multiVer_copy phonedetect_service_emulator SET
                receive_size = %s, 
                begin_time=%s, 
                end_time = %s, 
                dl_status = %s,
                fullpath= %s  WHERE dl_id = %s ;

            '''
            dbhandler.update(sql, (os.stat(file_path).st_size, time.strftime(
                '%Y-%m-%d %H:%M:%S', start_time), time.strftime('%Y-%m-%d %H:%M:%S', end_time), 2, file_path, apk_url_info[0]))
            log_util.log_write_result("dlid = {}, {}下载完成".format(apk_url_info[0], file_path))    
        else:
            dbhandler.update(
                "update sp_random_download_task_multiVer_copy set dl_status = 4 where dl_id = %s and dl_status = 1", (apk_url_info[0],))
            log_util.log_write_result("dlid = {} 下载失败".format(apk_url_info[0]))
            try:
                os.remove(file_path)
            except Exception:
                log_util.log_write("发生异常 = " + traceback.format_exc())


def download_file(apk_url_info, num_thread=5):
    global global_get_ok
    global_get_ok = True
    dbhandler = mysql_util.MysqlUtil()
    file_path = str(apk_url_info[0])+"-" + \
        apk_url_info[4]+apk_url_info[19]+apk_url_info[21]
    file_path = os.path.join(config.DOWNLOAD_PATH, file_path.strip() + '.apk')
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            log_util.log_write("发生异常 = " + traceback.format_exc())


    r = requests.head(apk_url_info[3], allow_redirects=True)
    real_url = r.url
    if r.headers['Content-Type'] == 'application/vnd.android.package-archive':
        try:
            file_size = int(r.headers['content-length'])
        except:
            # 没有'content-length'，无法多线程下载
            log_util.log_write_result("dlid = {} 采用普通下载".format(apk_url_info[0]))
            single_down(apk_url_info, real_url, file_path)
            return

        #  创建一个和要下载文件一样大小的文件

        fp = open(file_path, "wb")
        fp.truncate(file_size)
        fp.close()

        # 开始下载时间
        start_time = time.localtime(time.time())
        # 启动多线程写文件
        thread_list = []  # 线程存放列表

        part = file_size // num_thread
        for i in range(num_thread):
            start = part * i
            if i == num_thread - 1:   # 最后一块
                end = file_size
            else:
                end = start + part

            t = threading.Thread(target=Handler, kwargs={
                                 'start': start, 'end': end, 'url': real_url, 'filename': file_path, 'referer': apk_url_info[5], 'dlid':apk_url_info[0]})
            t.setDaemon(True)
            thread_list.append(t)
            t.start()

        # 等待所有线程下载完成
        for t in thread_list:
            t.join()

        if not global_get_ok:
            log_util.log_write_result("dlid = {} 下载失败".format(apk_url_info[0]))
            # 下载失败，清理下载的文件
            try:
                os.remove(file_path)
            except Exception:
                log_util.log_write("发生异常 = " + traceback.format_exc())
            dbhandler.update(
            "update sp_random_download_task_multiVer_copy set dl_status = 4 where dl_id = %s and dl_status = 1", (apk_url_info[0],))
            return
        # 结束下载时间
        end_time = time.localtime(time.time())
        sql = '''
            UPDATE sp_random_download_task_multiVer_copy phonedetect_service_emulator SET
            file_size = %s,
            receive_size = %s, 
            begin_time=%s, 
            end_time = %s, 
            dl_status = %s,
            fullpath= %s  WHERE dl_id = %s ;

         '''
        dbhandler.update(sql, (file_size, file_size, time.strftime('%Y-%m-%d %H:%M:%S', start_time),
                               time.strftime('%Y-%m-%d %H:%M:%S', end_time), 2, file_path, apk_url_info[0]))
        log_util.log_write_result("dlid = {}, {}下载完成".format(apk_url_info[0] ,file_path))
    else:
        # 更新数据库，为无效链接
        log_util.log_write_result("dlid = {} 为无效链接".format(apk_url_info[0]))
        dbhandler.update(
            "update sp_random_download_task_multiVer_copy set dl_status = 128 where dl_id = %s and dl_status = 1", (apk_url_info[0],))
