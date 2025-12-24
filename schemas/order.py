from decimal import Decimal
from typing import List
from ninja.schema import Schema

class ItemSchema(Schema):
    name: str
    discount: Decimal
    quantities: int

class OrderSchema(Schema):
    name: str
    email: str
    country: str
    city: str
    address: str
    items: List[ItemSchema]
    phone: str