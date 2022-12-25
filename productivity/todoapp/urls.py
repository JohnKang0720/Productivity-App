from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit/<int:user_id>", views.edit, name="edit"),
    path("send", views.send, name="send"),
    path("urgency", views.urgency, name="urgency"),
    path("all_folders", views.all_folders, name="all"),
    path("folder/<str:name>", views.specific_folder, name="folder"),
    path("performance", views.performance, name="performance")
]