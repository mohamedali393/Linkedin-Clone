from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        UserModel = get_user_model()

        if username is None:
            username = kwargs.get('email')

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and user.is_active:
            return user

        return None