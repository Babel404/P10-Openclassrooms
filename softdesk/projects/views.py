from rest_framework import generics, permissions
from projects import serializers
from projects.models import Project, Contributor, Issue, Comment
from projects.permissions import (
    IsAuthorProjectOrContributorReadOnly,
    IsAuthorObjectOrContributorReadOnly,
    IsContributorList,
)
from projects.services_views import (
    serializer_method,
    get_contributors_projet,
    create_project,
    create_contributor_projet,
    destroy_object,
    queryset_filter,
    create_issue,
    update_issue,
    create_comment,
)


class ProjectList(generics.ListCreateAPIView):
    """
    View liste des projets liés
    à l'utilisateur
    """
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return serializer_method(self, 'Project')

    def get_queryset(self):
        return get_contributors_projet(self)

    def perform_create(self, serializer):
        return create_project(self, serializer)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View détail du projet
    Accessible uniquement à l'Author
    """
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorProjectOrContributorReadOnly
    ]
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        return destroy_object(self, 'Project')


class ContributorList(generics.ListCreateAPIView):
    """
    View liste des Contributors
    Accessible uniquement aux Contributors du projet
    Seul l'Author peut add des Contributors
    """
    serializer_class = serializers.ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorProjectOrContributorReadOnly
    ]

    def get_queryset(self, *args, **kwargs):
        return queryset_filter(self, 'project_id')

    def get_serializer_class(self):
        return serializer_method(self, 'Contributor')

    def perform_create(self, serializer):
        return create_contributor_projet(self, serializer=serializer)


class ContributorDelete(generics.DestroyAPIView):
    """
    View suppression de Contributors
    Accessible uniquement a l'Author
    """
    serializer_class = serializers.ContributorSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorProjectOrContributorReadOnly
    ]

    def get_queryset(self):
        queryset = Contributor.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        return destroy_object(self, 'Contributor')


class IssueList(generics.ListCreateAPIView):
    """
    View liste des issues d'un projet.
    Accessible uniquement aux Contributors
    """
    queryset = Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsContributorList
    ]

    def get_queryset(self):
        return queryset_filter(self, 'project_id')

    def get_serializer_class(self):
        return serializer_method(self, 'Issue')

    def perform_create(self, serializer):
        return create_issue(self, serializer)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View détail Issue d'un projet
    Accessible uniquement à l'Author de l'issue
    """
    queryset = Issue.objects.all()
    serializer_class = serializers.IssueSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorObjectOrContributorReadOnly
    ]
    http_method_names = ['put', 'delete']

    def perform_update(self, serializer):
        return update_issue(self, serializer)

    def destroy(self, request, *args, **kwargs):
        return destroy_object(self, 'Issue')


class CommentList(generics.ListCreateAPIView):
    """
    View liste des Comments
    Accessible uniquement aux Contributors
    """
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsContributorList
    ]

    def get_queryset(self):
        return queryset_filter(self, 'issue_id')

    def get_serializer_class(self):
        return serializer_method(self, 'Comment')

    def perform_create(self, serializer):
        create_comment(self, serializer)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View détail Comment
    Accessible uniquement à l'Author du Comment
    """
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorObjectOrContributorReadOnly
    ]
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        return destroy_object(self, 'Comment')
