
from . import views

from django.urls import path

urlpatterns = [
    path('', views.home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('create-record', views.create_record, name="create-record"),

    path('update-record/<int:pk>', views.update_record, name="update-record"),
    path('record/<int:pk>', views.singular_record, name="record"),
    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),






    path('leads/', views.leads_list, name='leads'),
    path('leads/create/', views.create_lead, name='create_lead'),
    path('update-lead/<int:pk>', views.update_lead, name="update-lead"),
    path('leads/<int:pk>', views.singular_lead, name="lead"),
    path('delete-lead/<int:pk>', views.delete_lead, name="delete-lead"),

    path('convert-lead/<int:pk>/', views.convert_lead, name='convert-lead'),
    path('leads/pipeline/', views.lead_pipeline, name='lead-pipeline'),
    path('leads/analytics/', views.lead_status_analytics, name='lead-analytics'),

]