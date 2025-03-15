from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('home/', views.product_list, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<int:id>/<slug:slug>/review/', views.product_review, name='product_review'),
    path('product/<int:id>/<slug:slug>/wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('category/<slug:category_slug>/products/', views.product_list, name='product_list_by_category'),
    path('review/<int:review_id>/helpful/', views.review_helpful, name='review_helpful'),
    path('review/<int:review_id>/report/', views.report_review, name='report_review'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('product/quick-view/<int:product_id>/', views.quick_view_product, name='quick_view_product'),
] 