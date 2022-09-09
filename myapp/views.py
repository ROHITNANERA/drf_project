from datetime import datetime
from rest_framework.serializers import ValidationError
from django.http import HttpResponse
from .models import Doctor, Hospital, Patient, Review
from .serializers import Hospital_serializer, Patient_serializer,DoctorSerializer, RegisterSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.conf import settings
from django.db.models.signals import post_save,post_delete
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from myapp.pagination import MyPagination


#to create the token automatically whenever user is created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def get_time(request):
    time = datetime.now().strftime("%I:%M:%S:%f")
    day = datetime.now().strftime("%A")
    date = datetime.now().strftime("%d %B %Y")
    # ctime= datetime.now().strftime("")
    data = f"""
    <table border='1px'>
        <tr>
            <td>Date</td><td>{date}</td>
        </tr>
        <tr>
            <td>Day</td><td> {day}</td>
        </tr>
        <tr>
            <td>Time<td>{time}</td>
        </tr>
    </table>"""
    return HttpResponse(data)



class AllPatients(generics.ListCreateAPIView):
    # permission_classes=[IsAuthenticatedOrReadOnly]
    queryset=Patient.objects.all()
    serializer_class = Patient_serializer
    pagination_class = MyPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['doctor__id','alive']

class PatientViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
#other viewsets are viewsets.ViewSet, and viewsets.ReadOnlyViewset
    queryset = Patient.objects.all()
    serializer_class = Patient_serializer


class ReviewViewset(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        # pk = self.kwargs.get('pk')
        pk = serializer.validated_data['hospital'].id
        hos=Hospital.objects.get(id=pk)
        rating = hos.h_rating
        count = hos.h_rcount

        creator  = self.request.user
        review_queryset = Review.objects.filter(hospital = hos,r_creator = creator.id)
        if review_queryset.exists():
            raise ValidationError("You reviewed that hospital already!")
        sumofallratings = rating*count
        count = count+1
        total = sumofallratings+serializer.validated_data['stars']
        hos.h_rating = total/count
        hos.h_rcount=count
        serializer.validated_data['r_creator'] = creator
        hos.save()
        serializer.save()
        return Response(serializer.data)

#to get the patient list  of specific doctors only.
class DoctorsPatients(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    # queryset=Patient.objects.all()
    serializer_class = Patient_serializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Patient.objects.filter(doctor=pk)

class Patient_data(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Patient.objects.all()
    serializer_class = Patient_serializer

class AllHospitals(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Hospital.objects.all()
    serializer_class = Hospital_serializer

class HospitalDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Hospital.objects.all()
    serializer_class=Hospital_serializer


class DoctorList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    # queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    def get_queryset(self):
        #to get the list of doctors which registered by the current user only.
        return Doctor.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DoctorDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



@api_view(['POST'])
def resiter_user(request):
    if request.method == 'POST':
        serialized = RegisterSerializer(data=request.data)
        data={}
        if serialized.is_valid():
            userid=serialized.save()
            # token = Token.objects.get(user=userid).key
            
            token = RefreshToken.for_user(userid)

            tokendata= {
                'refresh': str(token),
                'access': str(token.access_token),}
            data['username'] = userid.username
            data['email'] = userid.email
            data['token'] = tokendata
            return Response(data)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE'])
def user_logout(request):
    if request.method == 'DELETE':
        #delete the token to logout.
        request.user.auth_token.delete()
        return Response(data={"Message":"User loggedout successfully"},status=status.HTTP_200_OK)




# class AllHospitals(APIView):
#     serializer_class = Hospital_serializer
#     def get(self,request):
#         hospitals = Hospital.objects.all()
#         Serialized = Hospital_serializer(hospitals,many=True)
#         return Response(Serialized.data)
#     def post(self,request):
#         serialized = Hospital_serializer(request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data,status=status.HTTP_202_ACCEPTED)
#         return Response({"Message":"data is partial or request is not formatted properly"},status=status.HTTP_400_BAD_REQUEST)

# class HospitalDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = Hospital_serializer
#     def retrieve(self,request,pk):
#         queryset = Hospital.objects.get(pk=pk)
#         serialized = Hospital_serializer(queryset)
#         return Response(serialized.data)
#     def update(self,request,pk):
#         queryset = Hospital.objects.get(pk=pk)
#         serialized = Hospital_serializer(queryset,data=request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data,status = status.HTTP_202_ACCEPTED)
#         return Response({"Message":"Data is not valid!"},status = status.HTTP_400_BAD_REQUEST)
#     def delete(self, request,pk):
#         queryset = Hospital.objects.get(pk=pk)
#         queryset.delete()
#         return Response({"Message":"Data deleted successfully"},status = status.HTTP_204_NO_CONTENT)
