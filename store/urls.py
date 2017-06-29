from django.conf.urls import include, url
from . import views


urlpatterns=[

    url(r'^$', views.store, name="index"),
    url(r'^book/(\d+)', views.book_details, name='book_details')

]