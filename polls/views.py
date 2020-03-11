from django.shortcuts import render,get_object_or_404,redirect
from  django.http import HttpResponseRedirect
#from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Question , Choice
from django.db.models import F
from django.utils import timezone
from  polls.forms import AddPollFormQ
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm


# Create your views here.
"""
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
	    'latest_question_list': latest_question_list,
	}
	return render(request, 'polls/index.html',context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html',{'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,'polls/results.html',{'question':question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select a choice.",})
	else:
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
"""

#Create a generic view.

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select a choice.",})
	else:
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



def add_poll(request):
	if request.method == 'POST':
		q_query = request.POST.get('question_input')
		if q_query is not None:
			q = Question(question_text = q_query,pub_date = timezone.now())
			q.save()
			messages.success(request,f"Question Added")
			return redirect("/polls")
		
	return render(request,"polls/add_poll.html")

def add_choice(request,question_id):
	question = get_object_or_404(Question, pk=question_id)
	if request.method == 'POST':
		
		choice_input_query = request.POST.get('choice_input',None)
		question.choice_set.create(choice_text=choice_input_query, votes=0)
		messages.success(request,f"Choice Added")
		return redirect("/polls")
	context = {"question":question}
		
	return render(request,"polls/add_choice.html",context)
	



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request,data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect("polls:index")
			else:
				messages.error(request,"Invalid username or password")
		else:
			messages.error(request,"Invalid username or password")

	form = AuthenticationForm()
	return render(request,'polls/login.html',{"form":form})

def logout_request(request):
	logout(request)
	messages.info(request,"Logged out successfully")
	return redirect("polls:index")

def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f"New Account Created: {username}")
			login(request,user)
			messages.info(request,f"You are now logged in as {username}")
			return redirect("polls:index")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")
	form = NewUserForm()
	return render(request,"polls/register.html",{"form":form})			
    
