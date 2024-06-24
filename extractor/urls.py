from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('pdf-list/', views.pdf_list, name='pdf_list'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('logout/', views.logout_view, name='logout'),
    
]
