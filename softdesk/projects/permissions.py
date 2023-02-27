from rest_framework import permissions
from .services_permissions import (
    get_contributors_project,
    permission_method
)


class IsAuthorProjectOrContributorReadOnly(permissions.BasePermission):
    """
    Project
    Author Lecture/Ecriture
    Contributor Lecture
    """
    def has_permission(self, request, view):
        return permission_method(request)


class IsAuthorObjectOrContributorReadOnly(permissions.BasePermission):
    """
    Object (issue/comment)
    Author Lecture/Ecriture
    Contributor Lecture
    """
    def has_object_permission(self, request, view, obj):
        return permission_method(request, obj)


class IsContributorList(permissions.BasePermission):
    """
    Project
    Contributor authorized Lecture/Ecriture
    """
    def has_permission(self, request, view):
        return get_contributors_project(request)
