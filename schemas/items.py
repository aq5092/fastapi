from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
# Compare this snippet from schemas/items.py: