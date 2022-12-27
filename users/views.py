from account.auth_backends import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from users.forms import CodeForm
from users.tasks import send_code_to_email


def auth_view(request):
    """
    Представление входа
    """
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify_view')
    return render(request, 'auth.html', {'form': form})


def verify_view(request):
    """
    Представление подтверждение входа паролем с почты
    """
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        email = user.email
        if not request.POST:
            send_code_to_email(code, email)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('/admin/')
            else:
                return redirect('login_view')
    return render(request, 'verify.html', {'form': form})

