from __future__ import absolute_import
from django.conf.urls import include, url
from django.contrib.flatpages import urls as flatpages_urls
from rest_framework.routers import DefaultRouter
from rest_framework import urls as rest_framework_urls
from markitup import urls as markitup_urls

from observations.api import PenguinCountViewSet, PenguinObservationViewSet, VideoViewSet
from observations.sites import site
from observations.views import VideoImport, S3View


router = DefaultRouter()
router.register(r'count', PenguinCountViewSet)
router.register(r'observations', PenguinObservationViewSet)
router.register(r'videos', VideoViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include(rest_framework_urls, namespace='rest_framework')),
    url(r'^markitup/', include(markitup_urls)),
    url(r'^help/', include(flatpages_urls)),
    url(r'^cronjobs/video-import/$', VideoImport.as_view(), name='cronjobs_video_import'),
    url(r'^observations/s3/$', S3View.as_view(), name='s3_view'),
    url(r'', include(site.urls)),
]
