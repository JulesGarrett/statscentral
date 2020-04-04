from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('edit', views.account_edit, name='account_edit'),

]
