from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Video, Tagging, Comment, UserRating


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    exclude = ('duration', 'transcript', 'name','length_in_sec', 'bucket_size')


class TaggingAdmin(admin.ModelAdmin):
    exclude = ('date_subscribed', 'rating_value', 'amount_of_comments', 'transcript_score', 'rating_score',
               'total_tag_score', ' is_validated', 'start_seconds', 'end_seconds')


admin.site.register(Video, MyModelAdmin)
admin.site.register(Tagging, TaggingAdmin)
admin.site.register(Comment)
admin.site.register(UserRating)
