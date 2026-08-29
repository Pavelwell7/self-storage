
from .utils import calculate_box_size, calculate_box_price


def update_box_size_and_price(box):
    box.size = calculate_box_size(box.length, box.width)
    box.price_per_month = calculate_box_price(box.size, box.warehouse.price_per_square_meter)
    box.save(update_fields=['size', 'price_per_month'])