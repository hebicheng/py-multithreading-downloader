
import os
import config
import log_util
import mysql_util
import downloader
import time
if __name__ == "__main__":
    # 创建下载目录
    if not os.path.exists(config.DOWNLOAD_PATH):
        os.makedirs(config.DOWNLOAD_PATH)
    sql = "select * from sp_random_download_task_multiVer_copy where dl_status = 0 limit 1"
    dbhandler = mysql_util.MysqlUtil()
    # 每次获取一条没有下载的数据
    cur_selected_item = dbhandler.fetchone(sql)
    while cur_selected_item:
        # 乐观锁
        # 当此更新语句成功影响行后才确认拿到下载链接
        res = dbhandler.update("update sp_random_download_task_multiVer_copy set dl_status = 1 where dl_id = %s and dl_status = 0" ,(cur_selected_item[0],))
        if not res:
            cur_selected_item = dbhandler.fetchone(sql)
            continue
        else:
            print("downloading dl_id = {}".format(cur_selected_item[0]))
            downloader.download_file(cur_selected_item, config.THREAD_NUM)