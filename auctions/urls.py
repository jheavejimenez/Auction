from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("productDetail/<int:id>/", views.productDetail, name="productDetail"),
    path("productDetail/<int:id>/bid", views.take_bid, name="take_bid"),
    path("productDetail/<int:id>/close", views.close_listing, name="close_listing"),
    path("productDetail/<int:id>/add_comment/", views.add_comment, name="add_comment"),
    path("getProductCategory/<str:item_category>",
         views.getProductCategory, name="getProductCategory"),
    path("login", views.login_view, name="login"),
    path("login", auth_views.LoginView.as_view()),
    path("createList", views.createList, name="createList"),
    path("watchlist_add/<int:product_id>/",
         views.watchlist_add, name="watchlist_add"),
    path("get_watchlist", views.get_watchlist, name="get_watchlist"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")



]
