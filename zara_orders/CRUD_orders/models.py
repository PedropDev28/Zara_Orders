from django.db import models

class Order(models.Model):
    url = models.URLField()
    language = models.CharField(max_length=10)
    order_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50)
    mpn = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    description = models.TextField()
    price = models.TextField() 
    currency = models.CharField(max_length=10)
    availability = models.CharField(max_length=20)
    condition = models.CharField(max_length=20)
    images = models.TextField()  # Usa un TextField si quieres almacenar varias URLs separadas por "~"
    color = models.CharField(max_length=255)
    size_list = models.CharField(max_length=50)
    scraped_at = models.DateTimeField()

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"{self.name} - {self.order_id}"