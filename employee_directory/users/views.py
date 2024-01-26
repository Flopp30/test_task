from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User


# TODO удалить
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
#     else:
#         form = UserLoginForm()
#         context = {'form': form}
#         return render(request, '.signing/login.html', context)


class LoginView(DjangoLoginView):
    form_class = UserLoginForm
    template_name = '.signing/login.html'
    success_url = settings.LOGIN_REDIRECT_URL


# TODO удалить :)
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(settings.LOGIN_URL)
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, '.signing/register.html', context)


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = '.signing/register.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # авторизуем пользователя после успешной регистрации
        return response


# TODO удалить :)
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(settings.LOGIN_URL)
class LogoutView(DjangoLogoutView):
    ...
