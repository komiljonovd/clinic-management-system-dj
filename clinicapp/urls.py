from django.urls import path
from clinicapp.views import (doctor_views,
                             patient_views,
                             appointment_views,
                             prescription_views,
                             laborarory_views,
                             billing_views,
                             medical_records_views

)
from .dashboard import dashboard_view

urlpatterns = [
    # doctor
    path('doctor/',doctor_views.DoctorListCreateAPI.as_view(),name='doctor-list-create'),
    path('doctor/<int:user_id>/',doctor_views.DoctorDetailAPI.as_view(),name='doctor-detail'),
    # patient
    path('patient/',patient_views.PatientListCreateAPI.as_view(),name='patient-list-create'),
    path('patient/<int:user_id>',patient_views.PatientDetailAPI.as_view(),name='patient-detail'),
    # appointments
    path('appointment/',appointment_views.AppointmentListCreateAPI.as_view(),name='appointment-list-create'),
    path('appointment/<int:pk>',appointment_views.AppointmentDetailAPI.as_view(),name='appointment-detail'),
    # prescription 
    path('prescription/',prescription_views.PrescriptionListCreateAPI.as_view(),name='prescription-list-create'),
    path('prescription/<int:pk>',prescription_views.PrescriptionDetailAPI.as_view(),name='prescription-detail'),
    # Laboratory
    path('laboratory/',laborarory_views.LaboratoryListCreateAPI.as_view(),name='laboratory-list-create'),
    path('laboratory/<int:pk>',laborarory_views.LaboratoryDetailAPI.as_view(),name='laboratory-detail'),
    # Billing
    path('billing/',billing_views.BillingListCreateAPI.as_view(),name='billing-list-create'),
    path('billing/<int:pk>',billing_views.BillingDetailAPI.as_view(),name ='billing-detail'),
    # Medical Record
    path('medical-record/',medical_records_views.MedicalRecordListCreateAPI.as_view(),name='medical-record-list-create'),
    path('medical-record/<int:pk>',medical_records_views.MedicalRecordDetailAPI.as_view(),name='medical-record-detail'),

    path('dashboard/',dashboard_view,name='dashboard-view'),
]