from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        if ("status", "OPEN") in data.items():
            if self._args:
                user = self._args[0].creator
            else:
                user = self.context["request"].user
            adv_user_open = Advertisement.objects.filter(creator=user,
                                                         status=AdvertisementStatusChoices.OPEN)
            quantity_adv = len(adv_user_open)
            if quantity_adv >= 10:
                raise serializers.ValidationError('Превышен лимит действующих объявлений '
                                                  '(имеющих статус "Открыто"). '
                                                  'Закройте неактуальные и повторите попытку!')

        return data
