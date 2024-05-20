from django.contrib.auth.base_user import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email must be set')
        if not password:
            raise ValueError('Password must be set')

        email = self.normalize_email(email=email)
        account = self.model(email=email, password=password, **kwargs)
        account.set_password(account.password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        from courseoutline.models import Account
        kwargs.setdefault('is_approved', True)
        kwargs.setdefault('role', Account.Role.ADMIN)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **kwargs)
