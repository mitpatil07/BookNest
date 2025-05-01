from django.shortcuts import render, redirect, get_object_or_404
from Home.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings


@login_required(login_url='login')
def LandingPage(request):
    return render(request, 'LandingPage.html' )


@login_required(login_url='login')
def book_page(request):
    queryset=books_data.objects.all()
    data = {"data" : queryset}
    return render(request, 'books.html', context=data)


@login_required(login_url='login')
def add_to_cart(request, model_name, id):
    if model_name == 'books':
        book = get_object_or_404(books_data, id=id)
    elif model_name == 'story':
        book = get_object_or_404(story_book, id=id)
    elif model_name == 'history':
        book = get_object_or_404(History_book, id=id)
    else:
        return redirect('book_page')

    cart = request.session.get('cart', {})

    # Unique cart key
    book_key = f"{model_name}_{book.id}"

    if book_key in cart:
        cart[book_key] += 1
    else:
        cart[book_key] = 1

    request.session['cart'] = cart
    return redirect('cart_detail')

''''
@login_required(login_url='login')
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []

    if cart:
        for book_key, quantity in cart.items():
            try:
                model_name, book_id = book_key.split('_')
                book_id = int(book_id)

                if model_name == 'books':
                    book = books_data.objects.get(id=book_id)
                elif model_name == 'story':
                    book = story_book.objects.get(id=book_id)
                elif model_name == 'history':
                    book = History_book.objects.get(id=book_id)
                else:
                    continue

                cart_items.append({
                    'key': book_key,  # important for remove function later
                    'book': book,
                    'quantity': quantity,
                })
            except Exception:
                continue
    
    print(cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items})
'''
@login_required(login_url='login')
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []

    if cart:
        for book_key, quantity in cart.items():
            try:
                model_name, book_id = book_key.split('_')
                book_id = int(book_id)

                if model_name == 'books':
                    book = books_data.objects.get(id=book_id)
                    name = book.BookName
                    image = book.Bookimg.url if book.Bookimg else None
                elif model_name == 'story':
                    book = story_book.objects.get(id=book_id)
                    name = book.str_bookname
                    image = book.str_bookimg.url if book.str_bookimg else None
                elif model_name == 'history':
                    book = History_book.objects.get(id=book_id)
                    name = book.hstr_bookname
                    image = book.hstr_bookimg.url if book.hstr_bookimg else None
                else:
                    continue

                cart_items.append({
                    'key': book_key,
                    'book': book,
                    'quantity': quantity,
                    'display_name': name,
                    'display_image': image,
                })

            except (ValueError, books_data.DoesNotExist, story_book.DoesNotExist, History_book.DoesNotExist):
                continue

    print(cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required(login_url='login')
def remove_from_cart(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        del cart[key]

    request.session['cart'] = cart

    return redirect('cart_detail')


@login_required(login_url='login')
def story_books(request):
    queryset = story_book.objects.all() 
    context = {'story': queryset} 
    return render(request, 'booksPage2.html', context)

@login_required(login_url='login')
def history_books(request):
    queryset = History_book.objects.all()
    context = {"data": queryset}
    return render(request, 'bookPage3.html', context)

def login_page(request):
    if request.method == "POST":
        usernamea = request.POST.get("username", "").strip()
        passworda = request.POST.get("password", "").strip()

        # Check if username and password are provided
        if not usernamea or not passworda:
            messages.error(request, "Username and password cannot be empty.")
            return redirect('login')

        # Check if username exists
        if not User.objects.filter(username=usernamea).exists():
            messages.error(request, "Invalid Username")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=usernamea, password=passworda)
        if user is None:
            messages.error(request, "Invalid password")
            return redirect('login')

        # Login the user
        login(request, user=user)

        # Redirect based on user role (e.g., admin or regular user)
        if user.is_superuser:
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            return redirect('landing_page')  # Regular user landing page

    return render(request, "login.html")


def register_page(request):
    if request.method == "POST":
        namea = request.POST.get("name", "").strip()
        usernamea = request.POST.get("username", "").strip()
        emaila = request.POST.get("email", "").strip()
        passworda = request.POST.get("password", "").strip()

        # Ensure fields are not empty
        if not usernamea or not emaila or not passworda:
            messages.error(request, "All fields are required.")
            return redirect("register")

        # Check if username already exists
        if User.objects.filter(username=usernamea).exists():
            messages.error(request, "Username already exists. Try logging in.")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(email=emaila).exists():
            messages.error(request, "An account with this email already exists. Try logging in.")
            return redirect("register")

        # Check email validity
        try:
            validate_email(emaila)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return redirect("register")

        # Password validation
        if len(passworda) < 8 or not re.search(r"[A-Za-z]", passworda) or not re.search(r"\d", passworda):
            messages.error(request, "Password must be at least 8 characters long and contain both letters and numbers.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=usernamea,
            email=emaila,
            password=passworda
        )
        user.first_name = namea
        user.save()

        messages.success(request, "User Registration Success!!")
        return redirect("login")

    return render(request, "register.html")


def logout_page(request):
    logout(request)
    messages.success(request, "Logged Out!!")
    return redirect("login")

@login_required(login_url='login')
def about_page(request):
    return render(request, 'about.html')

# Modify the search suggestions view to include book type in the response
@login_required(login_url='login')
def search_suggestions(request):
    query = request.GET.get('query', '').strip()
    suggestions = []

    if query:
        # You can adjust the search logic to match any of your book fields
        books = books_data.objects.filter(BookName__icontains=query)[:10]
        story_books = story_book.objects.filter(str_bookname__icontains=query)[:10]
        history_books = History_book.objects.filter(hstr_bookname__icontains=query)[:10]

        # Collect book names as suggestions with book type
        for book in books:
            suggestions.append({
                'id': book.id,
                'name': book.BookName,
                'type': 'books_data'
            })
        for book in story_books:
            suggestions.append({
                'id': book.id,
                'name': book.str_bookname,
                'type': 'story_book'
            })
        for book in history_books:
            suggestions.append({
                'id': book.id,
                'name': book.hstr_bookname,
                'type': 'History_book'
            })

    return JsonResponse({'suggestions': suggestions})



def get_book_details(request):
    book_id = request.GET.get('book_id')
    book_type = request.GET.get('book_type')

    if book_type == 'books_data':
        book = get_object_or_404(books_data, id=book_id)
        response_data = {
            'name': book.BookName,
            'image_url': book.Bookimg.url if book.Bookimg else None,
            'description': book.BookInfo,
            'detail_url': book.get_absolute_url()  # Assuming you have a detail page
        }
    elif book_type == 'story_book':
        book = get_object_or_404(story_book, id=book_id)
        response_data = {
            'name': book.str_bookname,
            'image_url': book.str_bookimg.url if book.str_bookimg else None,
            'description': book.str_bookdsc,
            'detail_url': book.get_absolute_url()  # Assuming you have a detail page
        }
    elif book_type == 'History_book':
        book = get_object_or_404(History_book, id=book_id)
        response_data = {
            'name': book.hstr_bookname,
            'image_url': book.hstr_bookimg.url if book.hstr_bookimg else None,
            'description': book.hstr_bookdsc,
            'detail_url': book.get_absolute_url()  # Assuming you have a detail page
        }
    else:
        return JsonResponse({'error': 'Invalid book type'}, status=400)

    return JsonResponse(response_data)

@login_required(login_url='login')
def send_bill_email(request):
    user = request.user  # assuming user is logged in
    cart = request.session.get('cart', {})

    book_list = ""

    if cart:
        for book_key, quantity in cart.items():
            try:
                model_name, book_id = book_key.split('_')
                book_id = int(book_id)

                if model_name == 'books':
                    book = books_data.objects.get(id=book_id)
                    name = book.BookName
                elif model_name == 'story':
                    book = story_book.objects.get(id=book_id)
                    name = book.str_bookname
                elif model_name == 'history':
                    book = History_book.objects.get(id=book_id)
                    name = book.hstr_bookname
                else:
                    continue

                book_list += f"- {name} (x{quantity})\n"

            except Exception as e:
                print(e)
                continue

    subject = 'Your Book Purchase Bill 📚'
    message = f"Hello {user.first_name or user.username},\n\nThank you for shopping with us! Here are the books in your cart:\n\n{book_list}\n\nHappy Reading!\nTeam BookStore"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    messages.success(request, 'Bill sent to your email successfully! 📧')
    return redirect('cart_detail')