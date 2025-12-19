from django.contrib import admin
from .models import Product, Category, ProductSpecificationValue, Specification, Image, Video, FAQ

# Register your models here.
class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

class VideoInline(admin.StackedInline):
    model = Video
    extra =1
    max_num = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SpecificationInline]
    prepopulated_fields = {'slug': ('name',)}


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "specification":
            # If we're editing a product, limit specs to those of its category
            if request.resolver_match.kwargs.get('object_id'):
                product = Product.objects.get(pk=request.resolver_match.kwargs['object_id'])
                kwargs["queryset"] = Specification.objects.filter(category=product.category)
            else:
                # New product: show empty (will be handled after category selection)
                kwargs["queryset"] = Specification.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationValueInline, VideoInline, ImageInline]
    list_display = ['name', 'category', 'price', 'available']
    list_filter = ['category', 'available']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    # # Optional: Improve UX by grouping specs
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'category', 'description', 'price', 'available')
    #     }),
    # )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question']