from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^member/info/$', views.member_info, name="member_info"),
    re_path(r'^weekly/permission/$', views.weekly_permission,
            name="weekly_permission"),
    re_path(r'^client/dup/check/$', views.client_dup_check,
            name="client_dup_check"),
    re_path(r'^client/add/apply/$', views.client_add_apply,
            name="client_add_apply"),
]
