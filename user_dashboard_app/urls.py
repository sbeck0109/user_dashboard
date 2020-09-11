from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='my_index'),

    path('users/<int:user_id>/edit', views.edit, name='user_edit'),
    path('users/<int:user_id>/edit/update', views.update, name='user_update'),
    path('users/<int:user_id>/remove', views.remove_user, name='user_remove')
]
