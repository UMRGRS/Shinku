from django.urls import path

from . import views

urlpatterns = [
    path("encryption_tests", views.encrypt_decrypt, name='index')
]