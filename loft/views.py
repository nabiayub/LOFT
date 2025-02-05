from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegistrationForm, CustomerForm, ShippingForm, EditAccountForm, EditProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CartForAuthenticatedUser, get_cart_data
import stripe
from shop import settings
from django.contrib import messages

# Create your views here.
class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    template_name = 'loft/index.html'
    extra_context = {
        'title': 'LOFT мебель для дома'
    }

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories



class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'loft/category_page.html'
    paginate_by = 3

    def get_queryset(self):
        color_field = self.request.GET.get('color')
        kind_field = self.request.GET.get('kind')
        from_field = self.request.GET.get('from_p')
        till_field = self.request.GET.get('till_p')

        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        if color_field:
            products = products.filter(color_name=color_field)
        if kind_field:
            products = products.filter(kind__title=kind_field)
        if from_field:
            products = [i for i in products if int(i.price) >= int(from_field)]
        if till_field:
            products = [i for i in products if int(i.price) <= int(till_field)]

        return products



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)
        colors = list(set(i.color_name for i in products))
        discounts = list(set(i.discount for i in products))
        kinds = list(set(i.kind for i in products))
        prices = [i for i in range(500000, 5000000, 500000)]
        context['colors'] = colors
        context['discounts'] = discounts
        context['kinds'] = kinds
        context['prices'] = prices
        context['color'] = self.request.GET.get('color')
        context['kind'] = self.request.GET.get('kind')
        context['from'] = self.request.GET.get('from_p')
        context['till'] = self.request.GET.get('till_p')

        context['title'] = category.title
        return context



class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(kind__title=product.kind)
        products = [i for i in products if i != product]
        context['products'] = products
        context['title'] = product.title
        return context



def get_product_by_color(request, color, model):
    product = Product.objects.get(color_code=color, model__title=model)
    products = Product.objects.filter(kind__title=product.kind)
    products = [i for i in products if i != product]
    context = {
        'title': product.title,
        'product': product,
        'products': products
    }

    return render(request, 'loft/product_detail.html', context)


def save_favorite_product(request, slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=slug)
    favorite_products = FavoriteProduct.objects.filter(user=user)
    if user:
        if product in [i.product for i in favorite_products]:
            fav_product = FavoriteProduct.objects.get(product=product, user=user)
            fav_product.delete()
        else:
            FavoriteProduct.objects.create(product=product, user=user)

    next_page = request.META.get('HTTP_REFERER', 'main')  # Получим Адрес страницы с которой был запрос
    return redirect(next_page)



class FavoriteListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'loft/favorite_list.html'
    login_url = 'login'
    extra_context = {
        'title': 'Избранные товары'
    }

    # Переназначим вывод что бы полить имзбранное конкретного пользователя
    def get_queryset(self):
        user = self.request.user
        favorite_products = FavoriteProduct.objects.filter(user=user)
        products = [i.product for i in favorite_products]
        return products



def user_login(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    messages.success(request, 'Авторизация прошла успешно')
                    return redirect('main')
                else:
                    messages.error(request, 'Не верный логин или пароль')
                    return redirect('login')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')

        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация',
            'form': form
        }

        return render(request, 'loft/login.html', context)



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request, 'Уже уходите 😥')
        return redirect('main')
    else:
        return redirect('main')



def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                phone = request.POST.get('phone')
                profile = Profile.objects.create(user=user, phone=phone)
                profile.save()
                return redirect('login')
            else:
                return redirect('register')

        else:
            form = RegistrationForm()

        context = {
            'title': 'Регистарция',
            'form': form
        }
        return render(request, 'loft/register.html', context)


# Вьюшка для корзины
def my_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Ваша корзина',
            'products': cart_info['order_products'],  # Список заказанных товаров
            'order': cart_info['order']
        }

        return render(request, 'loft/my_cart.html', context)



# Вьюшка на добаление товара в корзину
def to_cart_view(request, product_slug, action):
    if not request.user.is_authenticated:
        return ('login')
    else:
        user_cart = CartForAuthenticatedUser(request, product_slug, action)
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)



# Вьюшка для удаление товара из корзины
def delete_order_product_view(request, pk, order):
    user = request.user if request.user.is_authenticated else None
    if user:
        order_product = OrderProduct.objects.get(pk=pk, order=order)
        order_product.delete()
        return redirect('my_cart')
    else:
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)



def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        cart_info = get_cart_data(request)

        context = {
            'cart_total_quantity': cart_info['cart_total_quantity'],
            'order': cart_info['order'],
            'items': cart_info['order_products'],

            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm(),
            'title': 'Оформление Заказа'
        }
        return render(request, 'loft/checkout.html', context)




# Вьюшка для оплаты
def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            user_cart = CartForAuthenticatedUser(request)
            cart_info = user_cart.get_cart_info()

            customer_form = CustomerForm(data=request.POST)
            shipping_form = ShippingForm(data=request.POST)
            if customer_form.is_valid() and shipping_form.is_valid():
                # Сохраняем данные покупателя
                customer = Customer.objects.get(user=request.user)
                customer.first_name = customer_form.cleaned_data['first_name']
                customer.last_name = customer_form.cleaned_data['last_name']
                customer.telegram = customer_form.cleaned_data['telegram']
                customer.save()
                # Сохраняем данные адреса доставки
                address = shipping_form.save(commit=False)
                address.customer = Customer.objects.get(user=request.user)
                address.order = user_cart.get_cart_info()['order']
                address.save()
            else:
                return redirect('checkout')

            total_price = cart_info['cart_total_price']
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'rub',
                        'product_data': {'name': 'Товары LOFT'},
                        'unit_amount': int(total_price) * 100
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('checkout'))
            )
            return redirect(session.url, 303)

        else:
            return redirect('checkout')


def success_payment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        order = cart_info['order']
        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_cart_total_price,
                                              order_number=order.pk)

        order_save.save()
        order_products = order.orderproduct_set.all()
        for item in order_products:
            save_order_product = SaveOrderProduct.objects.create(order_id=order_save.pk,
                                                                 product=str(item),
                                                                 quantity=item.quantity,
                                                                 product_price=item.product.price,
                                                                 final_price=item.get_total_price,
                                                                 photo=item.product.get_product_image(),
                                                                 color_name=item.product.color_name)
            save_order_product.save()

        user_cart.clear_cart()
        messages.success(request, 'Оплата прошла успешно')
        context = {
            'title': 'Результат оплаты'
        }
        return render(request, 'loft/success.html', context)



def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            form1 = EditAccountForm(request.POST, instance=request.user)
            form2 = EditProfileForm(request.POST, instance=request.user.profile)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                messages.success(request, 'Данные изменены')
                return redirect('profile')

        else:
            form1 = EditAccountForm(instance=request.user)
            form2 = EditProfileForm(instance=request.user.profile)

        profile = Profile.objects.get(user=request.user)
        if profile:
            try:
                customer = Customer.objects.get(user=request.user)
                orders = SaveOrder.objects.filter(customer=customer)
            except:
                orders = []
            context = {
                'orders': orders[::-1][:1],
                'title': f'Профиль: {profile.user.username}',
                'form1': form1,
                'form2': form2
            }

            return render(request, 'loft/profile.html', context)
        else:
            return redirect('login')


def customer_orders_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        try:
            customer = Customer.objects.get(user=request.user)
            orders = SaveOrder.objects.filter(customer=customer)
        except:
            orders = []
        context = {
            'orders': orders[::-1],
            'title': f'Все заказы:'
        }

        return render(request, 'loft/orders.html', context)




def send_mail_views(request):
    if request.user.is_superuser:
        from shop import settings
        from django.core.mail import send_mail
        if request.method == 'POST':
            text = request.POST.get('text')
            users = User.objects.all()
            mail_list = [i.email for i in users]
            for email in mail_list:
                mail = send_mail(
                    subject='У нас дял уникальное предложение',
                    message=text,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False
                )
                print(f'Сообщение отправленно на почту {email} - {"Успешно" if bool(mail) else "Не успешно"}')

            messages.success(request, 'Рассылка выполенена')
            return redirect('send_mail')

        else:
            pass

        context = {
            'title': 'Расслка сообщений'
        }
        return render(request, 'loft/send_mail.html', context)

    else:
        return redirect('main')




def about_view(request):

    context = {
        'title': 'О компании LOFT'
    }

    return render(request, 'loft/about.html', context)



def offer_user_view(request):
    if request.method == 'POST':
        offer = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        if offer and name and email:
            offer = OfferUser.objects.create(offer=offer, name=name, email=email)
            offer.save()
            messages.success(request, 'Мы рссмотрим ваше предложение. Спасибо за отзыв')
            return redirect('offer')
        else:
            messages.warning(request, 'Вы не заполнили поле')
            return redirect('offer')
    else:
        pass

    context = {
        'title': 'Связатся с нами'
    }

    return render(request, 'loft/offer.html', context)





