from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import (  # noqa: E501 pylint: disable=imported-auth-user
    Group,
    User
)
from django.utils.translation import gettext_lazy


class FZWAdminSite(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('Fajnie ze wiesz admin')  # type: ignore

    # Text to put in each page's <h1> (and above login form).
    site_header = gettext_lazy('Fajnie ze wiesz administration')  # type: ignore

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('Site administration')  # type: ignore


admin_site = FZWAdminSite()
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
