from urllib import request
from django.shortcuts import render
from kavenegar import *
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from .models import User, PhoneOTP
from .serializers import CreateUserSerializer,LoginUserSerializer,UserSerializer
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login




class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None :
            user.first_login = True
            user.save()
            
        elif user.first_login:
            user.first_login = False
            user.save()
            
        login(request, user)
        return super().post(request, format=None)



class UserAPI(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user





class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
            })







class ValidateOTPRegister(APIView):
   

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    otp = old.otp
                    if str(otp) == str(otp_sent):
                        old.logged = True
                        old.save()
                        if old.logged:
                            Temp_data = {'phone': phone, 'password': otp_sent }

                            serializer = CreateUserSerializer(data=Temp_data)
                            serializer.is_valid(raise_exception=True)
                            user = serializer.save()
                            user.save()

                            old.delete()
                            return Response({
                                'status' : True, 
                                'detail' : 'Congrts, user has been created successfully.'
                            })
                        else:
                            return Response({
                                'status': False,
                                'detail': 'Your otp was not verified earlier. Please go back and verify otp'
                            })

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password'
                    })
                else:
                    return Response({
                       
                            'status': False,
                            'detail': ' Please go back and verify phone first'

                    })
      

        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not recieved in Post request'
            })




def send_otp(phone):
    if phone:
        key= random.randint(1000, 9999)
        phone = str(phone)
        otp = str(key)
    
        return otp
    else:
        return False



        