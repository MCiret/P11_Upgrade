import base64
from django.test import TestCase, RequestFactory
from unittest import mock
from django.urls import reverse
from django.core import mail
import filldb_tests_module.crud_functions_to_test as crud
from account.models import User
from account.views import UserAccountView
from account.forms import UserPwdChangeForm, UserPwdResetForm


class AccountViewsTests(TestCase):

    def test_user_create_view(self):
        # Test empty user creation form displaying :
        response_get = self.client.get(reverse('account:user-create'))
        self.assertTemplateUsed(response_get, "account/create-account.html")

        # Test successful user creation in db using the form :
        response_post = self.client.post(reverse('account:user-create'), {
                                         'email': 'user_test@mail.com',
                                         'password1': 'toto1598',
                                         'password2': 'toto1598'}, follow=True)

        # Test home page redirect when form is validated :
        self.assertTemplateUsed(response_post, "research/home.html")

        # Test user is in db :
        self.assertEqual(User.objects.get().email, 'user_test@mail.com')

        # Test failing user creation in db using the form :
        response_post2 = self.client.post(reverse('account:user-create'), {
                                          'email': 'user_test@mail.com',
                                          'password1': 'toto1598',
                                          'password2': 'toto159'})
        # Test user create page is redisplayed if form is not validated :
        self.assertTemplateUsed(response_post2, "account/create-account.html")

    def test_user_login_view(self):
        # Test empty user login form displaying :
        response_get = self.client.get(reverse('account:user-login'))
        self.assertTemplateUsed(response_get, "account/login-account.html")
        self.assertContains(response_get, "Mot de passe oublié ?")

        # Test successful user login :
        crud.create_user('user_test@mail.com', 'tutu3574')
        response_post = self.client.post(reverse('account:user-login'), {
                                         'username': 'user_test@mail.com',
                                         'password': 'tutu3574', 'next': '/'}, follow=True)
        # the 'next' value is set in the form (see hidden input in the html template)
        # and not in the view so it has to be passed with post params
        # (like the username and password field values)

        # Test home page redirect when form is validated and user is logged :
        self.assertTemplateUsed(response_post, "research/home.html")

        # Test failing user login :
        response_post2 = self.client.post(reverse('account:user-login'), {
                                          'username': 'user_test@mail.com',
                                          'password': 'tutu357'})
        # Test user login page is redisplayed if form is not validated :
        self.assertTemplateUsed(response_post2, "account/login-account.html")

    def test_extract_user_name_from_mail(self):
        self.assertEqual(UserAccountView.extract_user_name_from_mail("abcde@mail.fr"), "abcde")

    @mock.patch('account.views.UserAccountView.extract_user_name_from_mail')
    def test_user_account_view(self, mock_extract):

        mock_extract.return_value = "user_test"

        # Test redirection to login page if user is not logged
        response_user_not_logged = self.client.get(reverse('account:user-account'), follow=True)
        self.assertTemplateUsed(response_user_not_logged, "account/login-account.html")

        # Test display user's account page if he is logged
        crud.create_user("user_test@gmail.com", "titi6789")
        self.client.login(username="user_test@gmail.com", password="titi6789")

        response_user_logged = self.client.get(reverse('account:user-account'))

        self.assertTrue(mock_extract.called)
        self.assertTemplateUsed(response_user_logged, "account/user-account.html")
        self.assertContains(response_user_logged, "user_test !", status_code=200)
        self.assertContains(response_user_logged, "user_test@gmail.com", status_code=200)
        self.assertContains(response_user_logged,
                            '<input type="password" name="old_password"')
        self.assertIsInstance(response_user_logged.context['form'], UserPwdChangeForm)

    def test_view_user_change_pwd_using_an_already_used_pwd(self):

        crud.create_user("user_test@gmail.com", "titi6789")
        self.client.login(username="user_test@gmail.com", password="titi6789")

        response_user_logged = self.client.get(reverse('account:user-account'))
        # Test modify password twice but try to re-use the same
        self.client.post(reverse('account:user-account'), {
                                 'old_password': 'titi6789',
                                 'new_password1': 'tutu1357',
                                 'new_password2': 'tutu1357'
                                })
        # Test change pwd with an allowed one (not already used) :
        self.assertTemplateUsed(response_user_logged, "account/user-account.html")
        self.assertNotContains(response_user_logged, "Vous avez déjà utilisé ce mot de passe.", status_code=200)

        # Test change pwd with a NOT allowed one (already used) :
        response_user_logged = self.client.post(reverse('account:user-account'), {
                                                        'old_password': 'tutu1357',
                                                        'new_password1': 'titi6789',
                                                        'new_password2': 'titi6789'
                                                        })
        self.assertTemplateUsed(response_user_logged, "account/user-account.html")
        self.assertContains(response_user_logged, "Vous avez déjà utilisé ce mot de passe.", status_code=200)

    def test_view_user_reset_pwd(self):

        crud.create_user("user_test@gmail.com", "titi6789")
        response = self.client.get(reverse('account:pwdreset'))
        self.assertTemplateUsed(response, "account/pwdreset-account.html")

        # Test if pwdresetdone-account.html is well displayed after email input :
        response = self.client.post(reverse('account:pwdreset'), {
                                            'email': 'user_test@gmail.com',
                                            }, follow=True)
        self.assertTemplateUsed(response, "account/pwdresetdone-account.html")

        # Test that pwdresetemail-account.html is not send as email if email input does not exist in db :
        response = self.client.post(reverse('account:pwdreset'), {
                                            'email': 'user_test2@gmail.com',
                                            })
        self.assertTemplateNotUsed(response, "account/pwdresetemail-account.html")

        # Test if pwdresetemail-account.html is well send as email :
        response = self.client.post(reverse('account:pwdreset'), {
                                            'email': 'user_test@gmail.com',
                                            })
        user_token = response.context['token']
        user_uid = response.context['uid']
        self.assertTemplateUsed(response, "account/pwdresetemail-account.html")

        # Test when user follow the link received by email to display the pwd reset form :
        resp_get = self.client.get(reverse('account:pwdresetlink',
                                kwargs = {
                                    'uidb64': user_uid,
                                    'token': user_token,
                                }), follow=True)
        self.assertTemplateUsed(resp_get, "account/pwdresetconfirm-account.html")

        resp_post = self.client.post(reverse('account:pwdresetlink',
                                             kwargs = {'uidb64': user_uid,
                                                       'token': 'set-password'}),
                                     {'new_password1': "tktk1598",
                                      'new_password2': "tktk1598"},
                                     follow=True)
        self.assertTemplateUsed(resp_post, "account/pwdresetcomplete-account.html")
        self.assertTrue(self.client.login(username="user_test@gmail.com", password="tktk1598"))


    def test_user_logout_view(self):
        crud.create_user("user_test@gmail.com", "titi6789")
        self.client.login(username="user_test@gmail.com", password="titi6789")

        response_user_to_log_out = self.client.get(reverse('account:user-logout'), follow=True)

        # Test redirection to home page when user logs out :
        self.assertTemplateUsed(response_user_to_log_out, "research/home.html")
        # Test redirected home page is well displayed with menu for an unlogged user :
        self.assertNotContains(response_user_to_log_out, "href=/accounts/logout")
        self.assertContains(response_user_to_log_out, "href=/accounts/create/")
