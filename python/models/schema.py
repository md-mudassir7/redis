from enum import Enum
from pydantic import BaseModel

class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class Task(BaseModel):
    title: str
    description: str
    due_date: str
    status : TaskStatus
