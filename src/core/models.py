from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "labels"

    def __str__(self):
        return self.name


class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1,
                                    choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    slug = models.SlugField()
    date_modified = models.DateTimeField(auto_now=True)
    seller = models.OneToOneField(Vendor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.title}"


