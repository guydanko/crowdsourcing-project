from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Video, Tagging


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    exclude = ('duration', 'transcript', 'name')


admin.site.register(Video, MyModelAdmin)
admin.site.register(Tagging)
