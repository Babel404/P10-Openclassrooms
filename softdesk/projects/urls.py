from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from projects import views

urlpatterns = [
    path(
        '',
        views.ProjectList.as_view()
    ),
    path(
        '<int:pk>',
        views.ProjectDetail.as_view()
    ),
    path(
        '<int:project_id>/users/',
        views.ContributorList.as_view()
    ),
    path(
        '<int:project_id>/users/<int:pk>',
        views.ContributorDelete.as_view()
    ),
    path(
        '<int:project_id>/issues/',
        views.IssueList.as_view()
    ),
    path(
        '<int:project_id>/issues/<int:pk>',
        views.IssueDetail.as_view()
    ),
    path(
        '<int:project_id>/issues/<int:issue_id>/comments/',
        views.CommentList.as_view()
    ),
    path(
        '<int:project_id>/issues/<int:issue_id>/comments/<int:pk>',
        views.CommentDetail.as_view()
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
