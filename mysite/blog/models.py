
from django.db import IntegrityError, models, router, transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
        null=True,
        blank=True,
    )
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField(
        max_length=200,
        allow_unicode=True,
        unique=True,
        blank=True,
        unique_for_date="created_at",
    )
    body = models.TextField("Текст")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    is_published = models.BooleanField("Опубликовано", default=True)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        if self.slug or (update_fields is not None and not update_fields):
            return super().save(*args, **kwargs)

        using = kwargs.get("using") or router.db_for_write(type(self), instance=self)
        kwargs["using"] = using
        if update_fields is not None:
            kwargs["update_fields"] = {*update_fields, "slug"}

        base = slugify(self.title, allow_unicode=True) or "post"
        if base.isdigit() or base == "create":
            base = f"post-{base}"
        max_length = self._meta.get_field("slug").max_length
        existing = type(self).objects.using(using).exclude(pk=self.pk)

        counter = 0
        while True:
            suffix = f"-{counter}" if counter else ""
            candidate = f"{base[:max_length - len(suffix)].rstrip('-')}{suffix}"
            counter += 1
            if existing.filter(slug=candidate).exists():
                continue

            self.slug = candidate
            try:
                with transaction.atomic(using=using):
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.slug = ""
                if not existing.filter(slug=candidate).exists():
                    raise

    def _dated_url(self, view_name):
        created = self.created_at
        if timezone.is_aware(created):
            created = timezone.localtime(created)
        return reverse(
            view_name,
            kwargs={
                "year": created.year,
                "month": created.month,
                "day": created.day,
                "slug": self.slug,
            },
        )

    def get_absolute_url(self):
        return self._dated_url("blog:post_detail")

    def get_edit_url(self):
        return self._dated_url("blog:post_edit")

    def get_delete_url(self):
        return self._dated_url("blog:post_delete")

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
        null=True,
        blank=True,
    )

    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author}"
