from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_list, name='form_list'),
    path('forms/<int:form_id>/', views.form_detail, name='form_detail'),
    path('thank-you/', views.form_submission_success, name='form_submission_success'),
    path('forms/<int:form_id>/analytics/', views.analytics, name='analytics'),
]
