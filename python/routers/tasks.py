from typing import List
from fastapi import APIRouter, Depends, HTTPException
from python.models import schema
from utils.logger import get_logger
from python.redis.client import RedisClient
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError

router = APIRouter(
    prefix="/api/v1",
    tags=["shorts"],
    responses={404: {"description": "Not found"}},
)

logger = get_logger(__name__)

@router.post("/tasks")
async def create_task(task: schema.Task):
    
    logger.info("Recieved task to create %s",task.title)
    redis_client = RedisClient.get_redis_client()
   
    try:
        task_id = len(redis_client.keys()) + 1
        redis_client.hmset(f'task:{task_id}', {
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'status': task.status.value
        })
        return task_id
    except Exception as e:
        logger.error("Error while saving task to redis", e)
        raise HTTPException(
            status_code = 500,
            detail = f"Error while saving task to redis {e}" 
        )
    finally:
        return task
    
@router.get("/tasks",response_model=List[schema.Task])
async def get_all_tasks():
    
    logger.info("fetching all tasks from redis")
    redis_client = RedisClient.get_redis_client()
    tasks = []
    try:
        for key in redis_client.keys("task:*"):
            task_data = redis_client.hgetall(key)
            task = schema.Task(
                title=task_data[b"title"].decode(),
                description=task_data[b"description"].decode(),
                due_date=task_data[b"due_date"].decode(),
                status=schema.TaskStatus(task_data[b"status"].decode()),
            )
            tasks.append(task)
    except Exception as e:
        logger.error("Error while fetching task from redis", e)
        raise HTTPException(
            status_code = 500,
            detail = f"Error while fetching task from redis {e}" 
        )
    finally:
        return tasks
        