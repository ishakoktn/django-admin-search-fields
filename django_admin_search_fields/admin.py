from django.contrib import admin


class DjangoAdminSearchFieldsMixin:
    change_list_template = "django_admin_search_fields/change_list.html"
    search_field_choices = ()
    _selected_search_fields = ()

    def get_selected_search_fields(self):
        """
        Retrieves the list of currently selected search fields.
        """
        if not self.search_field_choices or not self._selected_search_fields:
            return ()

        valid_fields = {field_name for field_name, *_ in self.search_field_choices}

        if not all(field in valid_fields for field in self._selected_search_fields):
            return ()

        return self._selected_search_fields

    def get_search_results(self, request, queryset, search_term):
        """
        Modifies search_fields to use the selected search fields while getting search results.
        """
        # Preserve the original search_fields
        original_search_fields = self.search_fields
        self.search_fields = self.get_selected_search_fields()

        # Get search results using the modified search_fields
        results = super().get_search_results(request, queryset, search_term)

        # Restore the original search_fields and save the selected fields
        self._selected_search_fields = self.search_fields
        self.search_fields = original_search_fields

        return results

    def get_search_field_selections(self, request):
        """
        Prepares a list of search fields with their prechecked status and verbose names.
        Defaults are based on search_field_choices.
        """
        if not self.search_field_choices:
            return []

        selections = []

        for item in self.search_field_choices:
            if len(item) == 3:
                field_name, prechecked, verbose_name = item
            else:
                field_name, prechecked = item
                assert "__" not in field_name, (
                    f"You should set a verbose name for the relational field "
                    f"({field_name}) in {self.__class__.__name__}'s search_field_choices"
                )
                verbose_name = self.model._meta.get_field(field_name).verbose_name

            # Override prechecked status based on user selection
            if self._selected_search_fields:
                prechecked = field_name in self._selected_search_fields

            selections.append((field_name, prechecked, verbose_name))

        return selections

    def changelist_view(self, request, extra_context=None):
        """
        Extends the changelist view to process selected search fields and add them to the context.
        """
        if request.GET:
            request.GET._mutable = True
            try:
                self._selected_search_fields = request.GET.pop("search-fields", None)
            except KeyError:
                self._selected_search_fields = None
            finally:
                request.GET._mutable = False

        extra_context = extra_context or {}
        extra_context["search_field_selections"] = self.get_search_field_selections(
            request
        )

        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {"all": ["django_admin_search_fields/search.css"]}
        js = ["django_admin_search_fields/search.js"]


class DjangoAdminSearchFieldModelAdmin(DjangoAdminSearchFieldsMixin, admin.ModelAdmin):
    """
    ModelAdmin class that allows the selection of search fields.

    Example usage:

    class PostModelAdmin(DjangoAdminSearchFieldModelAdmin):
        search_field_choices = (
            ('title', True, 'aTitle'),  # Prechecked by default
            ('subtitle', False),       # Not prechecked by default
            ('author__first_name', False, _("By Author's Name"))  # Requires a verbose name for relational fields
        )

    The `title` field will be prechecked. Check fewer fields for better performance.
    """
