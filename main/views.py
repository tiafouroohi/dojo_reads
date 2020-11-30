from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,Review,Book,Author
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        for message in error.values():
            messages.error(request, message)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(request.POST['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password= pw_hash
    )
    request.session['user_id'] = new_user.id
    return redirect('/success')

def login(request):
    error = User.objects.login_validator(request.POST)
    if len(error) > 0:
        for message in error.values():
            messages.error(request, message)
        return redirect('/')
    list_of_users = User.objects.filter(email=request.POST['email'])
    if len(list_of_users) > 0:
        user = list_of_users[0]
        if bcrypt.checkpw(request.POST['password'].encode("utf-8"), user.password.encode("utf-8")):
            request.session['user_id'] = user.id
            return redirect('/success')
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    print(logged_in_user.__dict__)
    context = {
        'logged_in_user': logged_in_user
    }
    return render(request, "success.html", context)

def user(request):
    if 'user_id' not in request.session:
        return redirect
    user_id=request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        'user' : user,
        'all_book': Book.objects.all()
    }
    return render(request, "user.html", context)

def add_a_book(request):
    return render(request, "add_a_book.html")

def new_books(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    new_author = Author.objects.create(name=request.POST['new_author'])
    new_book = Book.objects.create(
        title=request.POST['title'],
        author=new_author,
        submitted_by= logged_in_user
    )
    new_review = Review.objects.create(
        content=request.POST['review_content'],
        rating=request.POST['review_rating'],
        reviewed_book=request.POST['new_book'],
        user_reviewing_book=request.POST['logged_in_user']

    )

    return redirect('/books_reviewed')

def books_reviewed(request):
   all_book = Book.objects.all()
   context = {
       'all_book': all_book,
   }
   print(request.POST)
   return render(request, "books_reviewed.html", context)

def individual_book(request, book_id):
    context = {
     'book' :Book.objects.get(id=book_id)   
    }
    
    return render(request, "individual_book.html", context)

def add_review(request):
    pass

def user_reviews(request):
    return render(request, "user_reviews.html")










def logout(request):
    request.session.clear()
    return redirect('/')




# Create your views here.
