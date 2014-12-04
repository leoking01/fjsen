# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class FjsenPipeline(object):
#    def process_item(self, item, spider):
#        return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html 
#import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors

class FjsenPipeline(object):
                          
#    def __init__(self):
#        self.conn=None
#        dispatcher.connect(self.initialize,signals.engine_started)
#        dispatcher.connect(self.finalize,signals.engine_stopped)
                          
#    def process_item(self,item,spider):
#        print '==============self',self
#        print '--------------self.conn',self.conn
#        print '--------------item',item
 #       f=mysql()
 #       f.Connect(user="root",passwd="",host="localhost",db="jibenditu")
 #       f.Begin()
#        self.conn.execute('insert into fjsen values(?,?,?,?)',(None,item['title'][0],'http://www.fjsen.com/'+item['link'][0],item['addtime'][0]))
#        return item
                          
    def initialize(self):
        if path.exists(self.filename):
            self.conn=sqlite3.connect(self.filename)
        else:
            self.conn=self.create_table(self.filename)
                          
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn=None
                          
    def create_table(self,filename):
        conn=sqlite3.connect(filename)
        conn.execute("""create table fjsen(id integer primary key autoincrement,title text,link text,addtime text)""")
        conn.commit()
        return conn
                          
############
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='jibenditu',
                user='root', passwd='', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)
 
    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
 
        return item
 
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        tx.execute("select * from fjsen where link = %s", (item['link'][0], ))
        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
            tx.execute("insert into fjsen (id,link,title,addtime) "
                "values (%s, %s,%s,%s)",
                (item['id'],item['link'][0],item['title'][0],
                 datetime.datetime.now())
            )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)
 
    def handle_error(self, e):
        log.err(e)

##########################################3

import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
class MongoDBPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = pymongo.Connection(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]
    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if not data:
                err_msg += 'Missing %s of poem from %s\n' % (field, item['url'])
        if err_msg:
            raise DropItem(err_msg)
        self.collection.insert(dict(item))
        log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),
                level=log.DEBUG, spider=spider)
        return item
