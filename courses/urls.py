from django.urls import path
from courses.views import CourseSectionListView

urlpatterns = [
    path('list/', CourseSectionListView.as_view(), name='course-list'),
]
