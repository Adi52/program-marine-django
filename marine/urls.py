from django.urls import path

from . import views

app_name = 'marine'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_book/<int:parking_place_id>/', views.new_book, name='new_book'),
    path('new_book/<str:secret_key>/', views.congrats, name='congrats'),
    path('new_book/<str:secret_key>/download/', views.create_and_download_declaration,
         name='download'),
    path('new_book/confirm_email/<str:secret_key_email>/', views.confirm_email, name='confirm_mail'),

]
