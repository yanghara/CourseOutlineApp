import random

from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Account(AbstractUser):
    first_name = None
    last_name = None

    avatar = CloudinaryField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Quản trị viên'
        LECTURER = 'lecturer', 'Giảng viên'
        STUDENT = 'student', 'Sinh viên'

    # Trường mở rộng để lưu vai trò của người dùng
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    from courseoutline.managers import AccountManager
    objects = AccountManager()

    def __str__(self):
        return self.username

    # Xác định xem người dùng có phải là quản trị viên hay không
    def is_admin(self):
        return self.role == 'admin'

    # Xác định xem người dùng có phải là giảng viên hay không
    def is_lecturer(self):
        return self.role == 'lecturer'

    def is_student(self):
        return self.role == 'student'

    def get_lecturer_profile(self):
        try:
            return self.lecturers.get()
        except Lecturer.DoesNotExist:
            return None

    def get_student_profile(self):
        try:
            return self.students.get()
        except Student.DoesNotExist:
            return None


class User(BaseModel):
    class Meta:
        abstract = True

    account = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)ss')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.CharField(max_length=2)
    gender = models.BooleanField(default=True)  # true is female, false is male
    code = models.CharField(max_length=10, null=True, blank=True, unique=True, editable=False)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def save(self, *args, **kwargs):
        super().save(args, kwargs)
        if not self.code:
            self.code = self.generate_code()
            self.save()

    def generate_code(self):
        return f"{random.randint(0, 90):04d}{self.id:02d}"


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Evaluation(BaseModel):
    percentage = models.FloatField()
    method = models.CharField(max_length=255)
    note = models.CharField(max_length=255)


class Lecturer(User):
    position = models.CharField(max_length=255)


class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject


class Course(BaseModel):
    year = models.IntegerField(unique=True)

    lessons = models.ManyToManyField(Lesson)


class Outline(BaseModel):
    name = models.CharField(max_length=255)
    credit = models.IntegerField()
    overview = RichTextField()
    image = CloudinaryField(null=True)
    is_approved = models.BooleanField(default=False)  # nhớ thêm vào
    evaluation = models.ManyToManyField(Evaluation)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Student(User):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.PROTECT)
    lessons = models.ManyToManyField(Lesson, blank=True)
    outline = models.ManyToManyField(Outline, blank=True)


class Interaction(BaseModel):
    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.TextField()


class Chat(BaseModel):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Approval(BaseModel):
    is_approved = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, unique=True)
