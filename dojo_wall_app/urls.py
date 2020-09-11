from django.urls import path
from . import views

app_name = 'dojo_wall'
urlpatterns = [
    path('', views.welcome),
    path('signin', views.loginReg),
    path('process_reg', views.process_reg),
    path('process_login', views.process_login),
    path('index/<int:user_id>', views.index, name='my_user_info'),
    path('new_message/<int:user_id>', views.new_message, name ='new_message'),
    path('wall/<int:user_id>', views.display_new_message, name='my_wall'),
    path('new_comment', views.new_comment),
    path('<int:message_id>/delete_message/<int:user_id>', views.delete_message, name='my_delete_message'),
    # path('<int:comment_id>/delete_comment', views.delete_comment),
    path('log_out', views.log_out)
]
