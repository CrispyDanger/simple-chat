from django.contrib import admin
from django.urls import path
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


urlpatterns = [
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("api/threads/", ThreadListView.as_view(), name="threads_list"),
    path("api/threads/<int:id>/", ThreadDestroyView.as_view(), name="destroy_thread"),
    path(
        "api/threads/<int:id>/messages/",
        ThreadMessageListView.as_view(),
        name="messages",
    ),
    path(
        "api/threads/<int:thread_id>/messages/new/",
        ThreadMessageCreateView.as_view(),
    ),
    path(
        "api/threads/<int:thread_id>/messages/<int:message_id>/",
        ThreadMessageDetailview.as_view(),
    ),
    path("api/unread/", UnreadMessageView.as_view()),
]
