
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_post_authors(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    user = User.objects.filter(username='veronika').first()

    if user:
        Post.objects.filter(author='Вероника').update(author_new_id=user.id)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_comment_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_new',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                null=True,
                blank=True,
            ),
        ),
        migrations.RunPython(
            migrate_post_authors,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='author_new',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='posts',
                verbose_name='Автор',
                null=True,
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(
                default=True,
                verbose_name='Опубликовано',
            ),
        ),
    ]
