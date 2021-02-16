import pymysql
import config
import pdb


class DataBase():
    def __init__(self):
        self.db = pymysql.connect(
            user=config.DATABASE_CONFIG['user'],
            passwd=config.DATABASE_CONFIG['password'],
            host=config.DATABASE_CONFIG['host'],
            db=config.DATABASE_CONFIG['dbname'],
            charset='utf8'
        )
        print("DB Connect : %s" % self.db)
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        print("DB cursor : %s" % self.cursor)

    def db_insert(self, table_name, fid_dict):
        sql = "INSERT INTO {} (timestamp,{}) VALUES ((now()),{});".format(table_name,\
                                                        "".join(["{},".format(key) for key in fid_dict.keys()])[:-1],\
                                                        "".join(["'{}',".format(val.replace("'","")) for val in fid_dict.values()])[:-1])
        print("db insert!!")
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()

    def db_create_table(self, table_name, data_list):
        sql = "SHOW TABLES LIKE '{}';".format(table_name)
        if self.cursor.execute(sql) != 0:
            print("err : exist table {}".format(table_name))
            return
        sql = "CREATE TABLE {} (\nseq INT NOT NULL AUTO_INCREMENT,\ntimestamp TIMESTAMP DEFAULT '0000-00-00 00:00:00',\n{} {}\n) ENGINE=MYISAM DEFAULT CHARSET=utf32;"\
            .format(table_name,"".join(["{} VARCHAR(1024),\n".format(col) for col in data_list]),"PRIMARY KEY (seq,timestamp)")
        # print("create table \n {}".format(sql))
        self.cursor.execute(sql)
        self.db.commit()

    def db_select(self, table_name, column_name, value):
        sql = "SELECT * FROM {} WHERE {}='{}';".format(table_name, column_name, value.replace("'",""))
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


if __name__ == '__main__':
    database = DataBase()
    database.db_create_table("GoogleCrawler", ['title', 'link', 'text'])