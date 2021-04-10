import logging
import requests
import io
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView

from users.forms import UserProfileForm
from users.models import *

from golab.decorators import patient_login_required
from users.mixins import PatientLoginRequiredMixin
from .acuity.appointments import Appointments
from .filtersets import TestResultFilterSet
from .models import *
from .forms import *
from .admin import CustomTestModelForm
from django.http import HttpResponse
from django.http import Http404

import io as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
import PyPDF2
import os
from dawn_sun_23197.settings import STATIC_ROOT
from django.contrib.staticfiles import finders
from django.urls import reverse
from reports.patients.utils import get_form_value

logger = logging.getLogger(__name__)


def golab_index(request):
    data = {
        'title': 'Golab Home'
    }
    return render(request, 'golab/index.html', data)


@login_required()
def patient_dashboard(request):
    data = {
        'title': 'Dashboard'
    }
    return render(request, 'golab/patient/dashboard.html', data)


class PatientDashboardIndex(PatientLoginRequiredMixin, TemplateView):
    template_name = 'golab/patient/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(PatientDashboardIndex, self).get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        return context


# class CreateAppointment(PatientLoginRequiredMixin, CreateView):
#     model = AcuityAppointment
#     form_class = AcuityAppointmentCreateForm
#     template_name = 'golab/patient/appointments/create.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(CreateAppointment, self).get_context_data(**kwargs)
#         context['title'] = "Create New Appointment"
#         return context

class SelectAppointmentList(View):
    model = AcuityAppointment
    form_class = AcuityAppointmentCreateForm
    template_name = 'golab/patient/appointments/create.html'

    @staticmethod
    def get(request, *args, **kwargs):
        object_list = Appointments.appointment_types()
        data = {
            'title': 'Select Appointment Type',
            'types': object_list
        }
        return render(request, 'golab/patient/appointments/select_type.html', data)

    # def get_context_data(self, **kwargs):
    #     context = super(SelectAppointmentList, self).get_context_data(**kwargs)
    #     context['title'] = "Create New Appointment"
    #     return context


class TestResults(PatientLoginRequiredMixin, FilterView):
    model = Test
    paginate_by = 10
    template_name = 'golab/patient/medtests/index.html'
    filterset_class = TestResultFilterSet

    def get_queryset(self):
        queryset = super(TestResults, self).get_queryset()
        queryset = queryset.filter(acuity_appointment__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Test Results | GoLab'
        context['now'] = timezone.now()
        return context


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


# @login_required
def test_result_download(request, id):
    try:
        test_data = Test.objects.get(pk=id)
    except Test.DoesNotExist:
        raise Http404("Test Does Not Exist")
    if not ((request.user.is_superuser or request.user.is_staff) or \
            (test_data.acuity_appointment.user == request.user)):
        raise Http404("Unauthorized")
    # if not int(test_data.acuity_appointment.user.id) == int(request.user.id):
    #     raise Http404("Unauthorized")
    image_src = os.path.join(STATIC_ROOT, 'img/golab-fin-transparent-01.png')
    fidalab_signature_src = os.path.join(STATIC_ROOT, 'img/fidalab-signature.png')
    date_of_birth, gender, test_location = '', '', ''
    if test_data.acuity_appointment:
        appointment = test_data.acuity_appointment
        date_of_birth = get_form_value(appointment.appointment_data.get("forms", {}))
        gender = get_form_value(appointment.appointment_data.get("forms", {}), 8666022)
        test_location = appointment.appointment_data.get('location')
    test_type_description = None
    try:
        test_type = test_data.test_type.all().first()
        test_type_description = test_type.type_description
        sheet = test_type.fact_sheet

        if 'http' in sheet.url:
            response = requests.get(
                sheet.url.split('?')[0]).content
            pdf2File = io.BytesIO()
            pdf2File.write(response)
        else:
            pdf2File = open(sheet.url, 'rb')
        logger.warning(msg='found fact sheet')
    except Exception as e:
        logger.warning(msg=e)
        pdf2File = open('test3.pdf', 'rb')
    data = {
        "test": test_data,
        'image_src': image_src,
        'date_of_birth': date_of_birth,
        'gender': gender,
        'test_location': test_location,
        'fidalab_signature_src': fidalab_signature_src,
        'test_type_description': test_type_description
    }

    template = get_template('golab/patient/export/result-final.html')
    html = template.render(data)

    file = open('report.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()
    # Open the files that have to be merged one by one
    pdf1File = open('report.pdf', 'rb')

    # Read the files that you have opened
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

    # Create a new PdfFileWriter object which represents a blank PDF document
    pdfWriter = PyPDF2.PdfFileWriter()

    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Loop through all the pagenumbers for the second document
    for pageNum in range(pdf2Reader.numPages):
        pageObj = pdf2Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open('MergedFiles.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)

    # Close all the files - Created as well as opened
    pdfOutputFile.close()
    pdf1File.close()
    pdf2File.close()
    file = open('MergedFiles.pdf', "rb")

    pdf = file.read()
    file.close()
    # return HttpResponse(pdf, 'application/pdf')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response


@login_required
def test_result_download_test(request):
    image_src = os.path.join(STATIC_ROOT, 'img/golab-fin-transparent-01.png')
    print(image_src)
    return HttpResponse("OK")


class EditTestView(PatientLoginRequiredMixin, UpdateView):
    model = Test
    form_class = CustomTestModelForm
    template_name = "golab/patient/medtests/test.html"

    def get_context_data(self, **kwargs):
        ctx = super(EditTestView, self).get_context_data(**kwargs)
        u = Test.objects.get(pk=self.kwargs['id']).acuity_appointment.user
        uu = UserProfile.objects.filter(user=u)[0]
        mform = UserProfileForm(
            initial={'user': u, 'date_of_birth': uu.date_of_birth, 'contact_number': uu.contact_number,
                     'zip_code': uu.zip_code, 'gender': uu.gender, 'street_address': uu.street_address})
        ctx['ctx'] = {"mform": mform}
        return ctx

    def get_object(self, *args, **kwargs):
        test_data = get_object_or_404(Test, pk=self.kwargs['id'])
        return test_data

    def post(self, request, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        u = Test.objects.get(pk=self.kwargs['id']).acuity_appointment.user
        uu = UserProfile.objects.filter(user=u)
        uu.update(contact_number=request.POST['contact_number'])
        uu.update(date_of_birth=request.POST['date_of_birth'])
        uu.update(zip_code=request.POST['zip_code'])
        uu.update(gender=request.POST['gender'])
        uu.update(street_address=request.POST['street_address'])
        return super(EditTestView, self).post(request, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse("golab:test_results")
