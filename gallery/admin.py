from django.contrib import admin
from gallery.models import FileGallery


@admin.register(FileGallery)
class FileGalleryAdmin(admin.ModelAdmin):
    list_display = (
        'alt',
        'created_at',
        'created_by',
    )
    readonly_fields = (
        'created_at',
        'created_by',
    )
    fields = (
        'alt',
        'file',
        'created_at',
        'created_by',
    )

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.save()
        form.save_m2m()
        return instance
