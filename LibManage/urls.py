from django.contrib import admin
from django.urls import path
from Home.views import *
from django.conf.urls.static import static
from django.conf import settings
from Home.views import * 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage, name="landing_page"),
    path("comicbooks/", book_page, name="book_pages"),
    path("storybooks/", story_books, name="story_books"),
    path("historybooks/", history_books, name="history_books"),
    # path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('add-to-cart/<str:model_name>/<int:id>/',add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'), 
    # path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('remove-from-cart/<str:key>/',remove_from_cart, name='remove_from_cart'),
    path('about/', about_page, name="about"),
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", logout_page, name="logout"),
    path('suggestions/',search_suggestions, name='search'),
    path('get_book_details/', get_book_details, name='get_book_details'),
    path('send-bill/', send_bill_email, name='send_bill_email'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
