# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class Hw3Pipeline:

    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect('db.sqlite3')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS comps(
            id INTEGER PRIMARY KEY,
            link VARCHAR UNIQUE,
            timestamp TEXT,
            title VARCHAR,
            freq_i FLOAT,
            ram INTEGER,
            rom INTEGER,
            price INTEGER,
            rank FLOAT
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute("""
            INSERT OR IGNORE INTO comps (link, timestamp, title, freq_i, ram, rom, price, rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item['link'],
            item['timestamp'],
            item['title'],
            item['freq_i'],
            item['ram'],
            item['rom'],
            item['price'],
            item['rank']
        ))

        ## Execute insert of data into database
        self.con.commit()
        return item

class Hw13NoDuplicatesPipeline:

    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect('db.sqlite3')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS comps(
            id INTEGER PRIMARY KEY,
            link VARCHAR,
            timestamp TEXT,
            title VARCHAR,
            freq_i FLOAT,
            ram INTEGER,
            rom INTEGER,
            price INTEGER,
            rank FLOAT
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute("select * from comps where link = ?", (item['link'],))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['link'])
        
        ## If text isn't in the DB, insert data
        else:

        ## Define insert statement
            self.cur.execute("""
                INSERT INTO comps (link, timestamp, title, freq_i, ram, rom, price, rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item['link'],
                item['timestamp'],
                item['title'],
                item['freq_i'],
                item['ram'],
                item['rom'],
                item['price'],
                item['rank']
            ))

            ## Execute insert of data into database
            self.con.commit()
        
        return item