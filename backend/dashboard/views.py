import csv
from datetime import datetime
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, TemplateView, base, ListView
from django_filters.views import FilterView

from dashboard.decorators import admin_login_required
from dashboard.mixins import AdminOnlyViewPermissionMixin, StaffViewsPermissionOnly
from golab.acuity.appointments import Appointments
from golab.acuity.clients import AcuityClients
from golab.filtersets import TestResultFilterSet

from golab.models import *
from golab.forms import *
from users.filtersets import PatientNotificationFilterSet
from users.mixins import PatientLoginRequiredMixin
from users.models import *
from django.http import JsonResponse, HttpResponse
from .serializers import *
from .utils import appointment_csv_header, get_dob
from dashboard.templatetags.custom_template_tags import getTestTypes, getTest
import json
from golab.functions import send_ready_stauts_for_test


# staff_urls_only = [
#     reverse('golab:dashboard_acuity_appointments'),
#     reverse('golab:dashboard_acuity_appointment_detail'),
#     reverse('golab:dashboard_acuity_appointment_types'),
#     reverse('golab:dashboard_acuity_appointment_addons'),
# ]


@admin_login_required
def dashboard_index(request):
    data = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard/index.html', data)


class DashboardIndex(StaffViewsPermissionOnly, View):

    def get(self, request, *args, **kwargs):
        # print(request.path)
        # print(reverse('golab:patient_dashboard'))
        # print(staff_urls_only)
        data = {
            'title': 'Dashboard'
        }
        return render(request, 'dashboard/index.html', data)

    # def get_context_data(self, **kwargs):
    #     context = super(DashboardIndex, self).get_context_data(**kwargs)
    #     context['title'] = 'Dashboard'
    #     return context


# @admin_login_required
# def appointments(request):
#     data = {
#         'title': 'Appointments',
#         'appointment_active': True,
#         'appointments': Appointments.appointment_list()
#     }
#     return render(request, 'dashboard/appointments/list.html', data)
def get_test_ids(instance):
    try:
        return [test.id for test in instance.test.test_type.all()]
    except:
        return []


def get_test(instance):
    try:
        return instance.test
    except:
        return Test()


def can_sms_notify(ids):
    queryset = AcuityAppointment.objects.filter(acuity_appointment_id__in=ids)
    return [
        {'marked': i.send_sms_notification,
         'acuity_appointment_id': i.acuity_appointment_id,
         'type_ids': get_test_ids(i),
         'test': get_test(i)
         }
        for i in queryset]


class AppointmentList(StaffViewsPermissionOnly, View):
    # permission_required = True

    @staticmethod
    def get(request, *args, **kwargs):
        params = request.GET
        # print(params)
        # users = User.objects.filter(is_patient=True)
        test_types = TestType.objects.all()
        test_statuses = Test_Status
        test_results = Results
        appointment_list = Appointments.appointment_list(params)
        appointment_data = can_sms_notify([i.get('id') for i in appointment_list])
        # ids_list = [a['id'] for a in appointment_list]
        # result_list = Test.objects.filter(acuity_appointment__acuity_appointment_id__in=ids_list).values('test_status')
        # # hhh = UserProfile.objects.filter(contact_number__in=[str(4255036246)])
        # print(result_list)
        data = {
            'title': 'Appointments',
            'appointment_active': True,
            # 'users': users,
            'test_types': test_types,
            'test_results': test_results,
            'test_statuses': test_statuses,
            'specimen_types': Specimen_types,
            'appointments': appointment_list,
            'appointment_data': appointment_data
        }
        return render(request, 'dashboard/appointments/list.html', data)


class AppointmentListCSV(StaffViewsPermissionOnly, View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        now = datetime.now()

        response['Content-Disposition'] = 'attachment; filename="appointment-report-%s.csv"' % now.timestamp()
        writer = csv.writer(response)
        # Create the HttpResponse object with the appropriate CSV header.
        writer.writerow(appointment_csv_header)
        params = request.GET

        for appointment in Appointments.appointment_list(params):
            test = getTest(appointment.get('id', None))
            row_data = [
                appointment.get('id', ''),  # Appointment id
                appointment.get('type', ''),  # Appointment Type
                appointment.get("firstName", ""),  # First Name
                appointment.get("lastName", ""),  # Last Name
                get_dob(appointment.get("forms", {})),  # Patient Date of Birth
                appointment.get('date', ''),  # Appointment date
                appointment.get('time', ''),  # Test Time
                getTestTypes(appointment.get('id')),  # Test Type
                test.test_status,  # Test Status
                test.result  # Test Results
            ]

            writer.writerow(row_data)

        return response


# class AppointmentList(StaffViewsPermissionOnly, ListView):
#     # permission_required = True
#     template_name = 'dashboard/appointments/list.html'
#     context_object_name = 'appointments'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(AppointmentList, self).get_context_data(**kwargs)
#         context['title'] = 'Appointments'
#         context['appointment_active'] = True
#         return context

# def get(self, request, *args, **kwargs):
#     params = request.GET
#     # print(params)
#     data = {
#         'title': 'Appointments',
#         'appointment_active': True,
#         'appointments': Appointments.appointment_list(params)
#     }
#     return render(request, 'dashboard/appointments/list.html', data)


# @admin_login_required
# def appointment_detail(request, appointment_id):
#     appointment = Appointments.appointment_detail(appointment_id)
#     data = {
#         'title': 'Appointment Detail',
#         'appointment': appointment
#     }
#     return render(request, 'dashboard/appointments/detail.html', data)

class AppointmentDetail(StaffViewsPermissionOnly, View):
    def get(self, request, *args, **kwargs):
        appointment = Appointments.appointment_detail(kwargs['appointment_id'])
        data = {
            'title': 'Appointment Detail',
            'appointment': appointment
        }
        return render(request, 'dashboard/appointments/detail.html', data)


class AppointmentTypes(StaffViewsPermissionOnly, View):
    def get(self, request, *args, **kwargs):
        object_list = Appointments.appointment_types()
        data = {
            'title': 'Appointment Types',
            'appointment_active': True,
            'appointment_types': object_list
        }
        return render(request, 'dashboard/appointments/types.html', data)


class AppointmentAddons(StaffViewsPermissionOnly, View):
    def get(self, request, *args, **kwargs):
        object_list = Appointments.appointment_addons()
        data = {
            'title': 'Appointment Addons',
            'appointment_active': True,
            'appointment_addons': object_list
        }
        return render(request, 'dashboard/appointments/addons.html', data)


class AcuityClientList(StaffViewsPermissionOnly, View):
    def get(self, request, *args, **kwargs):
        object_list = AcuityClients.client_list()
        data = {
            'title': 'Clients',
            'client_active': True,
            'clients': object_list
        }
        return render(request, 'dashboard/acuity/clients.html', data)


def find_appointment_type(appointment_types, id):
    res = ''
    for item in appointment_types:
        if item.get('id') == id:
            res = item.get('name', '')
            break
    return res


class BulkAddEditTestResult(StaffViewsPermissionOnly, View):
    def post(self, request, *args, **kwargs):
        appointments_post_data = json.loads(request.POST.get('appointments_checked_data'))
        appointment_types = Appointments.appointment_types()

        errors = []

        for post_data in appointments_post_data:
            result_id = post_data.get("result_id")
            acuity_appointment_id = post_data.get('acuity_appointment_id')
            appointment_data = Appointments.appointment_detail(acuity_appointment_id)
            appointment_type_id = appointment_data.get('appointmentTypeID')
            appointment_type = find_appointment_type(appointment_types, appointment_type_id)
            if post_data.get('user'):
                user_qs = User.objects.filter(pk=post_data.get('user'))
            else:
                user_qs = User.objects.filter(email=post_data.get('user_email'))
            if user_qs.exists():
                user = user_qs.first()
            else:
                errors.append({'user': 'User with id %s not found' % post_data.get('user_email')})
                continue
            try:
                appointment = AcuityAppointment.objects.get(acuity_appointment_id=acuity_appointment_id)
            except AcuityAppointment.DoesNotExist:
                appointment = AcuityAppointment(user=user,
                                                acuity_appointment_id=post_data.get('acuity_appointment_id'),
                                                appointment_type=appointment_type,
                                                appointment_data=appointment_data)
                appointment.save()

            test_types = json.loads(request.POST.get('test_type'))
            data = {
                "acuity_appointment": appointment.id,
                "collection_date": request.POST.get('collection_date'),
                "processing_date": request.POST.get('processing_date'),
                "specimen_type": request.POST.get('specimen_type'),
                "iterpretation": request.POST.get('interpretation'),
                "location": request.POST.get('location'),
                "test_status": request.POST.get('test_status'),
                "test_type": test_types,
                "result": request.POST.get('test_result'),
            }
            if result_id and result_id != 'None':
                del data['acuity_appointment']
            test_result = TestResultSerializer(data=data)
            if test_result.is_valid():
                test = None
                if result_id and result_id != 'None':
                    existing_test = Test.objects.filter(pk=result_id)
                    if existing_test.exists():
                        test = existing_test.first()
                if test is None:
                    instance = test_result.save()
                    instance.save()
                else:
                    test.collection_date = data.get('collection_date')
                    test.processing_date = data.get('processing_date')
                    test.specimen_type = data.get('specimen_type')
                    test.result = data.get('result')
                    test.iterpretation = data.get('iterpretation')
                    test.location = data.get('location')
                    test.test_status = data.get('test_status')
                    test.test_type.set(test_types)
                    test.save()
            else:
                errors.append(test_result.errors)

        response_data = {
            'success': True if len(errors) == 0 else False,
            'message': 'Success' if len(errors) == 0 else errors,
            'errors': errors
        }
        return JsonResponse(response_data)


class AddEditTestResult(StaffViewsPermissionOnly, View):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.POST)
        result_id = request.POST.get("result_id")
        acuity_appointment_id = request.POST.get('acuity_appointment_id')
        appointment_types = Appointments.appointment_types()
        appointment_type = ''

        appointment_data = Appointments.appointment_detail(acuity_appointment_id)
        appointment_type_id = appointment_data.get('appointmentTypeID')

        for item in appointment_types:
            if item.get('id') == appointment_type_id:
                appointment_type = item.get('name', '')
                break

        if result_id == 'None':
            try:
                if request.POST.get('user'):
                    user = User.objects.get(pk=request.POST.get('user'))
                else:
                    user = User.objects.filter(email=request.POST.get('user_email')).first()
            except User.DoesNotExist:
                response_data = {
                    'success': False,
                    "message": {'user': ["Inalid User"]}
                }
                return JsonResponse(response_data)

            try:
                appointment = AcuityAppointment.objects.get(acuity_appointment_id=acuity_appointment_id)
            except AcuityAppointment.DoesNotExist:
                appointment = AcuityAppointment(user=user,
                                                acuity_appointment_id=request.POST.get('acuity_appointment_id'),
                                                appointment_type=appointment_type,
                                                appointment_data=appointment_data)
                appointment.save()
            test_types = json.loads(request.POST.get('test_type'))
            data = {"acuity_appointment": appointment.id, "collection_date": request.POST.get('collection_date'),
                    "processing_date": request.POST.get('processing_date'),
                    "specimen_type": request.POST.get('specimen_type'), "result": request.POST.get('test_result'),
                    "iterpretation": request.POST.get('interpretation'), "location": request.POST.get('location'),
                    "test_status": request.POST.get('test_status'), "test_type": test_types}
            test_result = TestResultSerializer(data=data)
            if test_result.is_valid():
                instance = test_result.save()
                response_data = {
                    'success': True,
                    "message": "Created"
                }
                return JsonResponse(response_data)
            response_data = {
                'success': False,
                'message': test_result.errors
            }
            return JsonResponse(response_data)
        else:
            try:
                existing_test = Test.objects.get(pk=result_id)
            except Test.DoesNotExist:
                response_data = {
                    'success': False,
                    "message": {'test': ["Inalid Result Id Provided"]}
                }
                return JsonResponse(response_data)
            try:
                user = User.objects.get(pk=request.POST.get('user'))
            except User.DoesNotExist:
                response_data = {
                    'success': False,
                    "message": {'user': ["Inalid User"]}
                }
                return JsonResponse(response_data)

            try:
                appointment = AcuityAppointment.objects.get(acuity_appointment_id=acuity_appointment_id)
            except AcuityAppointment.DoesNotExist:
                appointment = AcuityAppointment(user=user,
                                                acuity_appointment_id=request.POST.get('acuity_appointment_id'),
                                                appointment_type=appointment_type,
                                                appointment_data=appointment_data)
                appointment.save()
            test_types = json.loads(request.POST.get('test_type'))
            data = {"collection_date": request.POST.get('collection_date'),
                    "processing_date": request.POST.get('processing_date'),
                    "specimen_type": request.POST.get('specimen_type'), "result": request.POST.get('test_result'),
                    "iterpretation": request.POST.get('interpretation'), "location": request.POST.get('location'),
                    "test_status": request.POST.get('test_status'), "test_type": test_types}
            test_result = TestResultSerializer(data=data)
            if test_result.is_valid():
                existing_test.collection_date = request.POST.get('collection_date')
                existing_test.processing_date = request.POST.get('processing_date')
                existing_test.specimen_type = request.POST.get('specimen_type')
                existing_test.result = request.POST.get('test_result')
                existing_test.iterpretation = request.POST.get('interpretation')
                existing_test.location = request.POST.get('location')
                existing_test.test_status = request.POST.get('test_status')
                existing_test.test_type.set(test_types)
                existing_test.save()
                response_data = {
                    'success': True,
                }
                return JsonResponse(response_data)
        response_data = {
            'success': False,
            "message": test_result.errors
        }
        return JsonResponse(response_data)


class ToggleNotify(StaffViewsPermissionOnly, View):
    def post(self, request, *args, **kwargs):
        acuity_appointment_id = request.POST.get('acuity_appointment_id')
        send_sms_notification = request.POST.get('send_sms_notification')
        if send_sms_notification == '1':
            send_sms_notification = True
        else:
            send_sms_notification = False
        try:
            appointment = AcuityAppointment.objects.get(acuity_appointment_id=acuity_appointment_id)
            appointment.send_sms_notification = send_sms_notification
            appointment.save()
            success = True
            message = "Data is saved"
        except AcuityAppointment.DoesNotExist:
            # No need to create, becuase we can't create until user is not defined.
            success = False
            message = "Appointment User is not set in our record. unable to save"
        responseData = {
            'success': success,
            'message': message
        }
        return JsonResponse(responseData)


class BulkNotifyPatient(StaffViewsPermissionOnly, View):
    def post(self, request, *args, **kwargs):
        appointments_post_data = json.loads(request.POST.get('appointments_checked_data'))
        try:
            for post_data in appointments_post_data:
                result_id = post_data.get("result_id")
                if result_id == 'None':
                    continue  # only send notification for acuity appointments with test result
                test_qs = Test.objects.filter(pk=result_id)
                if test_qs.exists():
                    test = test_qs.first()
                else:
                    continue
                if test.test_status == 'ready':
                    send_ready_stauts_for_test(test)
            response_data = {
                'success': True,
                "message": {'notify': ["Notified User"]}
            }
        except Test.DoesNotExist:
            response_data = {
                'success': False,
                "message": {'notify': ["Unable to notify user invalid test"]}
            }
        return JsonResponse(response_data)


class NotifyPatient(StaffViewsPermissionOnly, View):
    def post(self, request, *args, **kwargs):
        result_id = request.POST.get("result_id")
        try:
            test = Test.objects.get(pk=result_id)
            if test.test_status == 'ready':
                send_ready_stauts_for_test(test)
            responseData = {
                'success': True,
                "message": {'notify': ["Notified User"]}
            }
        except Test.DoesNotExist:
            responseData = {
                'success': False,
                "message": {'notify': ["Unable to notify user invalid test"]}
            }
        return JsonResponse(responseData)


# notification list
class PatientNotificationList(StaffViewsPermissionOnly, FilterView):
    model = PatientNotification
    queryset = PatientNotification.objects.all().order_by('-updated')
    context_object_name = 'notifications'
    template_name = 'dashboard/patient/notification_list.html'
    paginate_by = 25
    filterset_class = PatientNotificationFilterSet

    # filterset_fields = ['user__first_name__icontains', 'user__last_name', 'user__email', 'created', 'updated']

    def get_queryset(self):
        return PatientNotification.objects.select_related('user', 'acuity_appointment', 'acuity_appointment__test') \
            .prefetch_related('user', 'acuity_appointment', 'acuity_appointment__test').all().order_by('-created')

    def get_context_data(self, *args, **kwargs):
        ctx = super(PatientNotificationList, self).get_context_data(*args, **kwargs)
        ctx['title'] = 'Patient Notifications'
        return ctx


class AppointmentTestResults(StaffViewsPermissionOnly, FilterView):
    model = Test
    paginate_by = 10
    template_name = 'dashboard/test/results.html'
    filterset_class = TestResultFilterSet

    def get_queryset(self):
        queryset = super(AppointmentTestResults, self).get_queryset()
        queryset = queryset.prefetch_related('acuity_appointment', 'acuity_appointment__user')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Test Results | GoLab'
        context['now'] = timezone.now()
        return context
