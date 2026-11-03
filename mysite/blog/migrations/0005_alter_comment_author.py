
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_comment_authors(apps, schema_editor):
    Comment = apps.get_model('blog', 'Comment')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    user = User.objects.filter(username='veronika').first()

    if user:
        Comment.objects.filter(author='Вероника').update(author_new_id=user.id)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_is_published_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
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
            migrate_comment_authors,
            migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='author_new',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='comments',
                verbose_name='Автор',
                null=True,
                blank=True,
            ),
        ),
    ]
