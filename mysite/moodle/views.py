from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages
from .models import *
from .forms import *
from .utils import *
from django.contrib.auth import get_user_model, update_session_auth_hash
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
import calendar, pytz, csv, os, json, numpy, subprocess
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.decorators import login_required


utc=pytz.UTC

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
 

def aboutview(request):
	return render(request,"about.html")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_act_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/email_confirm.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/mysite/login')   
    else:
        return HttpResponse('Activation link is invalid!')

			 
def userpage(request):
	course_list = Course.objects.all()
	return render(request,'user.html',{'courses': course_list})


def teacherpage(request):
	course_list = request.user.profile.course_list
	# course_list = Course.objects.all()
	return render(request,'teacher.html',{'courses': course_list})

def teachercoursepage(request, uid):
	assignments = Uploada.objects.filter(course_code=uid)
	course_obj = Course.objects.get(course_code=uid)
	videos = Uploadv.objects.filter(course_code=uid)
	lectures = Uploadl.objects.filter(course_code=uid)
	return render(request,'teachercoursepage.html', 
		{'assignments': assignments, 
		'course_code':uid,
		'course_obj' : course_obj,
		'videos' : videos,
		'lectures' : lectures,
		})

def studentcoursepage(request, uid):
	assignments = Uploada.objects.filter(course_code=uid)
	solutions = Uploadb.objects.filter(course_code=uid, by_whom=request.user.username)
	lectures = Uploadl.objects.filter(course_code=uid)
	list1 = {}
	total = 0
	count = 0
	for solution in solutions:
		count += solution.status
		total +=1

	if total == 0:
		percent = 100
	else:
		percent = round((count/total)*100, 2)

	for assignment in assignments:
		solution = solutions.get(solution_for=assignment.title)
		list1.update({assignment:solution})

	todo = Uploadb.objects.filter(
		course_code=uid,
		end_time__gte=datetime.now(),
		by_whom=request.user.username,
		status=0,
		).order_by('-end_time')

	videos = Uploadv.objects.filter(course_code=uid)

	course_obj = Course.objects.get(course_code=uid)

	return render(request,'studentcoursepage.html',
		{'dictionary': list1,
		'course_code':uid,
		'percent' : percent,
		'todo' : todo,
		'time' : datetime.now(),
		'course_obj' : course_obj,
		'videos' : videos,
		'lectures' : lectures,
		})


def tacoursepage(request, uid):
	assignments = Uploada.objects.filter(course_code=uid)
	priviledges = tapriviledges.objects.get(ta_name=request.user.username, course_code=uid)
	course_obj = Course.objects.get(course_code=uid)

	return render(request,
		'tacoursepage.html',
		{'assignments': assignments,
		'course_code':uid, 
		'priviledges' : priviledges,
		'course_obj' : course_obj}
		)


def tapage(request):
	course_list = request.user.profile.course_list
	priviledges = tapriviledges.objects.filter(ta_name=request.user.username)
	return render(request,'ta.html',{'courses': course_list, 'priviledges' : priviledges})

def tapriviledge(request, code):
	if request.method == 'POST':
		form = TAForm(request.POST)
		if form.is_valid():
			ins = form.save(commit=False)
			ta_name1 = form.cleaned_data.get("ta_name")
			ta_model = tapriviledges.objects.filter(ta_name = ta_name1,
				course_code=code
				)
			ta_model.delete()
			ins.course_code = code
			ins.save()
			return redirect('../../teacher/')
	else:
		form = TAForm()
	args = {'form': form}	 
	return render(request,'priviledges.html', args)

def studentpage(request):
	course_list = request.user.profile.course_list
	dict_percent = {}
	dict_teacher = {}
	dict_total_assignments = {}
	dict_submission_count = {}
	for course,role in course_list.items():
		tempcourse = Course.objects.get(course_code=course)
		if (role == 'student'):
			total = 0
			count = 0
			solutions = Uploadb.objects.filter(course_code=course,by_whom=request.user.username)
			for solution in solutions:
				count += solution.status
				total +=1
			dict_total_assignments.update({course:total})
			dict_submission_count.update({course:count})	
			if total>0:
				percent = round((count/total)*100, 2)
			else: 
				percent = 100
			dict_percent.update({course:percent})

		for name,role in tempcourse.user_list.items():
			if (role == 'teacher'):
				dict_teacher.update({course:name})

	return render(request,'student.html',
		{'courses': course_list,
		'percent': dict_percent,
		'teacher':dict_teacher,
		'total':dict_total_assignments,
		'count':dict_submission_count
		})


def createcoursepage(request):
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			ins = form.save(commit=False)
			ins.course = request.user.profile
			request.user.profile.course_list[ins.course_code] = 'teacher'
			ins.user_list[request.user.username] = 'teacher'
			ins.save()
			request.user.profile.save()
			return redirect('../teacher')
	else:
		form = CourseForm()
	args = {'form': form}
	return render(request, 'createcourse.html', args)

def addstudentpage(request):
	c_list = request.user.profile.course_list
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			code = form.cleaned_data.get("course_code")
			usernames_list = form.cleaned_data.get("user_names")
			role_list = form.cleaned_data.get("roles")
			a_course = Course.objects.get(course_code=code)
			persons_list = usernames_list.split(",")
			roles_list = role_list.split(",")
			for i in range(len(persons_list)):
				tem_list = {persons_list[i]:roles_list[i]}
				a_course.user_list.update(tem_list)
				user_obj = User.objects.get(username=persons_list[i])
				ins = Profile.objects.get(user=user_obj)
				tem_list2 = {code:roles_list[i]}
				ins.course_list.update(tem_list2)
				ins.save()

				user = User.objects.get(username=persons_list[i])
				to_email = user.email
				res = send_mail(
					"You have been added to " + str(code), 
					"Hii " + str(persons_list[i]) +
					" You have been added to Course " + str(code) +
					" as a " + str(roles_list[i]), 
					os.environ['EMAIL_USER'], 
					[to_email,],
					fail_silently=False
					)

				if roles_list[i] == "ta":
					ins1 = tapriviledges.objects.create(
						ta_name=persons_list[i],
						course_code=code,
						enrollment=False,
						add_assignment=False,
						grade_assignment=True,
						)
					ins1.save()

			a_course.save()
			return redirect('../teacher')
	else:
		form = StudentForm()

	return render(request, 'addstudent.html',{'form': form,'courses':c_list})


def uploada(request, uid):
	tempcourse = Course.objects.get(course_code= uid)
	role = tempcourse.user_list[request.user.username]
	if request.method == 'POST':
		form = UploadaForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=False)
			title = form.cleaned_data.get('title')
			start = form.cleaned_data.get('start_time')
			end = form.cleaned_data.get('end_time')
			weightage = form.cleaned_data.get('weightage')
			description = form.cleaned_data.get('description')
			code = tempcourse.course_code
			uploada1 = request.FILES['uploada']
			for name,role in tempcourse.user_list.items():
				if role == 'student':
					object=Uploadb.objects.create(
						end_time=end,
						by_whom=name,
						title=title+str('-solution'),
						uploadb=uploada1,
						course_code=code,
						submit_time=end,
						solution_for=title,
						status=0,
						start_time=start,
						grade=0,
						feedback="NA",
						grade_status=0,
						weightage = weightage,
						)
					object.save()
					user = User.objects.get(username=name)
					to_email = user.email
					res = send_mail(
						'New Assignment', 
						"Hii " + str(name) + 
						" A new assignment has been added in Course " + str(code) +
						". Deadline is " + str(end), 
						os.environ['EMAIL_USER'], 
						[to_email,], 
						fail_silently=False
						)

			object=Grading.objects.create(
				course_code = code,
				assignment_name = title,
				mark_list = {},
				)
			object.save()

			object=Uploada.objects.create(
				title=title,
				uploada=uploada1,
				course_code=code,
				description=description,
				weightage=weightage,
				start_time=start,
				end_time=end,
				)

			object.save()
			return redirect('/mysite/' + str(tempcourse.user_list[request.user.username]))
		else:
		    messages.error(request,('Unable to complete request'))
	else:
		form = UploadaForm()
		
	args = {'form': form}
	return render(request, 'uploada.html',args)

	

def uploadl(request, uid):
	tempcourse = Course.objects.get(course_code= uid)
	role = tempcourse.user_list[request.user.username]
	if request.method == 'POST':
		form = UploadlForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=False)
			title = form.cleaned_data.get('title')
			description = form.cleaned_data.get('description')
			code = tempcourse.course_code
			uploadl1 = request.FILES['uploadl']
			object=Uploadl.objects.create(
				title=title,
				uploadl=uploadl1,
				course_code=code,
				description=description,
				)
			object.save()
			return redirect('/mysite/' + str(role)) 
		else:
		    messages.error(request,('Unable to complete request'))  
	else:
		form = UploadlForm()
		
	args = {'form': form}
	return render(request, 'uploadl.html',args)


def uploadb(request, uid, aid):
	tempcourse = Course.objects.get(course_code= uid)
	role = tempcourse.user_list[request.user.username]
	code = tempcourse.course_code
	now = timezone.now()
	submit_time = datetime.now()
	solution_for = aid
	by_whom=request.user.username
	object=Uploadb.objects.get(by_whom=by_whom,
	course_code=code,
	solution_for=solution_for,
	)
	s_t = utc.localize(object.start_time)
	e_t = utc.localize(object.end_time)

	if object.start_time < submit_time < object.end_time:
		if request.method == 'POST':
			form = UploadbForm(request.POST, request.FILES)
			if form.is_valid():
				form.save(commit=False)
				uploadb1= request.FILES['uploadb']
				object.uploadb= uploadb1
				object.status =1
				object.submit_time = datetime.now()
				object.save()
				user=User.objects.get(username=request.user.username)
				to_email = user.email
				res = send_mail('Assignment Submission', 
				 "You have submiited solution for " + str(solution_for) + " at " + str(submit_time), 
				 os.environ['EMAIL_USER'], 
				 [to_email,],
				 fail_silently=False
				 )

				return redirect('/mysite/' + str(role))
			else:
			    messages.error(request,('Unable to complete request'))  
		else:
			form = UploadbForm()
			
		args = {'form': form}
		return render(request, 'uploadb.html',args)
	else:
		return HttpResponse('Deadline is completed! :( or not yet started :)')


def uploadv(request, code):
	tempcourse = Course.objects.get(course_code= code)
	role = tempcourse.user_list[request.user.username]
	if request.method == 'POST':
		form = UploadvForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=False)
			title = form.cleaned_data.get('title')
			description = form.cleaned_data.get('description')
			code = tempcourse.course_code
			uploadv1 = form.cleaned_data.get('video_url')
			object=Uploadv.objects.create(
				title=title,
				video_url=uploadv1,
				course_code=code,
				description=description,
				submit_time=datetime.now(),
				)
			object.save()
			return redirect('/mysite/' + str(role)) 
		else:
		    messages.error(request,('Unable to complete request'))  
	else:
		form = UploadvForm()
		
	args = {'form': form}
	return render(request, 'uploadv.html',args)	


def downloada(request, code):
	if request.method=='POST':
		title=request.POST['title']
		code=request.POST['course_code']
		upload1=request.FILES['uploada']
		object=Uploada.objects.filter(title=title,uploada=upload1,course_code=code)
	return render(request,'download.html',{'object':object})

def downloadb(request, code, title1):
	tempcourse = Course.objects.get(course_code= code)
	role = tempcourse.user_list[request.user.username]
	if role == "teacher" or role == "ta":
		object=Uploadb.objects.filter(course_code=code, solution_for=title1)
		return render(request,'download_sol.html', {'course_code' : code,'objects':object,'title' : title1})
	else: 
		return HttpResponse("You are not allowed!")

def uploadg(request, code, title1):
	tempcourse = Course.objects.get(course_code=code)
	role = tempcourse.user_list[request.user.username]
	if role == "teacher" or role == "ta":
		if request.method == 'POST':
			form = UploadgForm(request.POST, request.FILES)
			if form.is_valid():
				form.save(commit=False)
				uploadg1 = request.FILES['uploadg']
				object=Uploadg.objects.create(title=title1,course_code=code,uploadg=uploadg1)
				object.save()
				my_path = os.path.abspath(os.path.dirname(__file__))
				path = os.path.join(my_path[:-7], "media/media/uploadg/")
				path += uploadg1.name
				with open(path, mode ='r') as file:
					csvFile = csv.reader(file)
					for lines in csvFile:
						object=Uploadb.objects.get(by_whom=lines[0], course_code=code, solution_for=title1)
						object.grade = lines[1]
						object.feedback = lines[2]
						object.grade_status = 1
						object.save()
						#added later for grading model
						object=Grading.objects.get(course_code=code, assignment_name=title1)
						object.mark_list.update({lines[0]:lines[1]})
						object.save()

				return redirect('/mysite/' + str(role) + "/" + str(code))  
		else:
			form = UploadgForm()
	else:
		return HttpResponse("you are not allowed to do this!")
		
	args = {'form': form}
	return render(request, 'uploadg.html',args)

def uploadag(request, uid, aid):
    tempcourse = Course.objects.get(course_code= uid)
    role = tempcourse.user_list[request.user.username]
    if role == "teacher" or role == "ta":
            if request.method == 'POST':
                form = UploadagForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save(commit=False)
                    code = tempcourse.course_code
                    uploadag1 = request.FILES['uploadag']
                    object = Uploadag.objects.create(
                        uploadag=uploadag1,
                        course_code=code,
                        ag_for=aid,
                    )
                    object.save()
                    object2=Uploada.objects.get(course_code=uid,title=aid)
                    object2.is_ag = 1
                    object2.save()
                    return redirect('/mysite/' + str(role))
                else:
                    messages.error(request,('Unable to complete request'))
            else:
                form = UploadagForm()   
            args = {'form': form}
            return render(request, 'uploadag.html',args)
    else :
        HttpResponse("You are not allowed to do this!")

def autograde(request, uid, aid):
    tempcourse = Course.objects.get(course_code = uid)
    role = tempcourse.user_list[request.user.username]
    object1 = Uploadag.objects.get(course_code = uid, ag_for = aid)
    object2 = Uploadb.objects.get(solution_for=aid, by_whom = request.user.username, course_code = uid)
    if object2.status == 1:
        my_path = os.path.abspath(os.path.dirname(__file__))
        agfile = object1.uploadag.name
        solfile = object2.uploadb.name
        agpath = os.path.join(my_path[:-7],"media/",agfile)
        solpath = os.path.join(my_path[:-7],"media/",solfile)
        s = subprocess.check_output("python3 "+str(agpath)+" -s "+str(solpath), shell=True)
        a,b = s.decode('utf-8').split(",")
        object2.grade = int(a)
        object2.feedback = b
        object2.grade_status = 1
        object2.save()
        object3 = Grading.objects.get(course_code=uid, assignment_name=aid)
        temp = {request.user.username : a}
        object3.mark_list.update(temp)
        object3.save()
        return redirect('/mysite/' + str(role) + "/" + str(uid))
    else:
        return HttpResponse("Please submit the solution first")

def editprofile(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		if user_form.is_valid():
		    user_form.save()
		    messages.success(request,('Your profile was successfully updated!'))
		else:
		    messages.error(request,('Unable to complete request'))
		return redirect ("userpage")
	user_form = UserForm(instance=request.user)
	return render(request = request, template_name ="editprofile.html", context = {"user":request.user, 
		"user_form": user_form })


class CalendarView(generic.ListView):
    model = Uploada
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required

def privatechat(request):
	if request.method == 'POST':
		form = PrivateChatForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			frnd_username = str(form.cleaned_data.get("username"))
			our_username = str(request.user.username)
			if(frnd_username < our_username ):
				room_name = frnd_username + "-" + our_username
			else:
				room_name = our_username + "-" + frnd_username

			return redirect(f'/privatechat/{room_name}')
	else:
		form = PrivateChatForm()
	args = {'form': form}
	return render(request, 'chat/privatechat.html',args)

def privateroom(request, room_name):
	user1,user2 = room_name.split("-")
	if( ((str(user1)==str(request.user.username)) or  (str(user2)==str(request.user.username))) and  not(str(user1)==str(user2)) ):
	    return render(request, 'chat/room.html', {
	        'room_name_json': mark_safe(json.dumps(room_name)),
	        'username': mark_safe(json.dumps(request.user.username)),
	    })
	else:
		return HttpResponse("Respect privacy!!")



def room(request, room_name):
    tempcourse = Course.objects.get(course_code=room_name)
    role = tempcourse.user_list[request.user.username]
    if tempcourse.chat_status :
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(request.user.username)),
            'code' : room_name,
            'role' : role,
        })
    return HttpResponse("Chat closed temporarily!")


def on_off(request, room_name):
	course_obj = Course.objects.get(course_code=room_name)
	course_obj.chat_status = not(course_obj.chat_status)
	course_obj.save()
	return redirect(f"../../mysite/teacher/{room_name}/")

def graphpage(request):
	course_list = request.user.profile.course_list
	grading={}
	for c,role in course_list.items():
		if (role == 'teacher' or role == 'ta'):
			grades_per_course = Grading.objects.filter(course_code=c)
			grading.update({c:grades_per_course})
			# marklist of various students for a course and an assignment of that course
			# is present inside the grading model object
	return render(request,'graphs.html',
		{'courses': course_list,
		'grades':grading,
		'role' : role,
		})


def graphcoursepage(request, uid):
	grades = Grading.objects.filter(course_code=uid)
	tempcourse = Course.objects.get(course_code=uid)
	role = tempcourse.user_list[request.user.username]
	dict_sum_grades = {}
	for g in grades:
		for name,marks in g.mark_list.items():
			if name in dict_sum_grades.keys():
				dict_sum_grades[name] = int(dict_sum_grades[name]) + int(marks);
			else:
				dict_sum_grades.update({name:marks})
	dict_mean={}
	dict_var = {}
	cum_mean = 0
	cum_var = 0
	test_list = []

	for g in grades:
		if len(g.mark_list.values()) != 0:
			test_list = list(map(int, g.mark_list.values()))
		mymean = numpy.mean(test_list)
		myvar = numpy.var(test_list)
		cum_mean += mymean
		cum_var += myvar
		dict_mean.update({g.assignment_name:mymean})
		dict_var.update({g.assignment_name:myvar})


	return render(request,'graphscoursepage.html',
		{'grades_per_course': grades,
		'course_code':uid,
		'sum_grades':dict_sum_grades,
		'mean':dict_mean,
		'variance':dict_var,
		'cummulative_mean':cum_mean,
		'cummulative_variance':cum_var,
		'role' : role
		})
