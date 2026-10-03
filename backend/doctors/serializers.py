from django.db.models import Count, Q
from rest_framework import serializers
from .models import Doctor
from patients.models import Patient
from bindings.models import Binding
from tasks.models import FollowupTask


class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'username', 'phone', 'real_name', 'hospital', 'department', 'title', 'audit_status']


class PatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    binding_status = serializers.SerializerMethodField()
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'username', 'phone', 'real_name', 'id_card', 'gender', 'age',
                  'surgery_type', 'surgery_date', 'binding_status', 'completion_rate', 'created_at']

    def get_binding_status(self, obj):
        request = self.context.get('request')
        doctor = self.context.get('doctor')
        if doctor:
            try:
                binding = Binding.objects.get(doctor=doctor, patient=obj)
                return binding.status
            except Binding.DoesNotExist:
                return None
        return None

    def get_completion_rate(self, obj):
        doctor = self.context.get('doctor')
        if doctor is None:
            return 0

        task_counts = FollowupTask.objects.filter(
            doctor=doctor,
            patient=obj,
        ).aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
        )
        total = task_counts['total']
        if not total:
            return 0
        return round(task_counts['completed'] * 100 / total)


class BindingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Binding
        fields = ['id', 'patient', 'status', 'created_at']


class CreateFollowupTaskSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    task_types = serializers.JSONField()  # 改为JSONField以支持复杂结构
    deadline = serializers.DateTimeField()


class FollowupTaskSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.real_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.real_name', read_only=True)

    class Meta:
        model = FollowupTask
        fields = ['id', 'doctor', 'patient', 'patient_name', 'doctor_name', 'title', 'content',
                  'task_types', 'deadline', 'status', 'created_at']
