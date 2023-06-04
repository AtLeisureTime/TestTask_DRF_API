from django.urls import path, re_path, include
from django.views.generic import TemplateView
import rest_framework_simplejwt.views as jwt_views
from rest_framework import renderers as rest_fw_renderers, routers as rest_fw_routers
from rest_framework.schemas import get_schema_view
from . import views

app_name = "org_events"

router = rest_fw_routers.DefaultRouter()

urlpatterns = [
    re_path('^token/?$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('^token/refresh/?$', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path('^token/verify/?$', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    re_path('^org/?$', views.OrganizationListCreateView.as_view(), name="api_org_list_create"),
    re_path('^org/(?P<pk>[0-9]+)/?$',
            views.OrganizationDetailView.as_view(), name="api_org_detail"),
    re_path('^event/?$', views.EventListCreateView.as_view(), name="api_event_list_create"),
    re_path('^event/(?P<pk>[0-9]+)/?$', views.EventDetailView.as_view(), name="api_event_detail"),
    re_path('^event/(?P<pk>[0-9]+)/uploadImage/?$', views.UploadEventImage.as_view(),
            name="api_event_image_upload"),

    path('openapi/', get_schema_view(
        title="App API", description="API", version="1.0.0",), name='openapi-schema'),
    path('openapi-schema.json/', get_schema_view(
        title="App API", description="API",  version="1.0.0",
        renderer_classes=[rest_fw_renderers.JSONOpenAPIRenderer],
    ), name='openapi-schema-json'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html', extra_context={'schema_url': 'org_events:openapi-schema'}
    ), name='swagger-ui'),
    path('', include(router.urls)),
]
