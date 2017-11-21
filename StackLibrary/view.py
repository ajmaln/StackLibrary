from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.base import View

from StackLibrary import settings


class IntroView(View):
    template_name = 'intro.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                return render(request, self.template_name, {'user_disabled': 'You are blocked'})
        else:
            return render(request, self.template_name, {'no_user': 'User does not exist'})

