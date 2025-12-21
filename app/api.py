from ninja import NinjaAPI
from routers import products, faq, order

api = NinjaAPI()

api.add_router('products/', products.router)
api.add_router('faqs/', faq.router)
api.add_router('order/', order.router)