from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_page, name='games_page'),
    
    # Game URLs
    path('games/create/', views.game_create, name='game_create'),
    path('games/update/<int:pk>/', views.game_update, name='game_update'),
    
    # Achivments URLs
    path('achivments/create/', views.achivment_create, name='achivment_create'),
    path('achivments/update/<int:pk>/', views.achivment_update, name='achivment_update'),
    
    # UserAchivment URLs
    path('user-achivments/create/', views.user_achivment_create, name='user_achivment_create'),
    path('user-achivments/update/<int:pk>/', views.user_achivment_update, name='user_achivment_update'),
    
    # Order URLs
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/update/<int:pk>/', views.order_update, name='order_update'),
]