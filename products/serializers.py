from rest_framework import serializers
from .models import Product

from django.contrib.auth import get_user_model
User = get_user_model()




class ProductSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Product
        fields = ('user','location','category','title','image','description',  'price', 'datetime_created', )
        
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user']=request.user
        return Product.objects.create(**validated_data)
   
