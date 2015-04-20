# coding=utf-8
from datetime import datetime
import json
import os
import pymongo
import sys


project_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = '%s/data' % (project_path)

sys.path.append(project_path)
from log.get_logger import logger, Timer

__author__ = 'Jayvee'

# logger初始化
# create logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# create file handler
# fh = logging.FileHandler('./logs/data_process_dumpMongoDB.log')
# fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s- '
# '%(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# # add handlers to logger
# logger.addHandler(fh)

@Timer
def dump_train_user(csv_path, db_address):
    """
    将train_user.csv的数据存入mongodb数据库
    :param csv_path: csv文件的路径
    :param db_address: mongodb的地址
    :return:
    """
    logger.info('dump_train_user start')
    csvfile = open(csv_path)
    # for line in csvfile:
    head = csvfile.readline()
    head = head.replace('\n', '')
    title = []
    for x in head.split(','):
        title.append(x)
    print title
    conn = pymongo.Connection(db_address, 27017)
    db = conn.TianchiData
    train_userdb = db.train_user_new
    # line = csvfile.readline()
    count = 0
    for line in csvfile:
        line = line.replace('\n', '')
        data = {}
        temp = line.split(',')
        for i in range(len(title)):
            if title[i] != 'time':
                data[title[i]] = temp[i]
            else:
                data[title[i]] = datetime.strptime(str(temp[i]), '%Y-%m-%d %H')
        train_userdb.insert(data)
        count += 1
        if count % 10000 == 0:
            logger.debug('%s inserted' % count)
            # line = csvfile.readline()
    conn.disconnect()
    logger.info('dump_train_user done')
    print '处理完毕'

@Timer
def dump_train_item(csv_path, db_address):
    """
    将train_item.csv的数据存入MongoDB数据库
    :param csv_path: csv文件的路径
    :param db_address: MongoDB的地址
    :return:
    """
    logger.info('dump_train_item start')
    csvfile = open(csv_path)
    # for line in csvfile:
    head = csvfile.readline()
    head = head.replace('\n', '')
    title = []
    for x in head.split(','):
        title.append(x)
    print title
    conn = pymongo.Connection(db_address, 27017)
    db = conn.TianchiData
    train_item_db = db.train_item_new
    # line = csvfile.readline()
    count = 0
    for line in csvfile:
        line = line.replace('\n', '')
        data = {}
        temp = line.split(',')
        for i in range(len(title)):
            # if title[i] != 'time':
            data[title[i]] = temp[i]
            # else:
            # data[title[i]] = datetime.strptime(str(temp[i]), '%Y-%m-%d %H')
        train_item_db.insert(data)
        count += 1
        if count % 10000 == 0:
            logger.debug('%s inserted' % count)
            # line = csvfile.readline()
    conn.disconnect()
    logger.info('dump_train_item done')
    print '处理完毕'


if __name__ == '__main__':
    db_address = json.loads(open('%s/conf/DB_Address.conf' % (project_path), 'r').read())['MongoDB_Address']
    dump_train_item(r'D:\tianchidata\tianchi_mobile_recommend_train_item.csv', db_address)
    dump_train_user(r'D:\tianchidata\tianchi_mobile_recommend_train_user.csv', db_address)