from django.urls import path
from .views import AllHospitals, AllPatients, DoctorDetail, DoctorList,ReviewViewset, DoctorsPatients, HospitalDetail, Patient_data, PatientViewset

urlpatterns = [
    path('allpatients/', AllPatients.as_view(), name="patient-list"),
    path('patient/<int:pk>/',Patient_data.as_view(),name="patient-detail"),
    # path('onepatient/<int:pk>/',one_patient,name="one patient"),
    path("allhospitals/",AllHospitals.as_view(),name="hospital-list"),
    path('hospital_detail/<int:pk>/',HospitalDetail.as_view(),name='hospital-detail'),
    path('doctorlist/',DoctorList.as_view(),name='doctor-list'),
    path('doctordetail/<int:pk>/',DoctorDetail.as_view(),name="doctor-detail"),
    path('doctor/<int:pk>/patients/',DoctorsPatients.as_view(),name='DoctorsPatient-list'),
    path("review/",ReviewViewset.as_view(),name="create-review"),

]
