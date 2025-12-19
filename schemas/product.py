from decimal import Decimal
from typing import List, Optional
from ninja import Schema

class ImageSchema(Schema):
    image : str

class SpecificationSchema(Schema):
    name: str
    value: str

class CategorySchema(Schema):
    name: str
    slug: str

class GroupProductShema(Schema):
    name: str
    slug:str
    description: str
    price: Decimal
    discount: Decimal
    feature: bool
    category: CategorySchema
    images: Optional[List[ImageSchema]] = None

class SingleProductSchema(Schema):
    name: str
    slug: str
    description: str
    price: Decimal
    discount: Decimal
    feature: bool
    category: CategorySchema
    images: Optional[List[ImageSchema]] = None
    specifications: Optional[List[SpecificationSchema]] = None
    video: Optional[str] = None
