from ast import Delete
from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly
from accounts.models import User
from products import serializers


class ProductListView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(instance=queryset, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):

    def get(self, request, pk):
        instance = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=instance)
        return Response(serializer.data)

class ProductAddView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    def post(self, request,):
        
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'added'})
        return Response(serializer.errors)

class ProductUpdateView(APIView):
    permission_classes = [IsAuthorOrReadOnly]
    def post(self, request, pk):
        insrance = Product.objects.get(id=pk)
        serializer=ProductSerializer(instance=insrance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'updated'})
        return Response(serializer.errors)

    def delete(self, request, pk):
        instance = Product.objects.get(id=pk)
        instance.delete()
        return Response({'response': 'deleted'})