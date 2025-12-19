from ninja import Schema

class FaqSchema(Schema):
    id: int
    question: str
    answer: str