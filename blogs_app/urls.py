from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns=[
             path('', views.home,name='home'),
             path('post/', views.all_posts ,name='all_posts'),
             path('signup/' ,views.signup_function ,name='signup'),
             path('login/', auth_view.LoginView.as_view(template_name='login.html') ,name='login'),
             path('logout',auth_view.LogoutView.as_view(template_name='logout.html'),name='logout'),
             path('writepost/', views.write_post ,name='writepost'),
             path('author_all_post/<str:author>',views.author_all_posts ,name='author_all_post'),
             path('post_detail/<slug:slugs>',views.post_detail ,name='post_detail'),
             path('search/',views.search ,name='search'),
             path('category/<str:category>', views.category ,name='category'),
             path('archive/<slug:month_years>', views.archive ,name='archive'),



]   