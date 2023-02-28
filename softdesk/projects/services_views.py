from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from projects.models import Project, Contributor, Issue
from projects import serializers


def users_list_id(self):
    """
    Retourne les ID des contributeurs
    d'un projet
    """
    return [
        user.user_id.id for user in Contributor.objects.filter(
            project_id=self.kwargs['project_id']
        )
    ]


def serializer_method(self, model):
    """
    Renvoi le Serializer à utiliser
    (Liste ou détail)
    """
    get_serializer = 'serializers.' + model + 'ListSerializer'
    post_serializer = 'serializers.' + model + 'Serializer'
    if self.request.method == 'GET':
        return eval(get_serializer)
    return eval(post_serializer)


def queryset_filter(self, obj):
    """
    Renvoi le filtre à utiliser pour le queryset
    """
    if obj == 'project_id':
        return self.queryset.filter(project_id=self.kwargs.get(obj))
    if obj == 'issue_id':
        return self.queryset.filter(issue_id=self.kwargs.get(obj))


def create_project(self, serializer):
    """
    Création d'un projet et
    attribution automatique du rôle 'Author'
    """
    project = serializer.save(author_user_id=self.request.user)
    contributor = Contributor.objects.create(
        user_id=self.request.user,
        project_id=project,
        role="Author"
    )
    contributor.save()


def get_contributors_projet(self):
    """
    Renvoie la liste des projets liés
    à un contributor
    """
    contributors_list = [
        project.project_id for project in Contributor.objects.filter(
            user_id=self.request.user
        )
    ]
    return contributors_list


def create_contributor_projet(self, serializer):
    """
    Ajouter un contributor au projet
    """
    project_id = Project.objects.get(pk=self.kwargs['project_id'])
    if int(self.request.data['user_id']) in users_list_id(self):
        raise ValidationError(
            "l'utilisateur fait deja partie du projet"
        )
    return serializer.save(project_id=project_id)


def destroy_object(self, obj):
    """
    Suppression d'un objet
    """
    if obj == 'Contributor':
        try:
            instance = Contributor.objects.get(
                user_id=User.objects.get(pk=self.kwargs['pk']),
                project_id=Project.objects.get(pk=self.kwargs['project_id'])
            )
            user = User.objects.get(pk=self.kwargs['pk'])
            author_project = Project.objects.get(
                pk=self.kwargs['project_id']
            ).author_user_id
            if user == author_project:
                raise ValidationError(
                    "L'auteur du projet ne peut pas être supprimé"
                )
            self.perform_destroy(instance)
            return Response("Utilisateur supprimé")
        except User.DoesNotExist:
            raise ValidationError("l'utilisateur n'existe pas")
        except Contributor.DoesNotExist:
            raise ValidationError(
                "l'utilisateur n'est pas contributeur du projet"
            )
    instance = self.get_object()
    self.perform_destroy(instance)
    return Response("{} supprimé".format(obj))


def test_user_assignee(self):
    """
    Test si le user est bien contributor
    d'un projet donné
    """
    if int(self.request.data['assignee_user_id']) not in users_list_id(self):
        raise ValidationError(
            "l'utilisateur assigné n'est pas collaborateur du projet"
        )


def create_issue(self, serializer):
    """
    Création d'une issue
    """
    test_user_assignee(self)
    project = Project.objects.get(pk=self.kwargs['project_id'])
    serializer.save(
        author_user_id=self.request.user,
        project_id=project
    )


def update_issue(self, serializer):
    """
    Modification issue
    """
    test_user_assignee(self)
    serializer.save()


def create_comment(self, serializer):
    """
    Création d'un comment
    """
    issue = Issue.objects.get(pk=self.kwargs['issue_id'])
    serializer.save(
        author_user_id=self.request.user,
        issue_id=issue
    )
