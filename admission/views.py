from itertools import count
from re import template
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from .models import *
from .forms import *

# Create your views here.
class AdminHome(View):
    template_name = 'admission/admin_home.html'

    def get(self, request):
        current_session = get_current_session()

        sessions = Session.objects.all().order_by('id')
        session = Session.objects.filter(Q(status__iexact='active'))
        return render(request, self.template_name, {'session': session, 'sessions': sessions, 'current_session': current_session})

    def post(self, request):
        context = {}
        session = request.POST.get('session')
        status = request.POST.get('status')

        if status == 'close':
            Session.objects.filter(session=session).update(status='not active')
            context['message'] = 'Successfully close !'
            context['status'] = 'Close'
        elif status == 'open':
            Session.objects.filter(session=session).update(status='active')
            context['message'] = 'Successfully open !'
            context['status'] = 'Open'
        elif status == 'current_session':
            print(session)
            Session.objects.all().update(current_session=0)
            Session.objects.filter(session=session).update(current_session=1)
            context['message'] = 'Current Session Successfully set up !'
            context['status'] = 'Current Session'
        return JsonResponse(context)

class HomeView(View):
    template_name = 'admission/home.html'
    
    def get(self, request):
        current_session = get_current_session()
        session = Session.objects.filter(Q(status__iexact='active'))
        return render(request, self.template_name, {'session': session, 'current_session': current_session})

@method_decorator(login_required, name="dispatch")
class CreateSession(View):
    template_name = 'admission/create_session.html'

    def get(self, request):
        session = SessionForm()
        sessions = Session.objects.all()
        return render(request, self.template_name, {'form': session, 'sessions': sessions})

    def post(self, request):
        session_data = SessionForm(request.POST)
        if session_data.is_valid():
            Session.objects.filter(status='active').update(status='not active')
            session = session_data.save(commit=False)
            session.save()
            return redirect('create_session')
        return render(request, self.template_name, {'form': session_data})

# @transaction.atomic
class ApplyForAdmissionView(View):
    template_name = 'admission/apply.html'
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    def get(self, request):
        applicant = ApplicantForm()
        sponsor = SponsorForm()
        nextofkin = NextOfKinForm()
        
        return render(request, self.template_name, {'applicant': applicant, 'sponsor': sponsor, 'nextofkin': nextofkin})

    def post(self, request):

        applicant = ApplicantForm(request.POST)
        sponsor = SponsorForm(request.POST)
        nextofkin = NextOfKinForm(request.POST)

        if all([applicant.is_valid(), sponsor.is_valid(), nextofkin.is_valid()]):
            #Save Applicant
            applicant_data = applicant.save(commit=False)
            applicant_data.sessions = get_current_session()
            applicant_data.save()
            applicant_id = applicant_data.id

            #Save Sponsor
            sponsor_data = sponsor.save(commit=False)
            sponsor_data.applicant_id = applicant_data.id
            sponsor_data.save()

            #Save Next of Kin
            nextofkin_data = nextofkin.save(commit=False)
            nextofkin_data.applicant_id = applicant_id
            nextofkin_data.save()

            messages.success(request, 'Your application has successfully submitted')
            return redirect('apply')
        else:
            return render(request, self.template_name, {'applicant': applicant, 'sponsor': sponsor, 'nextofkin': nextofkin})


class ViewApplicantView(View):
    template_name = 'admission/applicant_list.html'

    def get(self, request):
        current_session = get_current_session()
        applicant = Applicant.objects.filter(sessions=current_session)
        return render(request, self.template_name, {'applicants': applicant})


def admitReject(request):
    # if request.method == 'POST':
    session = Session.objects.filter(Q(status='active')).first()
  
    search = request.GET['search']
    applicant = Applicant.objects.filter(Q(id=search)).first()
    student = Admission.objects.filter(applicant_id=search).first()
   
    if not student:
        admit = Admission.objects.create(
            applicant_id = applicant.id,
            admitted = True,
            session_id = session.id
        )
        admit.save()
        return JsonResponse('admitted', safe=False)
    return JsonResponse('not admitted', safe=False)

class AdmissionList(ListView):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    # model = Admission
    # context_object_name = 'students'
    # template_name = 'admission/admission_list.html'
    # ordering = 'id'
    # paginate_by = 10

    # def get_queryset(self, *args, **kwargs):
    #     return Admission.objects.filter(Q(session=self.kwargs.get('2022/2023')))
    def get(self, request):
        current_session = get_current_session()
        session = Session.objects.filter(session=current_session).first()
        session = session.id
        admission = Admission.objects.filter(session=session)
        return render(request, 'admission/admission_list.html', {'students': admission})

def downloadAdmission1(request, pk):
    admission = Admission.objects.all()
    return render(request, 'admission/admission.html', {'students': admission})

class CheckAdmission(View):
    template_name = 'admission/check_admission.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {}
        search = request.POST.get('search')
        data = Applicant.objects.filter(Q(phone_number__iexact=search) | Q(email_address__iexact=search)).first()
        if data:
            pk = data.id
            admission = Admission.objects.filter(applicant=pk).first()
            if admission:
                context['pk'] = int(admission.id)
                context['admitted'] = str(admission.admitted)
                context['session'] = str(admission.session)
                context['admission'] = "admit"
                return render(request, 'admission/adm_down_btn.html', context)
            context['admission'] = "not admit"
            return render(request, 'admission/adm_down_btn.html', context)
        context['admission'] = "not apply"
        return render(request, 'admission/adm_down_btn.html', context)

class LoadAllAdmitted(View):
    template_name = 'admission/students.html'    
    
    def get(self, request):
        data = request.GET.get('search')
        if data == 'admission':
            students = Admission.objects.all()
        else:
            students = Applicant.objects.all()
        return render(request, self.template_name, {'students': students})


from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

def downloadAdmission(request, pk):

    # queryset
    admission = Admission.objects.filter(Q(id=pk)).first()
    num = admission.id
    
    admission_num = admission_number(num)

    # context passed in the template
    context = {'admission': admission, 'admission_number': admission_num}
    

    # render
    html_string = render_to_string(
        'admission/admission.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    filename = admission.applicant.get_fullname() + ' ' + admission.applicant.class_room
    
    # http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = f'inline; filename={filename}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        # output = open(output.name, 'r')
        response.write(output.read())

    return response

def admission_number(num):
    count = 0
    value = num
    while(value>0):
        count += 1
        value = value // 10 
    if count == 1:
        add_num = f'000{num}'
    elif count == 2:
        add_num = f'00{num}'
    elif count == 3:
        add_num = f'0{num}'
    else:
        add_num = f'{num}'

    return add_num

def get_current_session():
    session = Session.objects.filter(Q(current_session=1)).first()
    if session:
        current_session = session.session
        return current_session
    return None

    
def test_toggler(request):
    return render(request, 'admission/test_toggle.html')