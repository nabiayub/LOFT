from django import template
from loft.models import Category, Product, FavoriteProduct

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)



@register.simple_tag()
def get_products(category):
    return Product.objects.filter(category=category)[::-1][:2]


@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()


@register.simple_tag()
def get_normal_price(price):
    return f"{price:_}".replace("_", " ")

@register.simple_tag()
def get_product_colors(model):
    products = Product.objects.filter(model=model)
    colors = [i.color_code for i in products]
    return colors

@register.simple_tag()
def get_favorite_products(user):
    favs = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in favs]
    return products


@register.simple_tag()
def get_price_discount(total_price, discount=0):
    if discount:
        procent = (total_price * discount) / 100
        return procent










