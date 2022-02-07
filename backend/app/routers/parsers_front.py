from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from celery_worker import parsing_celery, celery, checking
import redis
import uuid
from parse_try import converter
from celery_status_check import get_celery_worker_status

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")

# @router.get("/check_redis/")
# def new_parse_home(request: Request):
#     return templates.TemplateResponse("check_redis.html", {"request": request})

# @router.post("/check_redis/")
# async def checking_redis(request: Request):
#     form = await request.form()
#     number_adds = int(form.get("num_adds"))
#     mail = form.get("email")
    
#     try:
#         city = form.get("city")
#         price1 = int(form.get("price1"))
#         price2 = int(form.get("price2"))
#     except:
#         city = None
#         price1 = None
#         price2 = None
#     r = redis.Redis(charset="utf-8", decode_responses=True)
#     data = {
#         "email": str(mail),
#         "number_of_adds": str(number_adds),
#         "city": str(city), 
#         "price1": str(price1),
#         "price2": str(price2)        
#     }
#     ttl = 604800
#     parse_id = str(uuid.uuid4())


#     for key in r.keys():
#         if r.hgetall(key) == data:
#             return {"Message": "This request is finded"}
#     r.hmset(parse_id, data)
#     r.expire(parse_id, ttl)
#     return {"Message": "Parsing started"}



@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.get("/new_parser/")
def new_parse_home(request: Request):
    list_of_celery = get_celery_worker_status()
    return templates.TemplateResponse("new_parser_page.html", {"request": request, "list_of_celery": list_of_celery})

@router.post("/new_parser/")
async def create_new_parser(request: Request):
    form = await request.form()
    number_adds = int(form.get("num_adds"))
    mail = form.get("email")
    
    try:
        city = form.get("city")
        price1 = int(form.get("price1"))
        price2 = int(form.get("price2"))
    except:
        city = None
        price1 = None
        price2 = None

    if price1 is not None and price2 is not None:
        if price1 > price2:
            return {"Message": "<Price1> can't be more than <price2>"}
        else:
            celery_id = parsing_celery.delay(mail, number_adds, city, price1, price2)
            celery_id_result = celery_id.id
            result = celery.AsyncResult(celery_id_result)
            cars_value = result.get()
            # return cars_value
            converter()
            return templates.TemplateResponse("kolesa.html", {"request": request})
    print("phase3")
    
    # asyncres = checking_cash(mail, number_adds, city, price1, price2)
    # asyncres_id = asyncres.id
    # result = celery.AsyncResult(asyncres_id)

    celery_id = parsing_celery.delay(mail, number_adds, city, price1, price2)
    # celery_id_result = celery_id.id
    # result = celery.AsyncResult(celery_id_result)
    
    print(celery.state)
    # cars_value = result.get()
    # return cars_value
    converter()
    return templates.TemplateResponse("kolesa.html", {"request": request})
    # return checking_cash(mail, number_adds, city, price1, price2)


# @router.get("/history/")
# def show_history(request: Request):
#     history_list = open_history_by_id()
#     titles = get_titles()
#     return templates.TemplateResponse("history.html", {"request": request, "history_list": history_list, "titles": titles})


@router.get("/settask/")
def settask(request: Request):
    res = checking.delay()
    result = res.id
    return result

@router.get("/gettask/{task_id}")
def gettask(request: Request, task_id):
    r3 = redis.Redis(charset="utf-8", decode_responses=True, db=3) 
    task_id = task_id
    task_redis_name = f'celery-task-meta-{task_id}'
    if task_redis_name in r3.keys():
        result = celery.AsyncResult(task_id)
        return result.state
    return "No id was provided"
