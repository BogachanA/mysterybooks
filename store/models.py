# -*- coding: utf-8 -*-

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def cover_upload_path(instance, filename):
    return '/'.join(['books', str(instance.id), filename])


class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Book(models.Model):
    title=models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    description=models.TextField()
    publish_date=models.DateField(default=timezone.now)
    price=models.DecimalField(decimal_places=2,max_digits=8)
    stock=models.IntegerField(default=0)
    cover_image=models.ImageField(upload_to=cover_upload_path, default='books/empty_cover.jpg')

    def __unicode__(self):
        return "%s" % (self.title)


class Review(models.Model):
    book=models.ForeignKey(Book)
    user=models.ForeignKey(User)
    publish_date=models.DateField(default=timezone.now)
    text=models.TextField()
    latitude=models.FloatField(max_length=20, default=37.41920)
    longitude = models.FloatField(max_length=20, default="122.8574")


class Cart(models.Model):
    user= models.ForeignKey(User)
    active=models.BooleanField(default=True)
    order_date=models.DateField(null=True)
    payment_type=models.CharField(max_length=100, null=True)
    payment_id=models.CharField(max_length=100, null=True)

    def add_to_cart(self,book_id):
        book = Book.objects.get(pk=book_id)
        try:
            preexisting_order = BookOrder.objects.get(book=book, cart=self)
            preexisting_order.quantity+=1
            preexisting_order.save()
        except BookOrder.DoesNotExist:
            new_order=BookOrder.objects.create(
                book=book,
                cart=self,
                quantity=1,
            )
            new_order.save()

    def remove_from_cart(self,book_id):
        book=Book.objects.get(pk=book_id)
        try:
            preexisting_order=BookOrder.objects.get(book=book, cart=self)
            if preexisting_order.quantity>1:
                preexisting_order.quantity-=1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except BookOrder.DoesNotExist:
            pass


class BookOrder(models.Model):
    book=models.ForeignKey(Book)
    cart=models.ForeignKey(Cart)
    quantity=models.IntegerField()
