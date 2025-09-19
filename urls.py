from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # API endpoints
    path("api/login/", views.login_view, name="login"),
    path("api/users/", views.manage_users_view, name="manage_users"),
    path("api/sections/<str:section_id>/", views.section_data, name="section_data"),
    path("api/sections/<str:section_id>/files/", views.attach_file_view, name="attach_file"),
]
