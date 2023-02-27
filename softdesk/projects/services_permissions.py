from django.http import Http404
from rest_framework import permissions
from .models import Project, Contributor


def get_project(request):
    """
    Renvoie le projet lié à la 'pk'
    ou au 'project_id' dans l'url
    """
    try:
        project_id = request.parser_context["kwargs"]["project_id"]
    except KeyError:
        project_id = request.parser_context["kwargs"]["pk"]
    try:
        projet = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404
    return projet


def get_contributors_project(request):
    """
    Renvoie la liste des constributeurs
    liés à un projet
    """
    contributors = [
        user.user_id for user in Contributor.objects.filter(
            project_id=get_project(request)
        )
    ]
    if request.user in contributors:
        return True


def permission_method(request, obj=None):
    """
    Renvoi les droits de Lecture/Ecriture
    liés à un projet/comment/issue
    """
    if request.method in permissions.SAFE_METHODS:
        return get_contributors_project(request)
    if obj:
        return obj.author_user_id == request.user
    return get_project(request).author_user_id == request.user
