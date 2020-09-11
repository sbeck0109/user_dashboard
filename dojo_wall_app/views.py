from django.shortcuts import render, redirect
from django.contrib import messages
from dojo_wall_app.models import User, Message, Comment
import bcrypt

# Create your views here.
def welcome(request):
  return render(request,"welcome.html")

def loginReg(request):
  return render(request, "loginReg.html")

def process_reg(request):
  errors = User.objects.register_validator(request.POST)
  if len(errors) > 0:
    for key, error_msg in errors.items():
      messages.error(request, error_msg)
    return redirect('/signin')
  first_name = request.POST['first_name']
  last_name = request.POST['last_name']
  email = request.POST['email']
  password = request.POST['password']
  pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  print(f"pw hash: {pw_hash}")
  new_user = User.objects.create(first_name=first_name, last_name=last_name,email=email, password=pw_hash)
  request.session['user_id'] = new_user.id
  messages.success(request, "Successfully registered!")
  if new_user.id == 1:
    new_user.level = 9
    new_user.level.save()
  return redirect("/signin")

def process_login(request):
  errors = User.objects.login_validator(request.POST)
  if len(errors) > 0:
    for key, error_msg in errors.items():
      messages.error(request, error_msg)
    return redirect('/signin')
  login_user_list = User.objects.filter(email=request.POST['email'])
  if login_user_list:
    this_user = login_user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
      request.session['user_id'] = this_user.id
      messages.success(request, "successfully logged in!")
      return redirect('dashboard:my_index')
  else:
    messages.error(request, "Password did not match")
  return redirect('/signin')

def delete_message(request, message_id, user_id):
  if 'user_id' not in request.session:
    return redirect('/signin')
  else:
    this_message=Message.objects.get(id=message_id)
    this_user = User.objects.get(id=request.session['user_id'])
    print('*************************', this_user)
    user = User.objects.get(id=user_id)

    if this_user.id == this_message.user_id:
      delete_this_message = Message.objects.get(id = message_id)
      print("*****************", delete_this_message)
      delete_this_message.delete()
      return redirect(f'/index/{user.id}')
# def delete_comment(request, comment_id, message_id):
#   if 'user_id' not in request.session:
#     return redirect('/')
#   else:

#     this_message=Message.objects.get(id=message_id)
#     this_comment=Comment.objects.get(id=comment_id)
#     this_user = User.objects.get(id=request.session['user_id'])
#     if this_user.id == this_message.comments.user_id:
#       delete_this_comment = Comment.objects.get(id = this_message.comments.comment_id)
#       delete_this_comment.delete()
#       return redirect('/index')

def log_out(request):
  request.session.flush()
  messages.success(request, "successfully logged out!")
  return redirect('/signin')


def index(request, user_id):
  if 'user_id' not in request.session:
    return redirect('/signin')
  user = User.objects.get(id = user_id)
  logged_in_user = User.objects.get(id=request.session['user_id'])
  all_messages = Message.objects.all()
  all_users = User.objects.all()
  print("************user is ", user)
  context = {

    "all_messages" : all_messages,
    "all_users" : all_users,
    "user" : user,
    "logged_in_user" : logged_in_user

  }
  return render (request, "wall_index.html", context)


def new_message(request, user_id):
  errors = Message.objects.message_validator(request.POST)
  if len(errors) > 0:
    for key, error_msg in errors.items():
      messages.error(request, error_msg)
    return redirect(f'/index/{user.id}')
  logged_in_user = User.objects.get(id=request.session['user_id'])
  message = request.POST['message']
  user = User.objects.get(id = user_id)
  Message.objects.create(message=message, user=logged_in_user)
  return redirect(f"/index/{user.id}")

def display_new_message(request, user_id):
  user = User.objects.get(id=user_id)
  logged_in_user_id=request.session['user_id']
  logged_in_user=User.objects.get(id=logged_in_user_id)
  print("logged in user is: ", logged_in_user.first_name)
  all_messages = Message.objects.all()
  all_users = User.objects.all()
  all_comments = Comment.objects.all()
  context = {
    "user" : user,
    "logged_in_user" : logged_in_user,
    "all_messages" : all_messages,
    "all_users" : all_users,
    "all_comments" : all_comments
  }
  return render(request, "wall.html", context)

def new_comment(request):
  errors = Comment.objects.comment_validator(request.POST)
  if len(errors) > 0:
    for key, error_msg in errors.items():
      messages.error(request, error_msg)
    return redirect('/index')
  user_id = request.session['user_id']
  print(f"************ user_id is: {user_id}")
  user = User.objects.get(id=user_id)
  comment = request.POST['comment']
  message_id = request.POST['message_id']
  print(message_id)
  this_message = Message.objects.get(id=message_id)
  new_comment = Comment.objects.create(
      comment=comment, user=user, message=this_message)
  return redirect(f"/wall/{user}")
