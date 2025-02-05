from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Категория')
    icon = models.ImageField(upload_to='icons/', blank=True, null=True, verbose_name='Иконка')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subcategories', verbose_name='Родитель')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return '-'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    description = models.CharField(max_length=300, verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    quantity = models.IntegerField(default=0, verbose_name='В наличии')
    slug = models.SlugField(unique=True, null=True)
    color_name = models.CharField(max_length=100, verbose_name='Цвет название')
    color_code = models.CharField(max_length=100, verbose_name=' Цвет код')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='products')
    discount = models.IntegerField(null=True, blank=True, default=0, verbose_name='Скидка')
    width = models.CharField(max_length=150, null=True, blank=True, verbose_name='Ширина')
    height = models.CharField(max_length=150, null=True, blank=True, verbose_name='Высота')
    length = models.CharField(max_length=150, null=True, blank=True, verbose_name='Глубина')
    kind = models.ForeignKey('KindCategory', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Вид', related_name='kind')
    model = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Модель', related_name='model')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})



    def get_product_image(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return '-'
        else:
            return '-'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ImageProduct(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар',
                                related_name='images')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'



class KindCategory(models.Model):
    title = models.CharField(max_length=150, verbose_name='Вид мебели')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вид мебели'
        verbose_name_plural = 'Вид мебели'


class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Модель мебели')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'



class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='Товар')

    def __str__(self):
        return f'Пользователь: {self.user.username} - Товар {self.product.title}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, verbose_name='Город', null=True, blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', null=True, blank=True)
    home = models.CharField(max_length=50, verbose_name='Дом №:', null=True, blank=True)
    flat = models.CharField(max_length=50, verbose_name='Квартира №: ', null=True, blank=True)

    def __str__(self):
        return f'Пользователь: {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# ========================================================================
# Модели для работы с корзиной
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, default='', verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=100, default='', verbose_name='Фамилия покупателя')
    telegram = models.CharField(max_length=50, blank=True, null=True, verbose_name='Телеграм')

    def __str__(self):
        return f'Пользователь: {self.user.username} имя: {self.first_name}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Статус заказа')
    shipping = models.BooleanField(default=False, verbose_name='Доставка')

    def __str__(self):
        return f'Покупатель: {self.customer.first_name} номер заказа: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # Методы которые вернут сумму заказа и ко-во заказанных товаров
    @property  # метод который подсчитывает общую стоимость заказа
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])  # считаем обш стоимость чека
        return total_price

    @property  # метод который подсчитывает общее кол-во товара
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ №: ')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'Продукт {self.product.title} заказа №: {self.order.id}'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    def total_price(self):   # Метод для получени суммы товаров в их кол-ве
        total_price = self.product.price * self.quantity
        return total_price

    @property
    def get_total_price(self):   # Метод для получени суммы товаров в их кол-ве
        if self.product.discount:
            proc = (self.product.price * self.product.discount) / 100
            self.product.price -= proc

        total_price = self.product.price * self.quantity
        return total_price




class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order,  on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=200, verbose_name='Адрес (ул, дом, кв)')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион')
    city = models.CharField(max_length=100, verbose_name='Город')
    phone = models.CharField(max_length=100, verbose_name='Номер телефона')
    comment = models.TextField(max_length=400, null=True, blank=True, verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')


    def __str__(self):
        return f'Доставка для {self.customer.first_name}z'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставок'



class Region(models.Model):
    region = models.CharField(max_length=100, verbose_name='Регион')

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'



class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order_number = models.IntegerField(verbose_name='Номер заказа')
    total_price = models.FloatField(default=0, verbose_name='Сумма чека')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    completed = models.BooleanField(default=False, verbose_name='Статус заказа')

    def __str__(self):
        return f'Закза №: {self.order_number} Покупателя {self.customer.user.username}'

    class Meta:
        verbose_name = 'Сохранённый заказ'
        verbose_name_plural = 'Сохранённые заказы'



class SaveOrderProduct(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, related_name='products', verbose_name='Закза')
    product = models.CharField(max_length=500, verbose_name='Название товара')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product_price = models.FloatField(verbose_name='Цена товара')
    final_price = models.FloatField(verbose_name='На сумму')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото товара')
    color_name = models.CharField(max_length=100, verbose_name='Цвет товара')


    def __str__(self):
        return f'Товар {self.product} закза №: {self.order.order_number} '

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            return '-'


class OfferUser(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя пользователя')
    email = models.EmailField(verbose_name='Почта пользователя')
    offer = models.TextField(verbose_name='Предложение пользователя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продложение'
        verbose_name_plural = 'Предложения покупатеелй'



