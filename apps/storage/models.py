from django.db import models
from django.conf import settings
from django.utils import timezone

class Warehouse(models.Model):
    city = models.CharField('Город', max_length=100)
    address = models.CharField('Адрес', max_length=250)
    feature = models.CharField(
        'Особенность',
        max_length=200,
        blank=True
    )
    image = models.ImageField(
        'Фото склада',
        upload_to='warehouses/',
        blank=True
    )
    price_per_square_meter = models.PositiveIntegerField('Цена за м² в месяц, ₽')
    temperature = models.IntegerField('Температура на складе')
    contacts = models.TextField('Контакты склада', blank=True, default='')
    description = models.TextField('Описание склада', blank=True, default='')
    route = models.TextField('Как проехать', blank=True, default='')
    class Meta:
        verbose_name = 'Cклад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.city} {self.address}'


class Box(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='boxes')
    number = models.CharField('Номер бокса', max_length=20)
    floor = models.PositiveSmallIntegerField('Этаж')
    length = models.DecimalField('Длина, м', max_digits=4, decimal_places=1)
    width = models.DecimalField('Ширина, м', max_digits=4, decimal_places=1)
    height = models.DecimalField('Высота, м', max_digits=4, decimal_places=1)
    size = models.DecimalField(
        'Площадь, м²',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True
    )
    price_per_month = models.DecimalField(
        'Цена в месяц, ₽',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    is_occupied = models.BooleanField('Занят', default=False)

    class Meta:
        verbose_name = 'Контейнер'
        verbose_name_plural = 'Контейнеры'

    def __str__(self):
        return f'{self.number} ({self.warehouse.city})'


class Order(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('expired', 'Истекла'),
        ('cancelled', 'Отменена'),
        ('completed', 'Завершена')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователб"
    )
    box = models.ForeignKey(
        Box,
        on_delete=models.PROTECT,
        related_name="rentals",
        verbose_name="Бокс"
    )
    price_per_month = models.DecimalField(
        'Цена за месяц (на момент аренды)',
        max_digits=10,
        decimal_places=2
    )
    total_price = models.DecimalField(
        'Итоговая стоимость',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')

    def __str__(self):
        return f'Аренда #{self.id} – {self.box} ({self.user})'

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['-start_date']




