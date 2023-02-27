from django.db import models
from django.contrib.auth.models import User
from projects import models_settings


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    project_type = models.CharField(
        max_length=20,
        choices=models_settings.TYPE_CHOICES
    )
    author_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_id'
    )
    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_id'
    )
    role = models.CharField(max_length=150)

    class Meta:
        """
        Un utilisateur ne peut s'enregistrer
        qu'une seule fois sur un même projet
        """
        unique_together = ['user_id', 'project_id']


class Issue(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    tag = models.CharField(
        max_length=20,
        choices=models_settings.TAG_CHOICES
    )

    priority = models.CharField(
        max_length=20,
        choices=models_settings.PRIORITY_CHOICES
    )
    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=models_settings.STATUS_CHOICES
    )
    author_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_user'
    )
    assignee_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignee_user'
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField()
    author_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE
    )
    created_time = models.DateTimeField(auto_now_add=True)
