from django import forms
from django.contrib.auth.models import User
from .models import Items

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150,help_text="")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ItemForm(forms.ModelForm):
    route_of_flights_form = [
        ('1st Route', 'from Point of Origin to RPMS'),
        ('2nd Route', 'from RPMS to Point of Destination'),
        ('3rd Route', 'from Point of Origin to Point of Destination'),
    ]

    bird_strike = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Bird Strike?"
    )

    runway_incursion = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.RadioSelect,
        label="Runway Incursion?"
    )

    route_of_flight = forms.ChoiceField(choices=route_of_flights_form)
    
    class Meta:
        model = Items
        fields = [
            'date_of_operation', 'call_sign', 'aircraft_type', 'detail',
            'origin', 'destination', 'route_of_flight','actual_time',
            'timeliness', 'type_of_flight', 'genav_detail', 'bird_strike',
            'runway_incursion','movement', 'user'
        ]
        labels = {
            'date_of_operation': 'Date of Operation',
            'call_sign': 'Call Sign',
            'aircraft_type': 'Type of Aircraft',
            'detail': 'Category',
            'origin': 'Point of Origin',
            'destination': 'Destination Airport',
            'route_of_flight': 'Flight route_of_flight',
            'actual_time': 'Actual Time (UTC)',
            'timeliness': 'Flight Timeliness',
            'type_of_flight': 'Type of Flight',
            'genav_detail': 'If GenAv, the detail:',
        }

        widgets = {
            'date_of_operation': forms.TextInput(attrs={'placeholder': 'MM/DD/YYYY'}),
            'call_sign': forms.TextInput(attrs={'placeholder': 'RP-C','id': 'id_call_sign'}),
            'route_of_flight': forms.Select(attrs={'id': 'id_route_of_flight'}),
            'origin': forms.TextInput(attrs={'id': 'id_origin'}),
            'destination': forms.TextInput(attrs={'id': 'id_destination'}),
            'actual_time': forms.TextInput(attrs={'id': 'id_actual_time'}),
            'type_of_flight': forms.Select(attrs={'id': 'id_type_of_flight'}),
            'genav_detail': forms.Select(attrs={'id': 'id_genav_detail'}),
            'movement': forms.Select(attrs={'id': 'id_movement'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        genav_detail = cleaned_data.get('genav_detail')
        flight_type = cleaned_data.get('type_of_flight')
        movement = cleaned_data.get('movement')
        bird_strike = cleaned_data.get('bird_strike')
        runway_incursion = cleaned_data.get('runway_incursion')
        actual_time = cleaned_data.get('actual_time')

       
        # Name arranging for counter sort

        if flight_type != "GenAv":
            cleaned_data['genav_detail'] = "N/A"

        if flight_type and movement and bird_strike:
            cleaned_data['bird_strike'] = f"{flight_type} {movement} {bird_strike}"

        if flight_type and movement and runway_incursion:
            cleaned_data['runway_incursion'] = f"{flight_type} {movement} {runway_incursion}"

        if flight_type and actual_time:
            cleaned_data['actual_time'] = f"{flight_type} {actual_time}"

        return cleaned_data

    
    

    

