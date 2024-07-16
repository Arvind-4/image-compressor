from enum import Enum

from pydantic import BaseModel, field_validator


class StatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class ImageData(BaseModel):
    serial_number: int
    product_name: str
    input_image_urls: list[str]
    output_image_urls: list[str] = []

    @field_validator("input_image_urls")
    @classmethod
    def validate_input_image_urls(cls, v, values, **kwargs):
        if isinstance(v, str):
            return [v.strip()]
        if isinstance(v, list):
            return [str(url).strip() for url in v]
        return v


class ImageDataMany(BaseModel):
    image_data: list[ImageData]
