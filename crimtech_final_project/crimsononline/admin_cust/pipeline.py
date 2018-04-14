from django.conf import settings
from django.contrib.auth.models import Group

from social.exceptions import AuthFailed


def force_new_user(backend, user=None, *args, **kwargs):
    """
    Prevent social auth from associating multiple social accounts with
    the same crimsononline account.
    """
    if user:
        raise AuthFailed(backend,
                         'Please log out of admin before attempting a login')


def update_permissions(user, is_new=False, *args, **kwargs):
    """
    Make any new crimson account a part of the SOCIAL_AUTH_BASEUSER
    group (defined in settings.py) and mark as staff.
    """
    if is_new:
        user.groups.add(Group.objects.get(name=settings.SOCIAL_AUTH_BASEUSER))
        user.is_active = True
        user.is_staff = True
        user.save()
