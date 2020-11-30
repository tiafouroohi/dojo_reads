from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"
        if len(post_data['email']) < 8:
            errors['length_email'] = "Email must be at least 8 characters long"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Invalid Email. Please try again"
        if len(post_data['password']) < 8:
            errors['length_password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['confirm_password']:
            errors['invalid_password'] = "Password and confirm doesn't match"
        return errors
    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['email']) < 8:
            errors['email_length'] = "Email must be at least 8 characters long"
        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Invalid email. Please try again"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager ()
    def __repr__(self):
        return f'{self.first_name}-{self.last_name}-{self.email}-'

class Author(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Book(models.Model):
    title = models.CharField(max_length=20)
    submitted_by = models.ForeignKey(User, related_name="submitted_books", on_delete=models.CASCADE)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    user_adding_book = models.ManyToManyField(User, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.CharField(max_length=20)
    rating = models.IntegerField()
    user_reviewing_book = models.ForeignKey(User, related_name="user_reviews", on_delete=models.CASCADE)
    reviewed_book = models.ForeignKey(Book, related_name="book_reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
