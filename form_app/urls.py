from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_list, name='form_list'),
    path('forms/<int:form_id>/', views.form_detail, name='form_detail'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('forms/<int:form_id>/analytics/', views.form_analytics, name='form_analytics'),
]
