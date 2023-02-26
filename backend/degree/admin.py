from django.contrib import admin

from degree.models import Degree, DegreeRequirement

# Register your models here.
class DegreeAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
    )
    search_fields = (
        "name",
        "code",
    )
    list_filter = [
        "name",
        "requirements"
    ]
    list_display = (
        "name",
    )

class DegreeRequirementAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
    )
    search_fields = (
        # "name",
        # "satisfied_by",
        # "topics",
        # "num",
        # "degree",
    )
    list_filter = [
        # "name",
        # "satisfied_by",
        # "topics",
        # "num",
    ]
    list_display = (
        "id",
    )

admin.site.register(Degree, DegreeAdmin)
admin.site.register(DegreeRequirement, DegreeRequirementAdmin)
