from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from django.contrib.auth.models import User
# Para usar el toke, primero se debe hacer una migracion

class RegisterApi(APIView):
    
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
            
        serializer.save()
        
        return Response({
            "status": True,
            "message": 'Succes'
        }, status = status.HTTP_201_CREATED)

# Create your views here.

# Creo la api view para el login
@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message': 'Succes'})
    
    return Response(serializer.errors)

# Hago una clase que herede de la APIView. Dentro de esta clase hago todo el CRUD y no necesito hacerlo todo por separado como hice mas abajo

class PersonAPI(APIView):
    
    def get(self, request):
        objs = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def put(self, request):
        return Response({'Message': 'put Mehot'})
    
    def patch(self, request):
        return Response({'Message': 'patch Mehot'})
    
    def delete(self, request):
        return Response({'Message': 'delete Mehot'})
    
    

@api_view(['GET', 'POST'])
def index(request):
    courses = {
        'course_name' : 'Python',
        'learn' : ['flask', 'Django', 'Tornado', 'FastApi'],
        'course_provider' : 'Scaler'
    }
    
    if request.method == 'GET':
        # Para obtener de la query string:
        name = request.GET.get('name')
        print('This is a GET')
        print(name)
        return Response(courses)
    elif request.method == 'POST':
        datos = request.data
        print(datos['age'])
        print('This is a POST')
        return Response(courses)

# Creo el CRUD para crear personas
# Ejemplo de view y urls por body. Ver urls.py
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        try:
            obj = Person.objects.get(id = request.data['id'])
        except Person.DoesNotExist:
            return Response({"error: Person not found"})
        data = request.data
        serializer = PeopleSerializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        try:
            obj = Person.objects.get(id = request.data['id'])
        except Person.DoesNotExist:
            return Response({"error: Person not found"})
        data = request.data
        serializer = PeopleSerializer(data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        
        return Response({'Message': 'Person delete'})

#Ejemplo de como hacer un endpoint y view por parametro. ver urls.py
@api_view(['GET'])
def personId(request, id=None):
    
    
        objs = Person.objects.get(pk=id)
        serializer = PeopleSerializer(objs)
        return Response(serializer.data)
    
    
# Ahora usamos el model viewset
class PeopleVieSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()
    
    # Le agrego un metodo de busqueda
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)
            
            serializer = PeopleSerializer(queryset, many=True)
            return Response({'status' : 200, 'data' : serializer.data})
    
