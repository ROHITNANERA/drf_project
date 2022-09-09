import contextlib
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

app_models = apps.get_app_config('myapp').get_models()

for model in app_models:
    with contextlib.suppress(AlreadyRegistered):
        class ModelAdmins(admin.ModelAdmin):
            all_fields = [i.name for i in model._meta.fields]
            list_display = list(all_fields)
            search_fields = [i.name for i in model._meta.fields if i.get_internal_type() not in ['OneToOneField', 'ForeignKey']]
            list_per_page = 50
            list_max_show_all = 500
            parent_fields = model.get_deferred_fields(model)

        admin.site.register(model, ModelAdmins)
