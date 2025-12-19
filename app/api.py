from ninja import NinjaAPI
from routers import products, faq

api = NinjaAPI()

api.add_router('products/', products.router)
api.add_router('faqs/', faq.router)