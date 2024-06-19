from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()
TASKS = []
STATUS_VARIABLE = ['DONE', 'IN PROGRESS', 'NOT STARTED']


class Task(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str


class TaskIn(BaseModel):
    name: str
    description: Optional[str]
    status: str


@app.get('/tasks', response_model=list[Task])
async def tasks():
    return TASKS


@app.get('/tasks/{task_id}', response_model=Task)
async def some_task(task_id: int):
    return TASKS[task_id - 1]


@app.post('/tasks', response_model=list[Task])
async def add_task(new_task: TaskIn):
    if new_task.status in STATUS_VARIABLE:
        TASKS.append(
            Task(id=len(TASKS) + 1,
                 name=new_task.name,
                 description=new_task.description,
                 status=new_task.status)
        )
        return TASKS
    raise HTTPException(status_code=404, detail='STATUS DOES NOT EXIST')


@app.put('/tasks/{task_id}', response_model=list[Task])
async def update_task(task_id: int, new_task: TaskIn):
    if task_id - 1 in range(len(TASKS)):
        cur_task = TASKS[task_id-1]
        cur_task.name = new_task.name
        cur_task.description = new_task.description
        cur_task.status = new_task.status
        return TASKS
    raise HTTPException(status_code=404, detail='Task not found')


@app.delete('/tasks/{task_id}', response_model=dict)
async def delete_task(task_id: int):
    if task_id - 1 in range(len(TASKS)):
        if task_id == TASKS[task_id-1].id:
            removed_task = TASKS.pop(task_id-1)
            return {'delete': removed_task}
    raise HTTPException(status_code=404, detail='Task not found')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )