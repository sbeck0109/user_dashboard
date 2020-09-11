from django.urls import path, include

urlpatterns = [
    # path('', include('loginReg_app.urls', namespace='loginReg')),
    path('', include('dojo_wall_app.urls', namespace='dojo_wall')),
    path('dashboard/', include('user_dashboard_app.urls', namespace='dashboard')),
]
