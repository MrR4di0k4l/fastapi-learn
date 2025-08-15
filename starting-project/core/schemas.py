from pydantic import BaseModel


class BaseSchemas(BaseModel):
    name: str
    age: int


class ItemCreateSchemas(BaseSchemas):
    pass


class ItemResponseSchemas(BaseSchemas):
    id: int
    
    
class ItemUpdateSchemas(BaseSchemas):
    pass