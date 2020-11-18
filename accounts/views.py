import tempfile
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

# from .models import Users, UserRoles
# from .forms import UserRegistrationForm
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.db import connections

# from passlib.hash import pbkdf2_sha256


LOG_FORMAT = "%(Levelname)s:%(asctime)s:%(message)s"
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


# def operator_reg(request):

#     return render(request, 'accounts/operator_reg.html')


# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password'] == request.POST['confirm-password']:
#             try:
#                 user = User.objects.get(username=request.POST['username'])
#                 return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})
#             except User.DoesNotExist:
#                 user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
#                 auth.login(request,user)
#                 return redirect('/')
#         else:
#              return render(request, 'accounts/signup.html', {'error':'Password must match'})


#     else:
#         return render(request, 'accounts/signup.html')


# def register_done(request):
#     if request.method == 'POST':
#         if request.POST['password'] == request.POST['confirm-password']:
#             if request.POST['username'] and request.POST['password']  and request.POST['firstname'] and request.POST['lastname'] and request.POST['status']  and request.POST['role']:
#                 username = request.POST['username']
#                 custom_pbkdf2 = pbkdf2_sha256.using(rounds=30000)
#                 password =  pbkdf2_sha256.hash(request.POST['password'])
#                 firstname = request.POST['firstname']
#                 lastname = request.POST['lastname']
#                 status = request.POST['status']
#                 role = request.POST['role']


#                 cursor = connections['default'].cursor()
#                 cursor.execute('INSERT INTO users(username, salted_hash, firstname, lastname, status, user_roles_id) VALUES (%s, %s, %s, %s, %s, %s)', [username, password, firstname, lastname, status, role])
#                 return render(request, 'accounts/register_done.html')
#             else:
#                 return render(request, 'accounts/operator_reg.html', {'error':'All fields are required'})
#         else:
#             return render(request, 'accounts/operator_reg.html', {'error':'Password must match'})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            logger.info('username or password is incorrect.')
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})

    else:
        logger.info('successfully login')
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        if request.session:
            messages.success(request, 'Successfully Logged Out')
        else:
            messages.error(request, 'Session Expired Please Login Again')
        auth.logout(request)
        logger.info('logout successfully')
        return redirect('/')

    return render(request, 'accounts/login.html')
