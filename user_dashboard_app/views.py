from django.shortcuts import render, redirect
from django.contrib import messages
from dojo_wall_app.models import User

def index(request):
  user_id = request.session['user_id']
  this_user = User.objects.get(id=user_id)
  print("*************this user id is: ", this_user.id)
  all_users = User.objects.all()
  context = {
    "all_users" : all_users,
    "this_user" : this_user
  }
  if this_user.id == 2:
    return render(request, 'admin_index.html', context)
  return render(request,'index.html', context)


def edit(request, user_id):
  if 'user_id' not in request.session:
    return redirect('/')
  logged_user = request.session['user_id']
  print('********logged user is:', logged_user)
  this_user = User.objects.get(id=user_id)
  context = {
    "this_user" : this_user
  }

  if logged_user == 2:
    return render(request, 'admin_edit.html', context)
  return render(request, 'user_edit.html', context)

def update(request, user_id):
  if 'user_id' not in request.session:
    return redirect('/')
  errors = User.objects.edit_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
  if request.method == "POST":
    edit_this_user = User.objects.get(id=user_id)
    edit_this_user.first_name = request.POST['first_name']
    edit_this_user.last_name = request.POST['last_name']
    edit_this_user.email = request.POST['email']
    edit_this_user.description = request.POST['description']
    edit_this_user.level = request.POST['level']
    edit_this_user.save()
    messages.success(request, "User information successfully updated")
    return redirect('/dashboard')

def remove_user(request, user_id):
  if 'user_id' not in request.session:
    return redirect('/')

  user_to_remove = User.objects.get(id=user_id)
  user_to_remove.delete()
  return redirect('/dashboard')
