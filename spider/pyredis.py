import redis




class PyRedis(object):
    def __init__(self):
        self.host = '10.10.4.180'
        self.port = '6379'
        self.db = 0
        # self.c = redis.StrictRedis(host=self.host,port=self.port,db=self.db)
        pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.redis_db = redis.Redis(connection_pool=pool)
        # self.c = redis.Redis(host=self.host,port=self.port,db=self.db)


    def get_redis(self):
        return self.redis_db

