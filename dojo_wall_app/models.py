from django.db import models
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
  def register_validator(self, postData):
    errors = {}
    #first_name
    if len(postData['first_name']) < 2:
      errors['first_name'] = "First name should be 2 or more letters."
    if len(postData["first_name"]) >= 2 and not postData['first_name'].isalpha():
      errors['first_name'] = "must only contain letters."
    #last_name
    if len(postData['last_name']) < 2:
      errors['last_name'] = "Last name should be 2 or more letters."
    if len(postData['last_name']) >= 2 and not postData['last_name'].isalpha():
      errors['last_name'] = "must only contain letters."
    #email
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    check_email = User.objects.filter(email=postData['email'])
    if check_email:
      errors['email'] = "Email already in use."
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "Invalid email address format."
    #password
    if len(postData['password']) < 8:
      errors['pass_length'] = "Your password must be 8 or more characters."
    if postData['password'] != postData['confirm_password']:
      errors['pass_confirm'] = "passwords need to match, fix now."
    return errors
  def login_validator(self, postData):
    errors = {}
    user = User.objects.filter(email=postData['email'])
    if user:
      our_user = user[0]
      if bcrypt.checkpw(postData['password'].encode(), our_user.password.encode()):
        #return empty dict
        return errors
      errors['no_pass'] = "Incorrect password given bud."
      return errors
    errors['no_email'] = "No emails match that query."
    return errors
    if len(postData['password']) < 8:
      errors['password'] = "password needs to be 8 or more characters."
    return errors
  def edit_validator(self, postData):
    errors = {}
    #first_name
    if len(postData['first_name']) < 2:
      errors['first_name'] = "First name should be 2 or more letters."
    if len(postData["first_name"]) >= 2 and not postData['first_name'].isalpha():
      errors['first_name'] = "must only contain letters."
    #last_name
    if len(postData['last_name']) < 2:
      errors['last_name'] = "Last name should be 2 or more letters."
    if len(postData['last_name']) >= 2 and not postData['last_name'].isalpha():
      errors['last_name'] = "must only contain letters."
    #email
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    check_email = User.objects.filter(email=postData['email'])
    if not EMAIL_REGEX.match(postData['email']):
      errors['email'] = "Invalid email address format."
    if len(postData['description']) < 1:
      errors['last_name'] = "Description should be 1 or more letter."
    return errors

class MessageManager(models.Manager):
  def message_validator(self, postData):
    errors = {}
    #message
    if len(postData['message']) < 1:
      errors['message'] = "Message must contain 1 or more letters."
    return errors
class CommentManager(models.Manager):
  def comment_validator(self, postData):
    errors = {}
    #message
    if len(postData['comment']) < 1:
      errors['message'] = "Comment must contain 1 or more letters."
    return errors


class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.CharField(max_length=45, blank=False, unique=True)
  password = models.CharField(max_length=45)
  description = models.CharField(max_length=255, null=True)
  level = models.CharField(max_length=45, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()


class Message(models.Model):
  message = models.CharField(max_length=255)
  user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = MessageManager()

class Comment(models.Model):
  comment = models.CharField(max_length=255)
  user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
  message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = CommentManager()
