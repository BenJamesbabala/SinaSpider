# 得到 redis 的数据, 再存入MongoDB
# import pymongo
import redis
import json
import pymysql

# mongoDB 的客户端
# client = pymongo.MongoClient(host='127.0.0.1', port=27017)
# redis
redis_cli = redis.StrictRedis(host='192.168.11.90', port=6379, db=0)
# mysql
cli = pymysql.connect(host='127.0.0.1', user='root', password='root',
                      db='atguigu_shop', port=3306, charset='utf8')
cursor = cli.cursor()
# 创建数据库
# sina = client['sina']
# 创建集合
# sina_item = sina['sina_item']

while True:
    try:
        source, data = redis_cli.blpop(['sina_guide:items'])
        print('source == ', source)
        print('data == ', data.decode('utf-8'))
        item = json.loads(data.decode('utf-8'))
        params = [item['parent_title'], item['sub_title'], item['sub_url'], item['tiezi_path'], item['tiezi_url'],
                  item['tiezi_title'], item['tiezi_content'], item['crawled'], item['spider']]
        sql = "INSERT INTO sina_items(parent_title, sub_title,sub_urls,sub_file_name,son_urls,head,content,crawled ,spider) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )"
        # 执行sql语句
        cursor.execute(sql, params)
        # 字典
        cli.commit()
        # sina_item.insert_one(json.loads(data.decode('utf-8')))
    except Exception as e:
        print(e)
