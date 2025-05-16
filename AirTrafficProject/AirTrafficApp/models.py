from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class ArchiveGroup(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)


class Items(models.Model):
    
    category_choices = [
        ('Fixed Wing', 'Fixed Wing'),
        ('Helicopter', 'Helicopter')
    ]

    flight_choices = [
        ('Commercial', 'Commercial (Domestic)'),
        ('GenAv', 'General Aviation'),
        ('Military', 'Military'),
    ]

    movement_choices = [
        ('Arrival', 'Arrival'),
        ('Enroute', 'Enroute'),
        ('Departure', 'Departure')
    ]

    timeliness_choices = [
        ('Commercial Delayed', 'Commercial Delayed'),
        ('Commercial On Time', 'Commercial On Time'),
        ('Commercial N/A', 'Commercial N/A'),

        ('GenAv Delayed', 'GenAv Delayed'),
        ('GenAv On Time', 'GenAv On Time'),
        ('GenAv N/A', 'GenAv N/A'),

        ('Military Delayed', 'Military Delayed'),
        ('Military On Time', 'Military On Time'),
        ('Military N/A', 'Military N/A'),
    ]
    
    
    genav_choices = [
    
    # Arrival Options
        ('Arrival Private', 'Arrival Private'),
        ('Arrival Cargo', 'Arrival Cargo'),
        ('Arrival Med Evac', 'Arrival Med Evac'),
        ('Arrival Utility/Maintenance', 'Arrival Utility/Maintenance'),
        ('Arrival Training', 'Arrival Training'),
        ('Arrival Government', 'Arrival Government'),

        # Departure Options
        ('Departure Private', 'Departure Private'),
        ('Departure Cargo', 'Departure Cargo'),
        ('Departure Med Evac', 'Departure Med Evac'),
        ('Departure Utility/Maintenance', 'Departure Utility/Maintenance'),
        ('Departure Training', 'Departure Training'),
        ('Departure Government', 'Departure Government'),

        # Enroute Options
        ('Enroute Private', 'Enroute Private'),
        ('Enroute Cargo', 'Enroute Cargo'),
        ('Enroute Med Evac', 'Enroute Med Evac'),
        ('Enroute Utility/Maintenance', 'Enroute Utility/Maintenance'),
        ('Enroute Training', 'Enroute Training'),
        ('Enroute Government', 'Enroute Government'),
        ('N/A', 'N/A'),

    ]


    call_sign = models.CharField(max_length=20)
    aircraft_type = models.CharField(max_length=20)
    detail = models.CharField(max_length=20, choices=category_choices, default='Fixed Wing')
    origin = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    movement = models.CharField(max_length=20, choices=movement_choices, default='Arrival')
    route_of_flight = models.CharField(max_length=20)
    actual_time = models.CharField(max_length=50)
    timeliness = models.CharField(max_length=20, choices=timeliness_choices, default='on_time')
    type_of_flight = models.CharField(max_length=30, choices=flight_choices, default='commercial')
    date_of_operation = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    archive_group = models.ForeignKey(ArchiveGroup, on_delete=models.SET_NULL, null=True, blank=True)
    genav_detail = models.CharField(max_length=50, choices=genav_choices, default='N/A')
    bird_strike = models.CharField(max_length=50, default="yes")
    runway_incursion = models.CharField(max_length=50, default="yes")
