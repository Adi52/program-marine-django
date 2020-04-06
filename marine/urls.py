from django.urls import path


from . import views

app_name = 'marine'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_book/<int:parking_place_id>/', views.new_book, name='new_book'),
    path('new_book/congrats/<int:parking_place_id>/<str:secret_key>/', views.congrats, name='congrats'),
    path('new_book/congrats/<int:parking_place_id>/<str:secret_key>/download/', views.create_and_download_declaration,
         name='download'),
]