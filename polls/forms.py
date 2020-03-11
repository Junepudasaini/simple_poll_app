from django import forms
from .models import Question , Choice
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddPollFormQ(forms.ModelForm):
	class Meta:
		model = Question
		fields = (
			       'question_text',
			       'pub_date',)



class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username","first_name","last_name","email","password1","password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit= False)
		user.email=self.cleaned_data['email']
		if commit:
			user.save()
		return user	
    		
    
    		