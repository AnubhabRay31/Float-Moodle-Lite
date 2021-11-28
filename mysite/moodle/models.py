from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from  embed_video.fields  import  EmbedVideoField


# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	course_list = models.JSONField(default=dict)

	def __str__(self):
		return self.user.username

	@receiver(post_save, sender=User) 
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
	


class Course(models.Model):
	course = models.ForeignKey(Profile, on_delete = models.CASCADE)
	course_code = models.CharField(max_length=100, default='')
	user_list = models.JSONField(default=dict)
	user_names = models.CharField(max_length=100000,default='',blank=True)
	roles = models.CharField(max_length=100000,default='',blank=True)
	chat_status = models.BooleanField(default=True)
	def __str__(self):
		return self.course_code


class Uploada(models.Model):
	title = models.CharField(max_length=100, default='')
	course_code = models.CharField(max_length=100, default='')
	uploada = models.FileField(upload_to="media/uploada")
	description = models.TextField(default='')
	weightage = models.IntegerField(default='100')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	is_ag = models.IntegerField(default=0)

	def __str__(self):
		return self.title + "/" + str(self.course_code)

class Uploadb(models.Model):
	by_whom = models.CharField(max_length=100,default='')
	title = models.CharField(max_length=100, default='')
	uploadb = models.FileField(upload_to="media/uploadb")
	course_code = models.CharField(max_length=100, default='')
	status = models.IntegerField(default='0')
	solution_for = models.CharField(max_length=100, default='')
	submit_time = models.DateTimeField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	weightage = models.IntegerField(default='100')
	grade_status = models.IntegerField(default='0')
	grade = models.IntegerField(default='0')
	feedback = models.TextField(default='')

	def __str__(self):
		return self.title + "/" + str(self.course_code)

class Uploadg(models.Model):
	course_code = models.CharField(max_length=100, default='')
	title = models.CharField(max_length=100, default='')
	uploadg = models.FileField(upload_to="media/uploadg")

	def __str__(self):
		return self.title + "/" + str(self.course_code)

class Grading(models.Model):
	course_code = models.CharField(max_length=100, default='')
	assignment_name = models.CharField(max_length=100, default='')
	mark_list = models.JSONField(default=dict)

	def __str__(self):
		return self.course_code + "/" + str(self.assignment_name)

class Uploadl(models.Model):
	title = models.CharField(max_length=100, default='')
	course_code = models.CharField(max_length=100, default='')
	uploadl = models.FileField(upload_to="media/uploadl")
	description = models.TextField(default='', blank=True)

	def __str__(self):
		return self.title + "/" + str(self.course_code)

class Uploadv(models.Model):
	title = models.CharField(max_length=100, default="")
	course_code = models.CharField(max_length=100, default="")
	description = models.TextField(default="")
	video_url = EmbedVideoField()
	submit_time = models.DateTimeField()

	def __str__(self):
		return self.title + "/" + str(self.course_code) + "/video" 

class tapriviledges(models.Model):
	# CHOICES = (
	# 	('1','Enroll new students to a course'),
	# 	('2','Add new Assignments'),
	# 	('3','Upload marks and feedback.'),
	# )
	ta_name = models.CharField(max_length=100,default='')
	course_code = models.CharField(max_length=100,default='') 
	enrollment = models.BooleanField(default=False)
	add_assignment = models.BooleanField(default=False)
	grade_assignment = models.BooleanField(default=True)

	def __str__(self):
		return self.ta_name + "/" + str(self.course_code)

# from django.contrib.auth import get_user_model
# User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100, default='')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name

    def last_10_messages(room):
    	return Message.objects.order_by('-timestamp').filter(room_name=room)[:10]


class PrivateChat(models.Model):
	username = models.CharField(max_length=100, default='')


class Uploadag(models.Model):
    course_code = models.CharField(max_length=100, default='')
    uploadag = models.FileField(upload_to="media/uploadag")
    ag_for = models.CharField(max_length=100, default='')
    def __str__(self):
        return str(ag_for) + "/" + str(self.course_code) + "/" + str(ag)