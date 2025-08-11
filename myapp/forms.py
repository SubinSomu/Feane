from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'guests']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'required': 'required'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone', 'required': 'required'}),
            'date': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
            'guests': forms.Select(choices=[(i, str(i)) for i in range(1, 6)] + [(6, '5+')], attrs={'required': 'required'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
