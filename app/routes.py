from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from app.schemas import ImageDataMany, StatusEnum
from app.services import fetch_request, save_request
from app.tasks import process_image_task
from app.utils import convert_dict_to_csv, parse_csv

router = APIRouter()


@router.post("/upload/")
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


@router.get("/status/{request_id}")
async def get_status(request_id: str):
    request_status = await fetch_request(request_id)
    if not request_status:
        return {"message": "Request not found."}
    status = request_status.get("status", StatusEnum.pending.value)
    return {
        "status": status,
    }


@router.get("/download/{request_id}")
async def get_csv(request_id: str):
    data = await fetch_request(request_id)
    status = data.get("status", StatusEnum.pending.value)
    if status != StatusEnum.completed.value:
        return {"message": "Request is still in progress. Please try again later."}
    output = convert_dict_to_csv(data)
    response = StreamingResponse(output, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=image_data.csv"
    return response
