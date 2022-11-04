from django.urls import path
from .views import *

urlpatterns = [
    # Admin Urls
    path('admin-admission/', AdminHome.as_view(), name='admin'),
    path('admin/session/create/', CreateSession.as_view(), name='create_session'),
    path('admin/view/applicant/', ViewApplicantView.as_view(), name='applicantView'),
    path('admin/admit/', admitReject, name='admit'),
    path('admin/admission/list/', AdmissionList.as_view(), name='admissionlist'),
    path('admin/ajax/load-all-admission', LoadAllAdmitted.as_view(), name='load_all'),
    path('admission/<int:pk>/download/', downloadAdmission, name='download'),
    
    # Applicant Urls
    path('', HomeView.as_view(), name='home'),
    path('applicant/apply/', ApplyForAdmissionView.as_view(), name='apply'),
    path('applicant/check-admission/', CheckAdmission.as_view(), name='check_admission'),
    

    path('test_toggler', test_toggler, name='test_toggler'),
]