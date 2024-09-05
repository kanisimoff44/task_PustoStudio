from fastapi import FastAPI

from app.task_two.router import router as task_two_router

app = FastAPI(title="Pusto studio",)

app.include_router(task_two_router)
