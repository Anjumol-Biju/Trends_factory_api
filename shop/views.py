
    
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework import authentication,permissions
from shop.serializers import UserSerializer,ProductSerializer,BasketSerializer,BasketItemSerializer
from shop.models import Product,Size,BasketItem
# Create your views here.

class SignUpView(CreateAPIView):
    
    serializer_class=UserSerializer
    queryset=User.objects.all()
    
class ProductListView(ListAPIView):
    
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    
class ProductDetailView(RetrieveAPIView):
    
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    

class AddToCartView(APIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    
    def post(self,request,*args, **kwargs):
        
        basket_object=request.user.cart
        
        id=kwargs.get("pk")
        
        product_object=Product.objects.get(id=id)
        
        size_name=request.data.get("size")
        size_object=Size.objects.get(name=size_name)
        
        quantity=request.data.get("quantity")

        BasketItem.objects.create(
            
            basket_object=basket_object,
            product_object=product_object,
            size_object=size_object,
            quantity=quantity
        )
        return Response(data={"message":"created"})

class CartListView(APIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        qs=request.user.cart
        serializer_instance=BasketSerializer(qs)
        return Response(data=serializer_instance.data)
    
class CartItemUpdateView(UpdateAPIView,DestroyAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
      
    serializer_class=BasketItemSerializer
    
    queryset=BasketItem.objects.all()
    
    
    def perform_update(self, serializer):
        
       size_name=self.request.data.get("size_object")
       
       size_obj=Size.objects.get(name=size_name)
       
       serializer.save(size_object=size_obj)
       

    
    
      