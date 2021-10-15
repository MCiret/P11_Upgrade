from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
import account.manage_used_pwd as mup


class UserCreateForm(auth_forms.UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].help_text = ''

    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email',)


class UserChangeForm(auth_forms.UserChangeForm):

    class Meta(auth_forms.UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email',)


class UserPwdResetForm(auth_forms.SetPasswordForm):

    error_messages = {
        **auth_forms.SetPasswordForm.error_messages,
        'password_already_used': _("You already used this new password."),
        # see https://docs.djangoproject.com/fr/3.2/topics/i18n/translation/#localization-how-to-create-language-files
        # about how to add translated text to be used with this _() (alias gettext) function
    }

    def clean_new_password2(self):
        password2 = super().clean_new_password2()
        if mup.pwd_not_already_used(str(self.user.email), password2) == -1:
            raise auth_forms.ValidationError(
                self.error_messages['password_already_used'],
                code='pwd_used'
            )
        password_validation.validate_password(password2, self.user)
        return password2


class UserPwdChangeForm(UserPwdResetForm, auth_forms.PasswordChangeForm):
    pass



