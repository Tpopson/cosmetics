from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django import forms 
from .models import Profile


# django forms 
class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username here'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name here'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name here'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email here'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repeat Password'}))


    class Meta:
        model = User 
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2')

    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    

        
class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Old Password'}))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter New Password'}))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repeat new Password'}))

    class Meta:
        model = User 
        fields = ('old_password','new_password1','new_password2')


    def __init__(self,*args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


        
class RestPasswordForm(PasswordResetForm):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email address.'}))
    

    class Meta:
        model = User 
        fields = ('email',)


    def __init__(self,*args, **kwargs):
        super(RestPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'



# modelform 
STATE =[
    ('Abia', 'Abia'),
    ('Bayelsa', 'Bayelsa'),
    ('Delta', 'Delta'),
    ('Edo', 'Edo'),
    ('Lagos', 'Lagos'),
]
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','email','phone','address','city','state','profile_img')
        widgets ={
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email Address'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Address'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter City'}),
            'state': forms.Select(attrs={'class':'form-control', 'placeholder':'Enter State'}, choices=STATE),
            'profile_img': forms.FileInput(attrs={'class':'form-control'})
        }
        