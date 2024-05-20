from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from courseoutline.models import *

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['year']


class AccountSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(required=True, write_only=True)

    # email = serializers.EmailField(required=True)
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'avatar', 'role', 'date_joined', 'code', 'is_approved']
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "role": {
                "read_only": True,
            },
            "date_joined": {
                "read_only": True,
            },
            "is_approved": {
                "read_only": True,
            }
        }


class LecturerAccountSerializer(AccountSerializer):
    avatar = serializers.ImageField(required=True, allow_null=False, allow_empty_file=False)

    class Meta:
        model = AccountSerializer.Meta.model
        fields = AccountSerializer.Meta.fields
        extra_kwargs = AccountSerializer.Meta.extra_kwargs

    def create(self, validated_data):
        code = f'{validated_data.pop("code"):06d}'
        lecturer = get_object_or_404(Lecturer, code=code)
        validated_data['role'] = Account.Role.LECTURER
        account = Account(**validated_data)
        account.set_password(account.password)
        account.save()
        lecturer.account = account
        lecturer.save()
        return account


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'percentage', 'method']


class StudentAccountSerializer(AccountSerializer):
    class Meta:
        model = AccountSerializer.Meta.model
        fields = AccountSerializer.Meta.fields
        extra_kwargs = AccountSerializer.Meta.extra_kwargs

    def create(self, validated_data):
        code = f"{validated_data.pop('code'):06d}"
        validated_data['is_approved'] = True
        student = get_object_or_404(Student, code=code)
        account = Account(**validated_data)
        account.set_password(account.password)
        account.save()
        student.account = account
        student.save()
        return account


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'code', 'first_name', 'last_name', 'age', 'gender', 'created_date', 'updated_date']


class StudentSerializer(UserSerializer):
    class Meta:
        model = Student
        fields = UserSerializer.Meta.fields


class LecturerSerializer(UserSerializer):
    class Meta:
        model = Lecturer
        fields = UserSerializer.Meta.fields + ['position']


class ApprovalSerializer(AccountSerializer):
    code = serializers.IntegerField(required=True, write_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Approval
        fields = ['id', 'is_approved', 'student', 'code']

    def create(self, validated_data):
        code = f"{validated_data.pop('code'):06d}"
        student = get_object_or_404(Student, code=code)
        try:
            approval = Approval.objects.create(student=student)
        except IntegrityError:
            raise ValidationError({"message": "Yeu cau dang duoc cho xu ly"})
        return approval


class OutlineSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True)
    evaluation = EvaluationSerializer(many=True)

    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url

        return req

    class Meta:
        model = Outline
        fields = ['id', 'name', 'credit', 'overview', 'created_date', 'image', 'lecturer', 'course',
                  'lesson', 'evaluation']
        read_only_fields = ['lecturer']

    def create(self, validated_data):
        raise NotImplementedError("Use OutlineViewSet.create_outline to create outlines.")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['lecturer', 'created_date', 'updated_date']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'outline', 'created_date', 'updated_date', 'student']
        read_only_fields = ['student', 'outline']


class OutlineApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outline
        fields = ['is_approved']


class CreateOutlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outline
        fields = ['id', 'name', 'credit', 'overview', 'created_date', 'updated_date', 'lecturer',
                  'lesson']
        read_only_fields = ['lecturer']
