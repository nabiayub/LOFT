from .models import Product, OrderProduct, Order, Customer


class CartForAuthenticatedUser:
    def __init__(self, request, product_slug=None, action=None):
        self.user = request.user

        if product_slug and action:
            self.add_or_delete(product_slug, action)

    # Метод для получения товаров Корзины
    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)

        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.orderproduct_set.all()

        cart_total_price = order.get_cart_total_price
        cart_total_quantity = order.get_cart_total_quantity

        return {
            'cart_total_price': cart_total_price,
            'cart_total_quantity': cart_total_quantity,
            'order': order,
            'order_products': order_products
        }

    # Метод добавления или удаления товара из корзины
    def add_or_delete(self, product_slug, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(slug=product_slug)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0 and product.quantity > order_product.quantity:
            order_product.quantity += 1

        elif action == 'delete':
            order_product.quantity -= 1

        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear_cart(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            item = Product.objects.get(pk=product.product.pk)
            item.quantity -= product.quantity
            item.save()
            product.delete()

        order.delete()



def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()
    return cart_info





