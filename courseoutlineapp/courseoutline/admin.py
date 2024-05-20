from django.contrib import admin
from courseoutline.models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import cloudinary


class OutlineForm(forms.ModelForm):
    overview = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Outline
        fields = "__all__"


class LecturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'age', 'code', 'position', 'account']
    search_fields = ['last_name']
    list_filter = ['last_name']


class OutlineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'credit', 'lecturer', 'active']
    search_fields = ['name', 'credit']
    list_filter = ['name']
    form = OutlineForm

    def evaluation_list(self, obj):
        return ", ".join([f"{eval.method} ({eval.percentage}%)" for eval in obj.evaluation.all()])

    evaluation_list.short_description = 'Evaluation'

    list_display.append('evaluation_list')


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'age', 'code', 'account']
    search_fields = ['last_name']
    list_filter = ['last_name', 'age']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'lecturer', 'active', 'created_date', 'updated_date']
    search_fields = ['subject']
    list_filter = ['subject']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'outline', 'created_date', 'student_name']
    search_fields = ['student_name']

    def student_name(self, obj):
        return obj.student.last_name

    student_name.short_description = 'Student'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'year']


admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
admin.site.register(Outline, OutlineAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Evaluation)
admin.site.register(Student, StudentAdmin)
admin.site.register(Comment, CommentAdmin)
