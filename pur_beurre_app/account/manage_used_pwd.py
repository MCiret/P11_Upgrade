from account.models import User, UsedPassword
from django.contrib.auth.hashers import check_password


def pwd_not_already_used(user_email: str, new_pwd: str):
    """
    Tests if a password (param new_pwd) has been already used
    by the user corresponding to the param user_email.
    Returns -1 if the password can't be re-used because it has already been,
    else saves the new password in the database.
    """
    user = User.objects.get(email=user_email)
    user_used_pwd = user.usedpassword_set.all()
    for elem in user_used_pwd:
        if check_password(new_pwd, elem.pwd):
            return -1
    save_used_pwd(user)


def save_used_pwd(user: User):
    """
    Creates an UsedPassword object and inserts it in the database with the user_id as foreign key (see account.models).
    """
    used_pwd = UsedPassword(pwd=user.password, user=user)
    used_pwd.save()
