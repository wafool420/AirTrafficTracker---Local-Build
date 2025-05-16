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
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
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
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials"
    return render(request, 'accounts/login.html', {'error':error_message})

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
            item = form.save()
            item.user = request.user
            form.save()
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
    form = ItemForm(instance=item)
    if request.method == 'POST':
        form = ItemForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('items')
    return render(request, 'main_site/item_edit_form.html', {'form': form})

@login_required
def archive_dataset_view(request):
    if request.method == "POST":
        group = ArchiveGroup.objects.create()
        Items.objects.filter(archive_group__isnull=True).update(archive_group=group)
        return redirect('items')  
    elif request.method == "GET":
        return render(request, 'main_site/archive.html')
    return redirect('items')

def archive_view(request):
    if request.method == "GET":
        archive = ArchiveGroup.objects.all().order_by('-id')

        for group in archive:
            items = group.items_set.all()
            group.fixed_wing_count = items.filter(detail="Fixed Wing").count()
            group.helicopter_count = items.filter(detail="Helicopter").count()
            group.arrival_count = items.filter(action="Arrival").count()
            group.departure_count = items.filter(action="Departure").count()
            group.enroute_count = items.filter(action="Enroute").count()
            group.delayed_count = items.filter(timeliness="Delayed").count()
            group.ontime_count = items.filter(timeliness="On Time").count()
            group.na_count = items.filter(timeliness="N/A").count()

        return render(request, 'main_site/archived_list.html', {'archive': archive})

@login_required
def archive_clear_view(request):
    if request.method == "POST":
        Items.objects.filter(archive_group__isnull=False).delete()
        ArchiveGroup.objects.all().delete()

        return redirect('archive_view')  
    elif request.method == "GET":
        return render(request, 'main_site/clear_archive.html')

@login_required
def archive_delete_group_view(request, group_id):
    group = ArchiveGroup.objects.get(id=group_id)
    group.items_set.all().delete()
    group.delete()
    return redirect('archive_view')  


