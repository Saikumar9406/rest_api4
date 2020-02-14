from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import studentSerializer
from .models import student
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

"""!!!!!!!!!!!!!!!! AUTHENTICATION @@@@@@@@@@@@@@@@@@@@@@"""
class userauthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response(token.key)

"""$$$$$$$$$$$$$$$$$ FUNCTION BASED VIEWS @@@@@@@@@@@@@@@@@@"""

@csrf_exempt
def studentlist(request):
    if request.method == 'GET':
        students=student.objects.all()
        serializer=studentSerializer(students,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data=JSONParser().parse(request)
        serializer=studentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
@csrf_exempt
def updatestudent(request,id):
    def get_student(id):
        try:
            s=student.objects.get(id=id)
            return s
        except student.DoesNotExist:
            return HttpResponse(f'Response object has no attribute')
    if request.method == 'GET':
        st=get_student(id)
        serializer=studentSerializer(st)
        return JsonResponse(serializer.data,safe=False,status=200)
    elif request.method == 'PUT':
        st = get_student(id)
        data=JSONParser().parse(request)
        serializer=studentSerializer(st,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors,status=400)
    elif request.method == 'DELETE':
        st = get_student(id)
        st.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""@@@@@@@@@@@@@@@@@@@@@@ API DECORATOR #####################"""
@api_view(['GET','POST'])
def student_list(request):
    if request.method == 'GET':
        students=student.objects.all()
        serializer=studentSerializer(students,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        #data=JSONParser().parse(request)
        serializer=studentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET','PUT','DELETE'])
def update_student(request,id):
    def get_student(id):
        try:
            s=student.objects.get(id=id)
            return s
        except student.DoesNotExist:
            return HttpResponse(f'Response object has no attribute')
    if request.method == 'GET':
        st=get_student(id)
        serializer=studentSerializer(st)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        st = get_student(id)
        #data=JSONParser().parse(request)
        serializer=studentSerializer(st,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        st = get_student(id)
        st.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""!!!!!!!!!!!!!!!! CLASS BASED API VIEWS****************************"""

class studentapiview(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication,SessionAuthentication,TokenAuthentication]
    def get(self,request):
        queryset=student.objects.all()
        serializer=studentSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=studentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class updatestudentapiview(APIView):
    authentication_classes = [BasicAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_student(self,id):
        try:
            model=student.objects.get(id=id)
            return model
        except student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,id):
        s=self.get_student(id)
        serializer=studentSerializer(s)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,id):
        s = self.get_student(id)
        serializer = studentSerializer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        s = self.get_student(id)
        s.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""@@@@@@@@@@@@@@@ GENERIC VIEWS AND MIXINS &&&&&&&&&&&&&&"""

class studentgenericview(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = studentSerializer
    queryset = student.objects.all()
    lookup_field = 'id'
    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self,request):
        return self.create(request)
    def put(self,request,id):
        return self.update(request,id)
    def delete(self,request,id):
        return self.destroy(request,id)

"""@@@@@@@@@@@@@@@@@@ VIEWSETS AND ROUTERS ##############3"""

class studentviewset(viewsets.ViewSet):
    #lookup_fields='id'
    def list(self,request):
        model=student.objects.all()
        serializer=studentSerializer(model,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def create(self,request):
        serializer=studentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        model=student.objects.all()
        s=get_object_or_404(model,pk=pk)
        serializer=studentSerializer(s)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def update(self,request,pk=None):
        model=student.objects.get(pk=pk)
        serializer=studentSerializer(model,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk=None):
        model = student.objects.get(pk=pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""!!!!!!!!!!!!!!!!!!!!!!!!!!! GENERICVIEW SETS & MIXINS ^^^^^^^^^^^^^^^^^^^^^^^"""

class studentgenericviewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,mixins.DestroyModelMixin):
   serializer_class = studentSerializer
   queryset = student.objects.all()


class studentmodelviewset(viewsets.ModelViewSet):
    serializer_class = studentSerializer
    queryset = student.objects.all()


