from typing import List
from ninja.router import Router
from model.models import FAQ
from schemas.faq import FaqSchema

router = Router()


@router.get("", response=List[FaqSchema])
def get_faqs(request):
    try:
        faqs = FAQ.objects.all()
        return faqs
    except Exception as e:
        print("error", str(e))
        return []
