import json

from allauth.account.utils import setup_user_email
from allauth.utils import generate_unique_username
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.api.v1.permissions import StaffPermissionForAppointment
from golab.acuity.appointments import Appointments
from golab.models import AcuityAppointment
from users.models import UserProfile

User = get_user_model()


class AcuityAppointmentDetail(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [StaffPermissionForAppointment]

    @staticmethod
    def get(request, *args, **kwargs):
        appointment_id = kwargs['appointment_id']

        try:
            appointment = Appointments.appointment_detail(appointment_id)

            return Response(appointment)
        except:
            return Response({'message': 'Appointment not found'}, status=404)

    @staticmethod
    def post(request, *args, **kwargs):
        appointment_id = kwargs['appointment_id']
        # print(request.data)
        json_data = json.dumps(request.data)
        # print(json_data)
        try:
            appointment = Appointments.appointment_update(appointment_id, json_data)
            print(appointment)
            status_code = 200
            if 'status_code' in appointment:
                status_code = appointment['status_code']
            return Response(appointment, status=status_code)
        except:
            return Response({
                'message': 'Appointment update failed'
            }, status=400)


class PullAppointments(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        max_items = request.GET.get('max')
        params = {
            'max': max_items
        }
        appointments = Appointments.appointment_list(params)
        for appointment in appointments:
            appointment_id = appointment['id']
            first_name = appointment['firstName']
            last_name = appointment['lastName']
            phone_number = appointment['phone']
            email = appointment['email']

            # try:
            #     user = User.objects.get(email=email)
            # except:
            #     user = None
            # print(user)
            try:
                user = User.objects.get(email=email)
                user.phone_number = phone_number
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                print('user found')
            except User.DoesNotExist:
                print('error: not user found')
                print('creating new')
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=generate_unique_username([
                        first_name, last_name, email, 'user'
                    ]),
                    phone_number=phone_number,
                    is_patient=True,
                )
                user.save()
                setup_user_email(request, user, [])

            print(user)

            if user:
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    user_profile.contact_number = phone_number
                    user_profile.acuity_form_data = appointment['forms']
                    user_profile.save()

                except UserProfile.DoesNotExist:
                    user_profile = UserProfile(
                        user=user,
                        contact_number=phone_number,
                        acuity_form_data=appointment['forms']
                    )
                    user_profile.save()

                try:
                    object_item = AcuityAppointment.objects.get(user=user, acuity_appointment_id=appointment_id)
                    object_item.appointment_data = appointment
                    object_item.save()
                except AcuityAppointment.DoesNotExist:
                    AcuityAppointment.objects.create(user=user, acuity_appointment_id=appointment_id,
                                                     appointment_data=appointment)
        return Response(appointments)
