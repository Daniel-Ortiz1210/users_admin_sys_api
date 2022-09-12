from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, isStaffUserSerializer
from .permissions import isAdminOrReadOnly, BasicPermissions
from rest_framework.permissions import IsAuthenticated
from .models import User
import datetime
from django.shortcuts import get_object_or_404
from .utils import DataValidationSuite

'''
Para entender la permisología de los usuarios, recomiendo analizar las clases isAdminOrReadOnly y BasicPermissions

Los usuarios de tipo "is_superuser" pueden: crear, actualizar, consultar y eliminar usuarios.
Los usuarios de tipo "is_staff" pueden actualizar y consultar datos de usuarios.
Usuarios que no tengan ninguna de estás dos propiedades, solo pueden consultar información.

Siempre al crear o modificar un usuario, vamos a validar campos como cp, curp, rfc, telefono y fecha con las funciones que encontraremos en el archivo utils.

La autenticación es a través de JWT, se puede observar en el archivo settings.py y en api/urls.py 
'''


class UsersView(APIView):
    permission_classes = [isAdminOrReadOnly]

    def post(self, request):

        validation = DataValidationSuite(request.data).execute_validation()

        for validation_case in validation:
            if type(validation_case) == Response:
                return validation_case

        if 'date' in request.data: 
            request.data['date'] = datetime.datetime.strptime(request.data['date'], "%d-%m-%Y").date()

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        q = User.objects.all()
        serializer = UserSerializer(q, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):

    permission_classes = [BasicPermissions]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
            
        validation = DataValidationSuite(request.data).execute_validation()

        for validation_case in validation:
            if type(validation_case) == Response:
                return validation_case
        
        if 'date' in request.data: 
            request.data['date'] = datetime.datetime.strptime(request.data['date'], "%d-%m-%Y").date()

        serializer = UserSerializer(user,request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        user = get_object_or_404(User, id=id)

        validation = DataValidationSuite(request.data).execute_validation()

        for validation_case in validation:
            if type(validation_case) == Response:
                return validation_case

        if 'date' in request.data: 
            request.data['date'] = datetime.datetime.strptime(request.data['date'], "%d-%m-%Y").date()
        
        serializer = UserSerializer(user,request.data,partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response(status=status.HTTP_200_OK)


