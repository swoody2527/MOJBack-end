from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class TaskBase(SQLModel):
    title: str
    desc: Optional[str] = None
    status: str
    due: date


class Task(TaskBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)


class UpdateTaskStatus(SQLModel):
    status: str