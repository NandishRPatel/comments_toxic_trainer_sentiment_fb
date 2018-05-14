from django.conf.urls import url, include

from .views import ProfileView, ProfilePostView, save_toxic_comment

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name="profile"),
    url(r'^post/(?P<profile>[a-zA-Z0-9_]+)/(?P<post_id>[0-9_]+)/$', ProfilePostView.as_view(), name="post"),
    url(r'^ajax/save_comment/$', save_toxic_comment, name='save_comment'),
]
