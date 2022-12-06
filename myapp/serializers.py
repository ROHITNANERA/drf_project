from rest_framework import serializers
from .models import Doctor, Hospital, Patient, Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import datetime
import re


class DoctorSerializer(serializers.ModelSerializer):
    patient = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='patient-detail')
    # doctor = serializers.HyperlinkedRelatedField(source='hospital.h_name',many=True,read_only=True,view_name='hospital-list')
    user = serializers.StringRelatedField()
    class Meta:
        model = Doctor
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    

class Patient_serializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    class Meta:
        model = Patient
        fields = '__all__'
    def get_age(self,obj):
  
        return datetime.datetime.now().year-obj.Birthdate.year
    hospital = serializers.SerializerMethodField()
    def get_hospital(self,obj):
        return obj.doctor.hospital.h_name


    def validate(self,obj):
        if obj['alive']!=True and (datetime.datetime.now().year-obj['Birthdate'].year)>100:
            raise serializers.ValidationError("SORRY, GHOSTS ARE NOT ALLOWED...")
        else:
            return obj

    def validate_name(self,value):
        if res := re.findall("[0-9]", value):
            raise serializers.ValidationError("Name should not contain numbers!")
        return value

class Hospital_serializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
    doctor = serializers.HyperlinkedRelatedField(view_name='doctor-detail',many=True,read_only=True)
    
class RegisterSerializer(serializers.ModelSerializer):
    confirmpass = serializers.CharField(write_only=True, max_length = 100)
    class Meta:
        model = User
        fields = ['username','email','password','confirmpass']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self):
        pass1 = self.validated_data['password']
        pass2 = self.validated_data['confirmpass']

        if pass1!=pass2:
            raise serializers.ValidationError({"Error: Your password and confirm password are not same!"})
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"Error: Email is alredy Registered."})  
        newuser = User(email = self.validated_data['email'],username=self.validated_data['username'])
        newuser.set_password(pass1)
        newuser.save()
        return newuser
        