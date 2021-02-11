from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.shortcuts import reverse

# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

CATEGORY_CHOICES = (
    ('S', 'Shirts'),
    ('TS', 'T-Shirts'),
    ('OW', 'Out Sports'),
)

LABELS = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES,
                                max_length=2,
                                default='S')
    labels = models.CharField(choices=LABELS,
                              max_length=1,
                              default='P')
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True)
    description = models.TextField(max_length=300)
    image = models.ImageField()

    class Meta:
        pass

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("core:products", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse("core:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart(self):
        return reverse("core:remove_from_cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False, )

    class Meta:
        pass

    def __str__(self):
        return f"{self.item}"

    def get_total_value(self):
        return self.quantity * self.item.price

    def get_discount_value(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_value() - self.get_discount_value()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_value()
        else:
            return self.get_total_value()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False, )

    class Meta:
        pass

    def __str__(self):
        return f"{self.user.username}  {self.ordered_date}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
