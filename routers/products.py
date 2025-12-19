from typing import List
from ninja.router import Router
from model.models import Category, Product
from schemas.product import CategorySchema, GroupProductShema, SingleProductSchema

router = Router()


@router.get("/all", response=List[SingleProductSchema])
def get_feature_product(request, offset: int = 0, limit: int = 100):
    try:
        products = Product.objects.select_related("category").prefetch_related(
            "images", "specifications", "video"
        )[offset:limit]
        res_list = []

        for product in products:
            images = [{"image": img.image.url} for img in product.images.all()]
            specifications = [
                {"name": spec.specification.name, "value": spec.value}
                for spec in product.specifications.all()
            ]
            video_obj = product.video.first()  # get first video object or None
            video_url = video_obj.video.url if video_obj else None

            res_list.append(
                {
                    "name": product.name,
                    "slug": product.slug,
                    "description": product.description,
                    "price": product.price,
                    "discount": product.discount,
                    "feature": product.feature,
                    "images": images,
                    "specifications": specifications,
                    "category": product.category,
                    "video": video_url,
                }
            )
        return res_list
    except Exception as e:
        print("error", str(e))
        return []


@router.get("/categories", response=List[CategorySchema])
def get_categories(request):
    try:
        cats = Category.objects.all()
        print(cats)
        return cats
    except Exception as e:
        print("error", str(e))

@router.get("/{slug}", response=SingleProductSchema)
def get_product(request, slug: str):
    try:
        product = (
            Product.objects.select_related("category")
            .prefetch_related("images", "specifications", "video")
            .get(slug=slug)
        )
        images = [{"image": img.image.url} for img in product.images.all()]
        specifications = [
            {"name": spec.specification.name, "value": spec.value}
            for spec in product.specifications.all()
        ]
        video_obj = product.video.first()
        video_url = video_obj.video.url if video_obj else None

        return {
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "price": product.price,
            "discount": product.discount,
            "feature": product.feature,
            "images": images,
            "specifications": specifications,
            "category": product.category,
            "video": video_url,
        }
    except Exception as e:
        print("error", str(e))
        return []
