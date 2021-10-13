from django.views.generic import CreateView
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.urls import reverse_lazy

from account.forms import UserCreateForm, UserPwdChangeForm, UserPwdResetForm
from account.models import User


class UserCreateView(CreateView):
    model = User  # this model has a get_absolute_url method which redirect user when account is well created
    template_name = 'account/create-account.html'
    form_class = UserCreateForm


class UserLoginView(LoginView):
    template_name = 'account/login-account.html'


class UserAccountView(PasswordChangeView):
    """ This view diplays the user's account e-mail and a form to change the password."""

    template_name = 'account/user-account.html'
    success_url = reverse_lazy('account:user-account')
    form_class = UserPwdChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = UserAccountView.extract_user_name_from_mail(str(self.request.user))
        context['user_mail'] = self.request.user
        return context

    @staticmethod
    def extract_user_name_from_mail(mail: str):
        return mail[:mail.find('@')]


class PwdResetView(PasswordResetView):
    """ User enter his email to receive the link to reset his password."""
    template_name = 'account/pwdreset-account.html'
    email_template_name = 'account/pwdresetemail-account.html'
    success_url = reverse_lazy('account:pwdresetdone')


class PwdResetDoneView(PasswordResetDoneView):
    """ Email with a link to reset his password has been sent to the user."""
    template_name = 'account/pwdresetdone-account.html'


class PwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/pwdresetconfirm-account.html'
    success_url = reverse_lazy('account:pwdresetcomplete')
    form_class = UserPwdResetForm


class PwdResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/pwdresetcomplete-account.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('research:home-page')
    # class attributes are evaluated on import that's why we use reverse_lazy() instead of reverse()
