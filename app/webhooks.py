from fastapi import APIRouter, File, UploadFile

from app.schemas import ImageDataMany
from app.services import save_request
from app.tasks import process_image_task
from app.utils import parse_csv

webhook = APIRouter()


@webhook.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    image_data, _ = parse_csv(content)
    validated_data = (
        ImageDataMany.model_validate({"image_data": image_data})
        .model_dump()
        .get("image_data")
    )
    request_id = await save_request(validated_data)
    process_image_task.delay(
        objs=validated_data,
        request_id=request_id,
    )
    return {"request_id": request_id}
