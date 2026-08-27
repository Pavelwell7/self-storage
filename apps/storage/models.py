from django.db import models



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
    class Meta:
        verbose_name = 'Cклад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'{self.city} {self.address}'


class Box(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='boxes')
    number = models.CharField('Номер бокса', max_length=20)
    floor = models.PositiveSmallIntegerField('Этаж')
    size = models.DecimalField(
        'Площадь, м²',
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True
    )
    length = models.DecimalField('Длина, м', max_digits=4, decimal_places=1)
    width = models.DecimalField('Ширина, м', max_digits=4, decimal_places=1)
    height = models.DecimalField('Высота, м', max_digits=4, decimal_places=1)
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

    def save(self, *args, **kwargs):
        self.size = self.length * self.width
        self.price_per_month = self.warehouse.price_per_square_meter * self.size
        super().save(*args, **kwargs)







