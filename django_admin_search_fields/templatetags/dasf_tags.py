from django.contrib.admin.views.main import IS_POPUP_VAR, SEARCH_VAR
from django.template import Library
from django.template.loader import render_to_string

try:
    from django.contrib.admin.views.main import IS_FACETS_VAR
except ImportError:
    IS_FACETS_VAR = None

register = Library()


@register.simple_tag
def dasf_search_form(cl, search_field_selections):
    return render_to_string(
        "django_admin_search_fields/search_form.html",
        {
            "cl": cl,
            "show_result_count": cl.result_count != cl.full_result_count,
            "search_var": SEARCH_VAR,
            "is_popup_var": IS_POPUP_VAR,
            "is_facets_var": IS_FACETS_VAR,
            "search_field_selections": search_field_selections,
        },
    )
