from rest_framework import generics as rest_fw_generics, filters as rest_fw_filters,\
    parsers as rest_fw_parsers, serializers as rest_fw_serializers, status as rest_fw_status
from rest_framework.response import Response as rest_fw_Response
import django_filters
from . import models, serializers

TEXT_FILTERS = ['iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith',
                'iendswith', 'regex', 'iregex']
DATE_FILTERS = ['range', 'date', 'year', 'iso_year', 'month', 'day', 'week', 'week_day',
                'iso_week_day', 'quarter', 'time', 'hour', 'minute', 'second']
COMMON_FILTERS = ['exact', 'in', 'isnull', 'gt', 'lt', 'gte', 'lte']


class OrganizationDetailView(rest_fw_generics.RetrieveAPIView):
    queryset = models.Organization.objects.prefetch_related('members')
    serializer_class = serializers.OrganizationSerializerList


class OrganizationListCreateView(rest_fw_generics.ListCreateAPIView):
    queryset = models.Organization.objects.prefetch_related('members')
    serializer_class = serializers.OrganizationSerializerList

    def create(self, request, *args, **kwargs):
        self.serializer_class = serializers.OrganizationSerializerCreate
        return super().create(request, *args, **kwargs)


class EventDetailView(rest_fw_generics.RetrieveAPIView):
    queryset = models.Event.objects.prefetch_related('organizations')
    serializer_class = serializers.EventSerializerList


class EventListCreateView(rest_fw_generics.ListCreateAPIView):
    queryset = models.Event.objects.prefetch_related('organizations')
    serializer_class = serializers.EventSerializerList
    parser_classes = [rest_fw_parsers.JSONParser,
                      rest_fw_parsers.MultiPartParser,
                      rest_fw_parsers.FormParser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       rest_fw_filters.SearchFilter,
                       rest_fw_filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['date']
    filterset_fields = {
        'title': TEXT_FILTERS + COMMON_FILTERS,
        'description': TEXT_FILTERS + COMMON_FILTERS,
        'date': DATE_FILTERS + COMMON_FILTERS,
    }

    def create(self, request, *args, **kwargs):
        self.serializer_class = serializers.EventSerializerCreate
        return super().create(request, *args, **kwargs)


class UploadEventImage(rest_fw_generics.CreateAPIView):
    """ Attach event image."""
    UPLOAD_ERROR = {"file_upload_error": "No 'image' field in the multipart form"}

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializerList
    parser_classes = [rest_fw_parsers.MultiPartParser, rest_fw_parsers.FormParser]

    def create(self, request, *args, **kwargs):
        if not request.data.get('image', None):
            raise rest_fw_serializers.ValidationError(self.UPLOAD_ERROR)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = {'image': serializer.data['image']}

        return rest_fw_Response(data, status=rest_fw_status.HTTP_201_CREATED, headers=headers)
