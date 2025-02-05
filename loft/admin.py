from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm
# Register your models here.

# admin.site.register(Category)
#admin.site.register(Product)
admin.site.register(ImageProduct)
admin.site.register(KindCategory)
admin.site.register(Brand)
admin.site.register(FavoriteProduct)
admin.site.register(Profile)

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(Region)
admin.site.register(OfferUser)


class ImageInlane(admin.TabularInline):
    fk_name = 'product'
    model = ImageProduct
    extra = 1


class SaveOrderProductInline(admin.TabularInline):
    fk_name = 'order'
    model = SaveOrderProduct
    readonly_fields = ['order', 'product', 'color_name', 'quantity', 'product_price',
                       'final_price', 'added_at', 'get_photo']
    exclude = ['photo']
    extra = 0

    def get_photo(self, obj):
        try:
            if obj.photo:
                return mark_safe(f'<img src="{obj.photo}" width="50">')
            else:
                return '-'
        except:
            return '-'

@admin.register(SaveOrder)
class SaveOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_price', 'created_at')
    list_display_links = ('order_number',)
    inlines = [SaveOrderProductInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_icon_category')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}
    form = CategoryForm

    def get_icon_category(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" width="40">')
        else:
            return 'Нет иконки'

    get_icon_category.short_description = 'Иконка'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'quantity', 'model',
                          'price', 'color_name', 'discount', 'created_at', 'get_photo')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'quantity',  'price')
    list_editable = ('category', 'quantity',  'price', 'model')
    inlines = [ImageInlane]
    prepopulated_fields = {'slug': ('title',)}




    def get_photo(self, obj):
        try:
            if obj.images:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="50">')

            else:
                return '-'
        except:
            return '-'

    get_photo.short_description = 'Фото'