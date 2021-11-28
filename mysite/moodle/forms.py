from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm, DateInput

class RegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=50,required=True)
	
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',	
		)



class UserForm(forms.ModelForm):
	first_name = forms.CharField(max_length=50,required=True)
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = (
			'course_code',
			)

class UploadaForm(forms.ModelForm):
	title = forms.CharField(max_length=50,required=True)
	uploada = forms.FileField()
	class Meta:
		model = Uploada
		widgets = {
			'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
			'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
	    }
		fields = (
			'title',
			'description',
			'uploada',
			'weightage',
			'start_time',
			'end_time',
			)
	def __init__(self, *args, **kwargs):
		super(UploadaForm, self).__init__(*args, **kwargs)
		# input_formats parses HTML5 datetime-local input to datetime field
		self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
		self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class UploadlForm(forms.ModelForm):
	title = forms.CharField(max_length=50,required=True)
	uploadl = forms.FileField()
	class Meta:
		model = Uploadl
		fields = (
			'title',
			'description',
			'uploadl',
			)
		
class UploadgForm(forms.ModelForm):
	uploadg = forms.FileField()
	class Meta:
		model = Uploadg
		fields = (
			'uploadg',
			)

class UploadagForm(forms.ModelForm):
	uploadag = forms.FileField()
	class Meta:
		model = Uploadag
		fields = (
			'uploadag',
			)


class UploadbForm(forms.ModelForm):
	uploadb = forms.FileField()
	class Meta:
		model = Uploadb
		fields = (
			'uploadb',
			)

class UploadvForm(forms.ModelForm):
	class Meta:
		model = Uploadv
		fields = (
			'title',
			'description',
			'video_url',
			)

class StudentForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = (
			'course_code',
			'user_names',
			'roles',
			)

def save(self, commit=True):
	user = super(RegistrationForm, self).save(commit=False) 	
	user.first_name = self.cleaned_data['first_name']
	user.last_name = self.cleaned_data['last_name']
	user.email = self.cleaned_data['email']

class TAForm(forms.ModelForm):
	ta_name = models.CharField(max_length=100,default='')
	class Meta:
		model = tapriviledges
		fields = (
			'ta_name',
			# 'course_code',
			'enrollment',
			'add_assignment',
			'grade_assignment',
			)

class PrivateChatForm(forms.ModelForm):
	class Meta:
		model = PrivateChat
		fields = (
			'username',
			)