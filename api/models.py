from pydantic import BaseModel

from typing import Mapping, Any, Union


class TriggerRequest(BaseModel):
    company_id: int
    feed_id: int


class TriggerResponse(BaseModel):
    task_id: str = "12312312"
    message: str = "success"
