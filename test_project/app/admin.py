from django.contrib import admin
from django.utils.translation import gettext as _

from django_admin_search_fields.admin import DjangoAdminSearchFieldModelAdmin

from .models import Author, Post


class PostAdmin(DjangoAdminSearchFieldModelAdmin):
    search_help_text = "You can select specific fields to target your search, allowing you to find the text you’re looking for more efficiently."
    search_field_choices = (
        ("title", True),
        ("subtitle", False),
        ("author__full_name", False, _("By Author's Name")),
    )
    list_display = ("title", "subtitle")

    class Meta:
        js = ("django_admin_search_fields/search.js",)
        css = ("django_admin_search_fields/search.css",)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
