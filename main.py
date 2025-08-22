from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select, delete
from db import engine, get_session
from typing import Annotated, List
from models import TaskBase, Task, UpdateTaskStatus
from datetime import date
from contextlib import asynccontextmanager






@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
            
            if session.exec(select(Task)).first():
                session.exec(delete(Task)) 
                session.commit()


            session.add_all([
                Task(title="Tesco Shop", desc="Milk, Bread, Eggs", status='todo', due=date(2025, 9, 21)),
                Task(title="CV Fixes", status='todo', due=date(2025, 9, 29)),
                Task(title="Interview prep", status='todo', due=date(2025, 9, 23)),
            ])
            session.commit()
    yield



app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get('/tasks', response_model=List[Task])
def get_all_tasks(session: SessionDep):
    result = session.exec(select(Task)).all()
    if not result:
         raise HTTPException(status_code=404, detail='There are currently no tasks.')
    return result



@app.get('/task/{task_id}', response_model=Task)
def get_tasks_by_id(task_id: int, session: SessionDep):
     task = session.get(Task, task_id)
     if not task:
          raise HTTPException(status_code=404, detail=f'No task with id: {task_id}.')
     return task


@app.post('/task', response_model=Task)
def post_new_task(payload: TaskBase, session: SessionDep):
     db_task = Task.model_validate(payload)
     session.add(db_task)
     session.commit()
     session.refresh(db_task)
     return db_task


@app.delete('/task/{task_id}')
def delete_task_by_id(task_id: int, session: SessionDep):
     task_to_delete = session.get(Task, task_id)
     if not task_to_delete:
          raise HTTPException(status_code=404, detail=f'Delete failed. No task with id: {task_id}')
     session.delete(task_to_delete)
     session.commit()
     return {'message': f'Task {task_id} successfully deleted.'}


@app.patch('/task/{task_id}', response_model=TaskBase)
def patch_task_status_by_id(task_id: int, payload: UpdateTaskStatus, session: SessionDep):
     task_to_patch = session.get(Task, task_id)
     if not task_to_patch:
          raise HTTPException(status_code=404, detail=f'Status update failed. No task with id: {task_id}.')
     task_to_patch.status = payload.status
     session.add(task_to_patch)
     session.commit()
     session.refresh(task_to_patch)

     return task_to_patch