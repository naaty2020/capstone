from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('item/<int:id>', views.item, name="item"),
    path('item-json/<int:id>', views.item_json, name="item_json"),
    path('type-vendor/<str:uname>', views.type_vendor, name="type_vendor"),
    path('edit-item/<int:id>', views.edit_item, name="edit_item"),
    path('subscribtion', views.subscribe, name="subscribe"),
    path('vendors', views.vendors, name="vendors"),
    path('vendor/<int:id>', views.vendor, name="vendor"),
    path('verified/<int:ver>', views.verified, name="verified"),
    path('subscribed/<int:sub>', views.subscribed, name="subscribed"),
    path('home/<str:name>', views.vendor_home, name="vendor_home"),
    path('trending-items', views.trending_items, name="trending"),
    path('new-items', views.new_items, name="new"),
    path('all-items', views.all_items, name="all"),
    path('upcoming-items', views.upcoming_items, name="upcoming"),
    path('subscription-items', views.subscription_items, name="subscribtion"),
    path('serach_results', views.search, name="search"),
    path('edit-page/<int:id>', views.edit_page, name="edit_page"),
    path('add-item', views.add_item, name="add_item"),
    path('login', views.login_view, name="login"),
    path('vendor-login', views.vendor_login_view, name="vendor_login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('vendor-register', views.vendor_register, name="vendor_register")
]