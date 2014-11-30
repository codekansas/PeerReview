from django import forms
from PeerReviewApp.models import *
from models import *
from django.conf import settings

SCHOOLS = settings.SCHOOLS
	
class LoginForm(forms.Form):
	''' On log in, you only need an email and a password '''
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Emory Email Address'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class AccountForm(forms.ModelForm):
	''' This is a pythonic way of changing a single user's settings ''' 
	def __init__(self, *args, **kwargs):
		super(AccountForm, self).__init__(*args, **kwargs)
		try:
			has_agreed = self.instance.agreed_to_form
		except AttributeError:
			has_agreed = True
		if has_agreed:
			self.fields['agreed_to_form'].widget = forms.widgets.HiddenInput()
		
	class Meta:
		model = SiteUser
		fields = ('email', 'first_name', 'last_name', 'department', 'lab', 'pi', 'school','review_count','agreed_to_form')
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control text-center', 'placeholder': 'Emory Email Address'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'First Name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Last Name'}),
			'department': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Department'}),
			'lab': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Name of Lab'}),
			'pi': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Name of Primary Investigator'}),
			'school': forms.Select(attrs={'class': 'form-control text-center', 'placeholder': 'Choose your School'}),
            'review_count': forms.TextInput(attrs={'class': 'form-control text-center','placeholder': 'Number of manuscripts previous reviewed'}),
		    }

class AgreementForm(forms.ModelForm):
	''' This is for just the agreement form. It allows the logged in
		user to agree with the Terms of Service document '''
	class Meta:
		model = SiteUser
		fields = ('agreed_to_form',)

class SignupForm(forms.ModelForm):
	''' This is the main sign-up form '''
	error_messages = { # Add errors here
		'password_mismatch': 'The two password fields didn\'t match.',
        }
	# Form needs two passwords to make sure the user doesn't mistype
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text-center', 'placeholder': 'Enter your Password'}), label='Password', help_text='Choose a password')
	retype_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control text-center', 'placeholder': 'Re-enter your password, for verification'}), label='Retype Password', help_text='Enter the same password as above, for verification.')
	
	class Meta:
		model = SiteUser
		# These are the fields that the user needs to input when they create their account
		fields = ('email', 'first_name', 'last_name', 'department', 'lab', 'pi', 'school','review_count')
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control text-center', 'placeholder': 'Emory Email Address'}),
			'first_name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'First Name'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Last Name'}),
			'department': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Department'}),
			'lab': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Name of Lab'}),
			'pi': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Name of Primary Investigator'}),
			'school': forms.Select(attrs={'class': 'form-control text-center', 'placeholder': 'Choose your School'}),
            'review_count': forms.TextInput(attrs={'class': 'form-control text-center','placeholder': 'Number of manuscripts previous reviewed'}),
		    }
	
	# This method validates that the two passwords are the same
	# If they don't match it throws an error
	def clean_retype_password(self):
		password = self.cleaned_data.get('password')
		retype_password = self.cleaned_data.get('retype_password')
		if password and retype_password and password != retype_password:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			    )
		return retype_password
	
	# This is the method for saving the newly created user
	def save(self, commit=True):
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

class UploadFileForm(forms.Form):
	''' Form for uploading a file '''
	upload = forms.FileField()
	
	def clean_upload(self):
		upload = self.cleaned_data['upload']
		content_type = upload.content_type
		if content_type in settings.CONTENT_TYPE:
			if upload._size > settings.MAX_UPLOAD_SIZE:
				raise forms.ValidationEngineer('Exceeded maximum file size')
		else:
			raise forms.ValidationError('File type is not allowed.')
		
		return upload

class UploadManuscript(forms.ModelForm):
    class Meta:
        model = Manuscript
        exclude = ('review_period', 'authors', 'reviewers', 'is_final','manuscript')

	fields = ('title', 'brief_title', 'abstract', 'field', 'keywords', 'target_journal',)
	widgets = {
		'title': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Enter Manuscript Title'}),
		'brief_title': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Enter a shorter title which contains less than 10 words'}),
		'abstract': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Enter Manuscript Abstract'}),
		'field': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Manuscript Field (for example: CS, BIO)'}),
		'keywords': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Keywords (no more than 10, separate by commas)'}),
		'target_journal': forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Which journal do you want to publish in?'}),
	    }

	def __init__(self, *args, **kwargs):
		super(UploadManuscript, self).__init__(*args, **kwargs)
