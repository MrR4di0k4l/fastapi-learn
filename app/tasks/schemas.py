from pydantic import BaseModel,Field
from datetime import datetime

class TaskBaseSchema(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=300)
    is_completed: bool = Field(default=False)
    
    
class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskUpdateSchema(TaskBaseSchema):
    pass

class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")
    created_at: datetime = Field(..., description="Creation date and time of the object")
    update_at: datetime = Field(..., description="Creation date and time of the object")
    pass