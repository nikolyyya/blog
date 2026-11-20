from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    bio = models.TextField("О себе", blank=True)
    location = models.CharField("Город", max_length=100, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else f"{settings.MEDIA_URL}avatars/default_avatar.png"

    def __str__(self):
        return f"Профиль пользователя {self.user.get_username()}"
