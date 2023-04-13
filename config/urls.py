from django.contrib import admin
from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from chat.views import (
    ThreadDestroyView,
    ThreadListView,
    ThreadMessageListView,
    ThreadMessageCreateView,
    ThreadMessageDetailview,
    UnreadMessageView,
)

admin.site.site_header = "Simple Chat Admin"
admin.site.index_title = "Simple Chat"

urlpatterns = [
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("api/threads/", ThreadListView.as_view(), name="threads_list"),
    re_path(
        r"^api/threads/(?P<id>\d+)/$",
        ThreadDestroyView.as_view(),
        name="destroy_thread",
    ),
    path(
        "api/threads/<int:id>/messages/",
        ThreadMessageListView.as_view(),
        name="messages",
    ),
    re_path(
        r"^api/threads/(?P<thread_id>\d+)/messages/new/$",
        ThreadMessageCreateView.as_view(),
    ),
    re_path(
        r"^api/threads/(?P<thread_id>\d+)/messages/(?P<message_id>\d+)/$",
        ThreadMessageDetailview.as_view(),
    ),
    re_path(r"^api/messages/unread/$", UnreadMessageView.as_view()),
]
