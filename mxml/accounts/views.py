import random
import requests

from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.conf import settings
from .models import SocialUser


# Create your views here.

def log_out(request):
    logout(request)
    return redirect('/')

def github_login(request):
    auth_url = 'https://github.com/login/oauth/authorize'
    client_id = settings.GITHUB_AUTH_CLIENT_ID

    state = str(random.randint(0,10000))
    request.session['github_auth_state'] = state 

    return redirect('%s?client_id=%s&state=%s' % (auth_url, client_id, state))

def github_auth(request):
    code = request.GET['code']
    status = request.GET['state']

    if status != request.session['github_auth_state']:
        raise PermissionDenied
    
    payload = {
        'code': code,
        'client_id': settings.GITHUB_AUTH_CLIENT_ID,
        'client_secret': settings.GITHUB_AUTH_CLIENT_SECRET
    }
    headers = {'Accept': 'application/json'}
    r = requests.post('https://github.com/login/oauth/access_token', data=payload, headers=headers)

    payload = {
        'access_token': r.json()['access_token']
    }
    r = requests.get('https://api.github.com/user', params=payload)

    if r.status_code != 200:
        raise Http404("Github user not avaliable.")

    user_info = r.json()
    social_user = list(SocialUser.objects.filter(github_id=user_info['id']))

    if not isinstance(user_info['name'], str):
        user_info['name'] = user_info['login']

    if len(social_user) == 0:
        new_user = User.objects.create_user(user_info['login'])
        social_user = SocialUser(
            user=new_user,
            github_id=user_info['id'],
            github_login=user_info['login'],
            github_name=user_info['name'],
            github_avatar=user_info['avatar_url']
        )
        user = new_user
    else:
        social_user = social_user[0]
        social_user.github_login = user_info['login']
        social_user.github_name=user_info['name']
        social_user.github_avatar=user_info['avatar_url']
        user = social_user.user

    login(request, user)

    if isinstance(user_info['email'], str):
        user.email = user_info['email']
    user.save()
    social_user.save()
    return redirect('/')