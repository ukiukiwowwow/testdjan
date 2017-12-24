from django.conf.urls import url

from . import views

app_name='register_page'
urlpatterns =[
    url(r'^$',views.LoginView.as_view(),name='login'),
]