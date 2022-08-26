from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    id = models.BigIntegerField(primary_key=True)  # Чтобы использовать те же id, что и сайт-партнер
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.ImageField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
