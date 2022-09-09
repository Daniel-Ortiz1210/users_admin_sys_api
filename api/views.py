from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import validate_curp, validate_rfc, validate_cp, validate_telephone, validate_date
from .serializers import UserSerializer, isStaffUserSerializer
from .permissions import isAdminOrReadOnly, BasicPermissions
from rest_framework.permissions import IsAuthenticated
from .models import User
import datetime
from django.shortcuts import get_object_or_404

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
        curp = request.data['curp'] 
        cp = request.data['cp'] 
        rfc = request.data['rfc']
        telephone = request.data['telephone']
        date = request.data['date']
        
        if not validate_curp(curp):
            return Response(data={'dato_invalido':'curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not validate_rfc(rfc):
            return Response(data={'dato_invalido':'rfc ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not validate_cp(cp):
            return Response(data={'dato_invalido':'cp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not validate_telephone(telephone):
            return Response(data={'dato_invalido':'curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if not validate_date(date):
            return Response(data={'dato_invalido':'date ingresado no respeta el formato oficial. El formato correto es "dd-mm-yyy"'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        request.data['date'] = datetime.datetime.strptime(date, "%d-%m-%Y").date()

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
        if request.user.is_superuser:
            user = get_object_or_404(User, id=id)

            if 'date' in request.data:
                if not validate_date(request.data['date']):
                    return Response(data={'dato_invalido':'date ingresado no respeta el formato oficial. El formato correto es "dd-mm-yyy"'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                request.data['date'] = datetime.datetime.strptime(request.data['date'], "%d-%m-%Y").date()
            
            if 'curp' in request.data:
                if not validate_curp(request.data['curp']):
                    return Response(data={'dato_invalido':'curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if 'rfc' in request.data:
                if not validate_rfc(request.data['rfc']):
                    return Response(data={'dato_invalido':'rfc ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if 'telephone' in request.data:
                if not validate_telephone(request.data['telephone']):
                    return Response(data={'dato_invalido':'curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if 'cp' in request.data:
                if not validate_cp(request.data['cp']):
                    return Response(data={'dato_invalido':'cp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = UserSerializer(user,request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = get_object_or_404(User, id=id)
            serializer = isStaffUserSerializer(user, request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        if request.user.is_superuser:
            user = get_object_or_404(User, id=id)
            
            if 'date' in request.data:
                if not validate_date(request.data['date']):
                    return Response(data={'dato_invalido':'date ingresado no respeta el formato oficial. El formato correto es "dd-mm-yyy"'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                request.data['date'] = datetime.datetime.strptime(request.data['date'], "%d-%m-%Y").date()
            
            if 'curp' in request.data:
                if not validate_curp(request.data['curp']):
                    return Response(data={'dato_invalido':'curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if 'rfc' in request.data:
                if not validate_rfc(request.data['rfc']):
                    return Response(data={'dato_invalido':'rfc ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if 'telephone' in request.data:
                if not validate_telephone(request.data['telephone']):
                    return Response(data={'dato_invalido':'curp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if 'cp' in request.data:
                if not validate_cp(request.data['cp']):
                    return Response(data={'dato_invalido':'cp ingresado no respeta el formato oficial'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = UserSerializer(user,request.data,partial=True)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = get_object_or_404(User, id=id)
            serializer = isStaffUserSerializer(user, request.data, partial=True)
            if serializer.is_valid():
                serializer.save(raise_exception=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response(status=status.HTTP_200_OK)


