from django.urls import path

from account.views import (UserCreateView, UserLoginView, UserAccountView, UserLogoutView,
                           PwdResetView, PwdResetDoneView, PwdResetConfirmView, PwdResetCompleteView)

app_name = 'account'

urlpatterns = [
    path('accounts/create/', UserCreateView.as_view(), name="user-create"),
    path('accounts/login/', UserLoginView.as_view(), name="user-login"),
    path('accounts/account/', UserAccountView.as_view(), name="user-account"),
    path('accounts/pwdreset/', PwdResetView.as_view(), name="pwdreset"),
    path('accounts/pwdresetdone/', PwdResetDoneView.as_view(), name="pwdresetdone"),
    path('accounts/pwdresetconfirm/<uidb64>/<token>', PwdResetConfirmView.as_view(), name="pwdresetlink"),
    path('accounts/pwdresetconfirm/', PwdResetConfirmView.as_view(), name="pwdresetform"),
    path('accounts/pwdresetcomplete/', PwdResetCompleteView.as_view(), name="pwdresetcomplete"),
    path('accounts/logout/', UserLogoutView.as_view(), name="user-logout"),
]
