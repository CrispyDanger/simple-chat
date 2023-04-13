from django.contrib import admin
from .models import Message, Thread


class MessageAdmin(admin.TabularInline):
    list_display = ("sender", "thread", "text")
    model = Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    def message_quantity(self, obj):
        return obj.messages.count()

    def unread_quantity(self, obj):
        return obj.messages.filter(is_read=False).count()

    list_display = [
        "__str__",
        "message_quantity",
        "unread_quantity",
    ]
    inlines = [
        MessageAdmin,
    ]


# Register your models here.
