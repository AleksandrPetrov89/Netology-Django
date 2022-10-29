from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
# from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Advertisement, AdvertisementStatusChoices
from .serializers import AdvertisementSerializer
from .permissions import IsOwnerOrSuperuserOrCreateOnly
from .filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    # throttle_classes = [AnonRateThrottle, UserRateThrottle] # Можно на весь проект или на ViewSet

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrSuperuserOrCreateOnly()]
        elif self.action in ["list_favorites", "add_to_favorites", "destroy_favorites"]:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.is_anonymous:
            queryset = Advertisement.objects.all().exclude(status=AdvertisementStatusChoices.DRAFT)
            return queryset
        elif self.request.user.is_authenticated:
            queryset = Advertisement.objects.all().exclude(status=AdvertisementStatusChoices.DRAFT) | \
                       Advertisement.objects.filter(status=AdvertisementStatusChoices.DRAFT,
                                                    creator=self.request.user)
            return queryset
        else:
            raise ValueError('Ошибка в get_queryset в AdvertisementViewSet!')

    @action(detail=False)
    def list_favorites(self, request):
        queryset = Advertisement.objects.filter(users=request.user)
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_favorites(self, request):
        queryset = Advertisement.objects.all()
        if request.data["id"] not in list(element.id for element in queryset):
            return Response("Такого объявления не существует!")
        adv = Advertisement.objects.get(id=request.data["id"])
        if request.user == adv.creator:
            return Response("Нельзя добавить в избранное свое объявление!")
        elif adv.status != 'OPEN':
            return Response("В избранное можно добавлять только открытые объявления!")
        else:
            request.user.favor_adv.add(adv)
            serializer = AdvertisementSerializer(adv, many=False)
            return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def destroy_favorites(self, request):
        queryset = request.user.favor_adv.all()
        adv_id = request.data["id"]
        if adv_id not in list(element.id for element in queryset):
            return Response("Это объявление отсутствует в Вашем списке избранных объявлений!")
        request.user.favor_adv.remove(request.user.favor_adv.get(id=adv_id))
        answer = f'Объявление с id={adv_id} удалено из Вашего списка избранных объявлений!'
        return Response(answer)
