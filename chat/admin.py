from django.contrib import admin
from .models import Message, Thread


class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "thread", "text")


admin.site.register(Message, MessageAdmin)
admin.site.register(Thread)
# Register your models here.
