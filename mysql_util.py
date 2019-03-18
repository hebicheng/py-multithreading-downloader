#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import traceback
import config
import log_util
#import pymysql


class MysqlUtil:
    def __init__(self):
        pass

    """ 
        获取数据库的连接 
    """
    @staticmethod
    def get_connect():
        # 数据库基本信息
        
        
        #download apk
        
        # 连接数据库
        db = MySQLdb.connect(host=config.DB_IP,
                             port=config.DB_PORT,
                             user=config.DB_USER,
                             passwd=config.DB_PW,
                             db=config.DB_NAME, charset='utf8')  # 获取连接
        return db

    '''
        查询数据库：单个结果集 
        fetchone(): 该方法获取下一个查询结果集。结果集是一个对象 
    '''
    def fetchone(self, sql):
        # 获取数据库连接
        db = self.get_connect()
        # 使用cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # noinspection PyBroadException
        try:
            # 执行sql语句
            result = None
            cursor.execute(sql)
            result = cursor.fetchone()
        except Exception:
            # 输出异常信息
            log_util.log_write("发生异常 = " + traceback.format_exc())
            # 如果发生异常，则回滚
            db.rollback()
        finally:
            # 最终关闭数据库连接
            db.close()
        return result

    '''
        查询数据库：多个结果集 
        fetchall(): 接收全部的返回结果行. 
    '''
    def fetchall(self, sql):
        # 获取数据库连接
        db = self.get_connect()
        # 使用cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # noinspection PyBroadException
        try:
            # 执行sql语句
            results = None
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception:
            # 输出异常信息
            log_util.log_write("发生异常 = " + traceback.format_exc())
            # 如果发生异常，则回滚
            db.rollback()
        finally:
            # 最终关闭数据库连接
            db.close()
        return results

    '''
        更新结果集 
    '''
    def update(self, sql, param):
        # 获取数据库连接
        db = self.get_connect()
        # 使用cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # noinspection PyBroadException
        try:
            # 执行sql语句
            result = 0
            result = cursor.execute(sql,param)
            db.commit()
        except Exception:
            # 输出异常信息
            log_util.log_write("发生异常 = " + traceback.format_exc())
            # 如果发生异常，则回滚
            db.rollback()
        finally:
            # 最终关闭数据库连接
            db.close()
        return result

    '''
        插入结果集 
    '''
    def insert(self, sql):
        # 获取数据库连接
        db = self.get_connect()
        # 使用cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # noinspection PyBroadException
        try:
            # 执行sql语句
            cursor.execute(sql)
            db.commit()

            log_util.log_write("insert()执行语句--" + sql.encode("utf-8") + "--插入完毕")
        except Exception:
            # 输出异常信息
            log_util.log_write("发生异常 = " + traceback.format_exc())
            # 如果发生异常，则回滚
            db.rollback()
        finally:
            # 最终关闭数据库连接
            db.close()

    '''
        获取select查询数量
    '''
    def get_effected_row_count(self, sql):
        # 获取数据库连接
        db = self.get_connect()
        # 使用cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # noinspection PyBroadException
        try:
            # 执行sql语句
            result = 0
            result = cursor.execute(sql)
        except Exception:
            # 输出异常信息
            log_util.log_write("发生异常 = " + traceback.format_exc())
            # 如果发生异常，则回滚
            db.rollback()
        finally:
            # 最终关闭数据库连接
            db.close()
        return result