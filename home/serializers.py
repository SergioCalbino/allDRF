from rest_framework import serializers
from .models import Person, Color
import re
from django.contrib.auth.models import User

# Creo la clase para el token y autenticacion

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    # primero busco en la db si el usuario existe
    
    def validate(self, data):
        
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username Already exist")
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError("Email Already exist")
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user  # Devuelve el objeto User creado

# Serializer para el login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name', 'id']

class PeopleSerializer(serializers.ModelSerializer):
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    # Puedo usar un serializador de metadato
    color_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        # fields = ['id','name', 'age']
        fields = '__all__'
        # Este solo sirve si tienen un campo para mostar, Si son varios, ya conviene hacer un serializardor propio del color. Ver arriba
        # depth = 1
    
    # creo el metodo para el serializaoro metatado
    def get_color_info(sefl, obj):
        if obj.color is not None:
            try:
                color_obj = Color.objects.get(id = obj.color.id) 
                return {
                "id": color_obj.id,
                "color_name": color_obj.color_name,
                # otros campos que necesites
            }
            except Color.DoesNotExist:
                return None  # o manejar el error de otra manera adecuada para tu caso
        else:
            return None  # o cualquier valor por defecto que necesites
        
    # Ahora vamos a validar datos
    def validate(self, data):
        # Valido en nombre con regex
        regex = "^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        if not re.match(regex, data['name']):
            raise serializers.ValidationError('Name has a invalid character')
        
        if data['age'] < 18 :
            raise serializers.ValidationError('Age should be grater than 18')
        
        return data