from . import common
from .. import models, serializers, permissions

from django_filters import rest_framework
from rest_framework import generics, filters, viewsets


class AuthorizationFilter(rest_framework.FilterSet):
    class Meta:
        model = models.Authorization
        fields = {
            'id': ['lt', 'gt'],
            'entity': ['exact'],
            'subject': ['exact'],
            'fingerprint': ['exact'],
            'timestamp': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'start_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'expiry_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }


class AuthorizationViewSet(viewsets.ModelViewSet):
    queryset = models.Authorization.objects.all()
    serializer_class = serializers.AuthorizationSerializer
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        common.PETSearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = AuthorizationFilter
    search_fields = ('subject', 'fingerprint')
    ordering_fields = ('id', 'timestamp')
    ordering = ('-id',)
    pagination_class = common.PETPagination


class EntityAuthorizationViewSet(AuthorizationViewSet):

    def get_queryset(self):
        print(self.request)
        return models.Authorization.objects.all()


class AuthorizationClientView(generics.ListAPIView):
    permission_classes = (permissions.PETAuthPermission,)
    serializer_class = serializers.AuthorizationClientSerializer

    def get_queryset(self):
        return self.request.entity.authorizations.all()
