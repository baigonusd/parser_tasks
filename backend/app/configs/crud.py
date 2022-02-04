import redis
import uuid
from celery_worker import parsing_celery, celery

def checking_cash(mail, number_adds, city, price1, price2):
    r = redis.Redis(charset="utf-8", decode_responses=True)
    r2 = redis.Redis(charset="utf-8", decode_responses=True, db=2)
    data = {
        "email": str(mail),
        "number_of_adds": str(number_adds),
        "city": str(city), 
        "price1": str(price1),
        "price2": str(price2)        
    }
    ttl = 604800
    for key in r.keys():
        print("for")
        if r.hgetall(key) == data:
            print("if")
            #Response will be finded parser
            response = r2.hget(key ,key)
            print(response)
            return response
    parse_id = str(uuid.uuid4())
    
    r.hmset(parse_id, data)
    r.expire(parse_id, ttl)
    celery_id = parsing_celery.delay(mail, number_adds, city, price1, price2)
    celery_id_result = celery_id.id
    result = celery.AsyncResult(celery_id_result)
    cars_value = result.get()
    string = '\n'.join([str(item) for item in cars_value])
    r2.hset(parse_id ,parse_id, string)
    r2.expire(parse_id, ttl) 

    return {"Message": "Parser started"}


def open_history_by_id():
    r2 = redis.Redis(charset="utf-8", decode_responses=True, db=2)
    s = r2.keys()
    a = []
    for key in s:
        a.append(r2.hgetall(key))
    return a
open_history_by_id()

def get_titles():
    r2 = redis.Redis(charset="utf-8", decode_responses=True, db=2)
    s = r2.keys()
    return s

def get_information_by_titles():
    r2 = redis.Redis(charset="utf-8", decode_responses=True, db=2)
    s = r2.keys()

def give_titles():
    r = redis.Redis(charset="utf-8", decode_responses=True)
    s = r.keys()
    
