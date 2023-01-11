from django.urls import path

from users import views

app_name = "users"

urlpatterns = [path("register/", views.CreateUserView.as_view(), name="register")]