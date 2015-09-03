from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    # def get_user(self, user_id):
    #     """ Get a User object from the user_id. """
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None

        # if not remote_user:
        #     return
        # user = None
        # username = self.clean_username(remote_user)
        #
        # UserModel = get_user_model()
        #
        # # Note that this could be accomplished in one try-except clause, but
        # # instead we use get_or_create when creating unknown users since it has
        # # built-in safeguards for multiple threads.
        # if self.create_unknown_user:
        #     user, created = UserModel._default_manager.get_or_create(**{
        #         UserModel.USERNAME_FIELD: username
        #     })
        #     if created:
        #         user = self.configure_user(user)
        # else:
        #     try:
        #         user = UserModel._default_manager.get_by_natural_key(username)
        #     except UserModel.DoesNotExist:
        #         pass
        # return user
