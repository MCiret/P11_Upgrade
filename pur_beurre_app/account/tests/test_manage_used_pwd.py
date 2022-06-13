from django.test import TransactionTestCase
import filldb_tests_module.crud_functions_to_test as crud
import account.manage_used_pwd as mup
from account.models import UsedPassword


class ManageUsedPwdTests(TransactionTestCase):

    def setUp(self):
        self.user1 = crud.create_user("user1@gmail.com", "tata1234")
        crud.change_user_pwd(self.user1, "tete1234")
        crud.change_user_pwd(self.user1, "titi1234")

    def test_pwd_not_already_used(self):
        self.assertEqual(-1, mup.pwd_not_already_used("user1@gmail.com", "tata1234"))
        self.assertIsNone(mup.pwd_not_already_used("user1@gmail.com", "toto1234"))

    def test_save_used_pwd(self):
        mup.save_used_pwd(self.user1)
        self.assertQuerysetEqual(self.user1.usedpassword_set.all(),
                                 UsedPassword.objects.filter(user_id=self.user1.pk),
                                 ordered=False)
