from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm, ItemForm
from .models import Items, ArchiveGroup


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
           
            user = User.objects.create_user(
                username=username, 
                password=password, 
                first_name=first_name, 
                last_name=last_name
            )   
            return redirect('login')     
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    error_message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials"
    return render(request, 'accounts/login.html', {'error': error_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    elif request.method == "GET":
        return render(request, 'accounts/logout.html')
    else:
        return redirect('home')


@login_required
def home_view(request):
    users = User.objects.all()
    return render(request, 'main_site/home.html', {'users': users})

@login_required
def create_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('items')
    else:
        form = ItemForm()
    return render(request, 'main_site/create_form.html', {'form': form})


@login_required
def item_list_view(request):
    items = Items.objects.filter(archive_group__isnull=True)
    return render(request, 'main_site/item_list.html', {'items': items})


@login_required
def delete_item_view(request, item_id):
    item = Items.objects.get(id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect('items')
    return render(request, 'main_site/delete.html', {'item': item})


@login_required
def item_edit_view(request, item_id):
    item = Items.objects.get(id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('items')
        else:
            form = ItemForm(instance=item)
    return render(request, 'main_site/item_edit_form.html', {'form': form})


@login_required
def archive_dataset_view(request):
    if request.method == "POST":
        group = ArchiveGroup.objects.create()
        Items.objects.filter(archive_group__isnull=True).update(archive_group=group)
        return redirect('items')  
    return render(request, 'main_site/archive.html')


def archive_view(request):
    if request.method == "GET":
        archive = ArchiveGroup.objects.all().order_by('-id')
        
        for group in archive:
            items = group.items_set.all()

            # Details (Category) Counts
            group.fixed_wing_count = items.filter(detail__icontains="Fixed Wing").count()
            group.helicopter_count = items.filter(detail__icontains="Helicopter").count()
            group.detail_total = group.fixed_wing_count + group.helicopter_count

            # Commercial Movement
            group.commercial_arrival = items.filter(actual_time__icontains="Commercial ARR").count()
            group.commercial_departure = items.filter(actual_time__icontains="Commercial DEP").count()
            group.commercial_enroute = items.filter(actual_time__icontains="Commercial ENRT").count()
            group.commercial_movement_total = (
                group.commercial_arrival +
                group.commercial_departure +
                group.commercial_enroute
            )

            # GenAv Movement
            group.genav_arrival = items.filter(actual_time__icontains="GenAv ARR").count()
            group.genav_departure = items.filter(actual_time__icontains="GenAv DEP").count()
            group.genav_enroute = items.filter(actual_time__icontains="GenAv ENRT").count()
            group.genav_movement_total = (
                group.genav_arrival +
                group.genav_departure +
                group.genav_enroute
            )

            # Military Movement
            group.military_arrival = items.filter(actual_time__icontains="Military ARR").count()
            group.military_departure = items.filter(actual_time__icontains="Military DEP").count()
            group.military_enroute = items.filter(actual_time__icontains="Military ENRT").count()
            group.military_movement_total = (
                group.military_arrival +
                group.military_departure +
                group.military_enroute
            )

            # Total Movement
            group.arrival_total = group.commercial_arrival + group.genav_arrival + group.military_arrival
            group.departure_total = group.commercial_departure + group.genav_departure + group.military_departure
            group.enroute_total = group.commercial_enroute + group.genav_enroute + group.military_enroute
            group.movement_overall_total = group.arrival_total + group.departure_total + group.enroute_total

            # Commercial Timeliness
            group.commercial_delayed = items.filter(timeliness__icontains="Commercial Delayed").count()
            group.commercial_ontime = items.filter(timeliness__icontains="Commercial On Time").count()
            group.commercial_na = items.filter(timeliness__icontains="Commercial N/A").count()
            group.commercial_timeliness_total = (
                group.commercial_delayed +
                group.commercial_ontime +
                group.commercial_na
            )

            # GenAv Timeliness
            group.genav_delayed = items.filter(timeliness__icontains="GenAv Delayed").count()
            group.genav_ontime = items.filter(timeliness__icontains="GenAv On Time").count()
            group.genav_na = items.filter(timeliness__icontains="GenAv N/A").count()
            group.genav_timeliness_total = (
                group.genav_delayed +
                group.genav_ontime +
                group.genav_na
            )

            # Military Timeliness
            group.military_delayed = items.filter(timeliness__icontains="Military Delayed").count()
            group.military_ontime = items.filter(timeliness__icontains="Military On Time").count()
            group.military_na = items.filter(timeliness__icontains="Military N/A").count()
            group.military_timeliness_total = (
                group.military_delayed +
                group.military_ontime +
                group.military_na
            )

            # Total Timeliness
            group.delayed_total = group.commercial_delayed + group.genav_delayed + group.military_delayed
            group.ontime_total = group.commercial_ontime + group.genav_ontime + group.military_ontime
            group.na_total = group.commercial_na + group.genav_na + group.military_na
            group.timeliness_overall_total = group.delayed_total + group.ontime_total + group.na_total

            # Commercial Bird Strike
            group.commercial_arrival_birdstrike = items.filter(bird_strike__icontains="Commercial Arrival yes").count()
            group.commercial_departure_birdstrike = items.filter(bird_strike__icontains="Commercial Departure yes").count()
            group.commercial_enroute_birdstrike = items.filter(bird_strike__icontains="Commercial Enroute yes").count()
            group.commercial_birdstrike_total = (
                group.commercial_arrival_birdstrike +
                group.commercial_departure_birdstrike +
                group.commercial_enroute_birdstrike
            )

            # GenAv Bird Strike
            group.genav_arrival_birdstrike = items.filter(bird_strike__icontains="GenAv Arrival yes").count()
            group.genav_departure_birdstrike = items.filter(bird_strike__icontains="GenAv Departure yes").count()
            group.genav_enroute_birdstrike = items.filter(bird_strike__icontains="GenAv Enroute yes").count()
            group.genav_birdstrike_total = (
                group.genav_arrival_birdstrike +
                group.genav_departure_birdstrike +
                group.genav_enroute_birdstrike
            )

            # Military Bird Strike
            group.military_arrival_birdstrike = items.filter(bird_strike__icontains="Military Arrival yes").count()
            group.military_departure_birdstrike = items.filter(bird_strike__icontains="Military Departure yes").count()
            group.military_enroute_birdstrike = items.filter(bird_strike__icontains="Military Enroute yes").count()
            group.military_birdstrike_total = (
                group.military_arrival_birdstrike +
                group.military_departure_birdstrike +
                group.military_enroute_birdstrike
            )

            # Total Bird Strike
            group.arrival_total_birdstrike = group.commercial_arrival_birdstrike + group.genav_arrival_birdstrike + group.military_arrival_birdstrike
            group.departure_total_birdstrike = group.commercial_departure_birdstrike + group.genav_departure_birdstrike + group.military_departure_birdstrike
            group.enroute_total_birdstrike = group.commercial_enroute_birdstrike + group.genav_enroute_birdstrike + group.military_enroute_birdstrike
            group.birdstrike_overall_total = group.arrival_total_birdstrike + group.departure_total_birdstrike + group.enroute_total_birdstrike

            # Commercial Runway Intrusion
            group.commercial_arrival_runwayintrusion = items.filter(runway_incursion__icontains="Commercial Arrival yes").count()
            group.commercial_departure_runwayintrusion = items.filter(runway_incursion__icontains="Commercial Departure yes").count()
            group.commercial_enroute_runwayintrusion = items.filter(runway_incursion__icontains="Commercial Enroute yes").count()
            group.commercial_runwayintrusion_total = (
                group.commercial_arrival_runwayintrusion +
                group.commercial_departure_runwayintrusion +
                group.commercial_enroute_runwayintrusion
            )

            # GenAv Runway Intrusion
            group.genav_arrival_runwayintrusion = items.filter(runway_incursion__icontains="GenAv Arrival yes").count()
            group.genav_departure_runwayintrusion = items.filter(runway_incursion__icontains="GenAv Departure yes").count()
            group.genav_enroute_runwayintrusion = items.filter(runway_incursion__icontains="GenAv Enroute yes").count()
            group.genav_runwayintrusion_total = (
                group.genav_arrival_runwayintrusion +
                group.genav_departure_runwayintrusion +
                group.genav_enroute_runwayintrusion
            )

            # Military Runway Intrusion
            group.military_arrival_runwayintrusion = items.filter(runway_incursion__icontains="Military Arrival yes").count()
            group.military_departure_runwayintrusion = items.filter(runway_incursion__icontains="Military Departure yes").count()
            group.military_enroute_runwayintrusion = items.filter(runway_incursion__icontains="Military Enroute yes").count()
            group.military_runwayintrusion_total = (
                group.military_arrival_runwayintrusion +
                group.military_departure_runwayintrusion +
                group.military_enroute_runwayintrusion
            )

            # Total Runway Intrusion
            group.arrival_total_runwayintrusion = group.commercial_arrival_runwayintrusion + group.genav_arrival_runwayintrusion + group.military_arrival_runwayintrusion
            group.departure_total_runwayintrusion = group.commercial_departure_runwayintrusion + group.genav_departure_runwayintrusion + group.military_departure_runwayintrusion
            group.enroute_total_runwayintrusion = group.commercial_enroute_runwayintrusion + group.genav_enroute_runwayintrusion + group.military_enroute_runwayintrusion
            group.runwayintrusion_overall_total = group.arrival_total_runwayintrusion + group.departure_total_runwayintrusion + group.enroute_total_runwayintrusion

            # GenAv Arrival Statistics
            group.private_arrival = items.filter(genav_detail__icontains="Arrival Private").count()
            group.cargo_arrival = items.filter(genav_detail__icontains="Arrival Cargo").count()
            group.medevac_arrival = items.filter(genav_detail__icontains="Arrival Med Evac").count()
            group.utility_arrival = items.filter(genav_detail__icontains="Arrival Utility/Maintenance").count()
            group.training_arrival = items.filter(genav_detail__icontains="Arrival Training").count()
            group.government_arrival = items.filter(genav_detail__icontains="Arrival Government").count()

            group.genav_arrival_total = (
                group.private_arrival +
                group.cargo_arrival +
                group.medevac_arrival +
                group.utility_arrival +
                group.training_arrival +
                group.government_arrival
            )

            # GenAv Departure Statistics
            group.private_departure = items.filter(genav_detail__icontains="Departure Private").count()
            group.cargo_departure = items.filter(genav_detail__icontains="Departure Cargo").count()
            group.medevac_departure = items.filter(genav_detail__icontains="Departure Med Evac").count()
            group.utility_departure = items.filter(genav_detail__icontains="Departure Utility/Maintenance").count()
            group.training_departure = items.filter(genav_detail__icontains="Departure Training").count()
            group.government_departure = items.filter(genav_detail__icontains="Departure Government").count()

            group.genav_departure_total = (
                group.private_departure +
                group.cargo_departure +
                group.medevac_departure +
                group.utility_departure +
                group.training_departure +
                group.government_departure
            )

            # GenAv Enroute Statistics
            group.private_enroute = items.filter(genav_detail__icontains="Enroute Private").count()
            group.cargo_enroute = items.filter(genav_detail__icontains="Enroute Cargo").count()
            group.medevac_enroute = items.filter(genav_detail__icontains="Enroute Med Evac").count()
            group.utility_enroute = items.filter(genav_detail__icontains="Enroute Utility/Maintenance").count()
            group.training_enroute = items.filter(genav_detail__icontains="Enroute Training").count()
            group.government_enroute = items.filter(genav_detail__icontains="Enroute Government").count()

            group.genav_enroute_total = (
                group.private_enroute +
                group.cargo_enroute +
                group.medevac_enroute +
                group.utility_enroute +
                group.training_enroute +
                group.government_enroute
            )

            # GenAv Totals for Each Category
            group.genav_private_total = (
                group.private_arrival +
                group.private_departure +
                group.private_enroute
            )
            group.genav_cargo_total = (
                group.cargo_arrival +
                group.cargo_departure +
                group.cargo_enroute
            )
            group.genav_medevac_total = (
                group.medevac_arrival +
                group.medevac_departure +
                group.medevac_enroute
            )
            group.genav_utility_total = (
                group.utility_arrival +
                group.utility_departure +
                group.utility_enroute
            )
            group.genav_training_total = (
                group.training_arrival +
                group.training_departure +
                group.training_enroute
            )
            group.genav_government_total = (
                group.government_arrival +
                group.government_departure +
                group.government_enroute
            )

            # Grand Total for GenAv
            group.genav_overall_total = (
                group.genav_arrival_total +
                group.genav_departure_total +
                group.genav_enroute_total
            )

    return render(request, 'main_site/archived_list.html', {'archive': archive})


@login_required
def archive_clear_view(request):
    if request.method == "POST":
        Items.objects.filter(archive_group__isnull=False).delete()
        ArchiveGroup.objects.all().delete()
        return redirect('archive_view')
    return render(request, 'main_site/clear_archive.html')


@login_required
def archive_delete_view(request, group_id):
    group = ArchiveGroup.objects.get(id=group_id)
    group.items_set.all().delete()
    group.delete()    
    return redirect('archive_view')  
