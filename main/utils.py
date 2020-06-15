import hashlib
import datetime

def pwd_hash(s, salt='dfssaltsalt'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

class PCRDate():

    def __init__(self, real_datetime, tzinfo):
        self.real_datetime = real_datetime
        self.tzinfo = tzinfo
    
    def day_begin(self):
        return datetime.datetime(
                self.real_datetime.year, 
                self.real_datetime.month, 
                self.real_datetime.day,
                5, 0, 0, 0,     #当日早上5:00
                tzinfo=self.tzinfo
            )
    
    def day_end(self):
        return datetime.datetime(
                (self.real_datetime+datetime.timedelta(days=1)).year, 
                (self.real_datetime+datetime.timedelta(days=1)).month, 
                (self.real_datetime+datetime.timedelta(days=1)).day,
                5, 0, 0, 0,     #次日早上5:00
                tzinfo=self.tzinfo
            )
    
    def tz_datetime(self):
        return self.real_datetime.astimezone(self.tzinfo)
    
    def __call__(self):
        return self.real_datetime