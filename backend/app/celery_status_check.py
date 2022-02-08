from celery_worker import celery


def get_celery_worker_status():
    i = celery.control.inspect()
    active_tasks = i.active()
    reserved_tasks = i.reserved()
    result = {
        'active_tasks': active_tasks,
        'reserved_tasks': reserved_tasks
    }
    a = []
    try:
        active_tasks_list = result['active_tasks']['celery@dimash-Vostro-5568'][0]['id']
        # for number in range(0, len(result['reserved_tasks']['celery@dimash-Vostro-5568'])):
        #     reserved_tasks_list = result['reserved_tasks']['celery@dimash-Vostro-5568'][number]['id']
        #     a.append(reserved_tasks_list)
            #a is reserved list
        return result
    except:
        return "Ready to parse" 


