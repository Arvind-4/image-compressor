from fastapi import FastAPI

from app.routes import router
from app.webhooks import webhook

app = FastAPI()

app.include_router(prefix="/api", router=router, tags=["api"])
app.include_router(prefix="/webhook", router=webhook, tags=["webhook"])
