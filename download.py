#!/usr/bin/python
# -*- coding: utf-8 -*-

import MysqlUtil
import requests
import os
import time
import hashlib


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在'
        return False


def get_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    return md5


#连接数据库
Mysqlopen = MysqlUtil.MysqlUtil()
db = Mysqlopen.get_connect()

#查询数据库表
sql_tableName = 'show tables'
result = Mysqlopen.fetchall(sql_tableName)
print(result)

sql_tableName = 'desc sp_random_download_task_multiVer_copy'
result = Mysqlopen.fetchall(sql_tableName)
print(result)

#逐个处理下载连接
max_apkid = 912224
for apk_id in range(1, max_apkid):

    sql_url = 'select * from sp_random_download_task_multiVer_copy where dl_id=%s' % apk_id
    results = Mysqlopen.fetchall(sql_url)
    for row in results:
        this_app_url = row[3]
        this_app_name = row[19]
        this_app_category = row[18]
        this_app_version = row[21]
        this_app_status = row[10]
        if this_app_status == 2:
            continue
        else:
            status = 1  # 没有在数据库里修改
            r = requests.get(this_app_url)
            r.status_code

            # TODO 判断下载是否成功，成功则进行....
            if r.status_code == 200:
                status = 2
            else:
                status = 4

            mkdir("E:\\download\\" )

            this_app_download_path = "E:\\download\\" + "\\" + str(apk_id) + "_" + this_app_category + "_" + this_app_name + "_" + this_app_version + ".apk"
            with open(this_app_download_path, "wb") as code:
                code.write(r.content)
            modifiedTime = time.localtime(os.stat(this_app_download_path).st_mtime)
            createdTime = time.localtime(os.stat(this_app_download_path).st_ctime)

            mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)
            cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)
            filesize = r.headers["Content-Length"]
            receivedsize = os.stat(this_app_download_path).st_size
            file_md5 = get_md5(this_app_download_path)

            sql_update = 'UPDATE sp_random_download_task_multiVer_copy phonedetect_service_emulator SET file_size = "'"%s"'", receive_size = "'"%s"'", begin_time="'"%s"'", end_time ="'" %s"'", dl_status = "'"%s"'", file_md5 = "'"%s"'",fullpath="'"%s"'"  WHERE dl_id = "'"%s"'"' % (filesize, receivedsize, cTime, mTime, status, file_md5, this_app_download_path,apk_id)
            Mysqlopen.update(sql_update)
            print(sql_update)































