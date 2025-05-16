from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.login_view,name="login"),
    path('logout/', views.logout_view,name="logout"),
    path('register/', views.register_view,name="register"),
    path('create_form/', views.create_item_view, name="create"),
    path('item_list/', views.item_list_view, name="items"),
    path('item_delete/<int:item_id>/', views.delete_item_view, name="delete"),
    path('item_edit/<int:item_id>/', views.item_edit_view, name="edit"),
    path('archive/', views.archive_dataset_view, name="archive"),
    path('archive_view/', views.archive_view, name="archive_view"),
    path('archive_clear/', views.archive_clear_view, name="clear_archive"),
    path('archive/delete/<int:group_id>/', views.archive_delete_view, name='delete_archive'),

]

