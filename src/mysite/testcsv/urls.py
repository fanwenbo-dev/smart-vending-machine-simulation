from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_csv, name='update_csv'),
    path('updated/', views.csv_updated, name='csv_updated'),
    path('rawcsv/', views.rawcsv, name='rawcsv'),
    path('payproc', views.payproc, name='payproc'),
    path('update/images/full.jpg', views.serve_image, name='serve_image'),
    path('updated/qrs/<str:image_name>.png', views.serve_qr_image, name='serve_qr_image'),
]
