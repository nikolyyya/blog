from django.db import migrations, models
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    post = apps.get_model("blog", "Post")
    posts = post.objects.using(schema_editor.connection.alias)
    reserved = set()
    max_length = post._meta.get_field("slug").max_length
    for pk, title in posts.order_by("pk").values_list("pk", "title").iterator():
        base = slugify(title, allow_unicode=True) or "post"
        if base.isdigit() or base == "create":
            base = f"post-{base}"

        counter = 0
        while True:
            suffix = f"-{counter}" if counter else ""
            candidate = f"{base[:max_length - len(suffix)].rstrip('-')}{suffix}"
            if candidate not in reserved:
                break
            counter += 1

        posts.filter(pk=pk).update(slug=candidate)
        reserved.add(candidate)


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_alter_post_author_alter_post_is_published"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=200, allow_unicode=True, blank=True, null=True),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(max_length=200, allow_unicode=True, blank=True, unique=True),
        ),
    ]
