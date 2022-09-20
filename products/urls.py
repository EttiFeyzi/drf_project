from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(), name='listview'),
    path('<int:pk>/',views.ProductDetailView.as_view(), name='detailview'),
    path('add/', views.ProductAddView.as_view(), name='addview'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='updateview'),
]