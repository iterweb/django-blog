from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView

from .views import *


urlpatterns = [
    path('category/<str:slug>/', GetCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostTag.as_view(), name='tag'),
    path('edit/', UserEdit.as_view(), name='edit'),
    path('user/<int:pk>/', UserProfileDetail.as_view(), name='user_profile'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('access_denied/', access_denied, name='access_denied'),
    path('password/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='reset_done'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('', HomePage.as_view(), name='home'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post'),
    path('like/<str:slug>/', like_view, name='like_post'),
    path('comment/<int:pk>/update/', UpdateComment.as_view(), name="update_comment"),
    path('comment/<int:pk>/', AddComment.as_view(), name="add_comment"),
    path('search/', SearchView.as_view(), name='search'),
    path('add/', CreatePostView.as_view(), name='add_post'),

]
