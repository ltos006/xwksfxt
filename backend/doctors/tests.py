from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from bindings.models import Binding
from doctors.models import Doctor
from patients.models import Patient
from tasks.models import FollowupTask, TaskSubmission
from users.models import User


class DoctorPatientCompletionRateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.doctor = Doctor.objects.create(
            user=User.objects.create_user(
                username='doctor',
                password='test-password',
                phone='13800000001',
                role='doctor',
            ),
            real_name='测试医生',
            hospital='测试医院',
            department='外科',
            title='attending',
        )
        self.patient = Patient.objects.create(
            user=User.objects.create_user(
                username='patient',
                password='test-password',
                phone='13800000002',
                role='patient',
            ),
            real_name='测试患者',
            gender='female',
            age=40,
            surgery_type='测试手术',
        )
        Binding.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            status='approved',
        )

    def get_patient_list(self):
        return self.client.get(
            '/api/doctors/patients/',
            {'doctor_id': self.doctor.id},
        )

    def create_task(self, *, doctor=None, status='in_progress'):
        return FollowupTask.objects.create(
            doctor=doctor or self.doctor,
            patient=self.patient,
            title='术后随访',
            content='记录恢复情况',
            task_types=['text'],
            deadline=timezone.now() + timedelta(days=1),
            status=status,
        )

    def test_completion_rate_reflects_completed_tasks(self):
        completed_task = self.create_task(status='completed')
        self.create_task()
        TaskSubmission.objects.create(
            task=completed_task,
            patient=self.patient,
            submission_data={'text_response': '恢复良好'},
        )

        response = self.get_patient_list()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['completion_rate'], 50)

    def test_completion_rate_is_zero_when_patient_has_no_tasks(self):
        response = self.get_patient_list()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['completion_rate'], 0)

    def test_completion_rate_only_counts_tasks_from_this_doctor(self):
        self.create_task(doctor=Doctor.objects.create(
            user=User.objects.create_user(
                username='other-doctor',
                password='test-password',
                phone='13800000003',
                role='doctor',
            ),
            real_name='其他医生',
            hospital='其他医院',
            department='外科',
            title='attending',
        ), status='completed')
        self.create_task()

        response = self.get_patient_list()

        self.assertEqual(response.data[0]['completion_rate'], 0)
