from django.shortcuts import render, HttpResponse
from django.db import connection
from accounts.models import Account

# Create your views here.

def account(request):
    return render(request, 'profile.html')

def account_edit(request):
    user = request.user
    profile = request.user.profile

    instance = request.user.profile
    form = UserForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'account_edit.html', {'form': form})
