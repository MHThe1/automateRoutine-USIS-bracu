from django.urls import path
from courses.views import CourseSectionListView, RoutineCheckView, GenerateRoutinesView, CourseSectionsView, CourseCodeSuggestionsAV, AllCourseCodesView

urlpatterns = [
    path('list/', CourseSectionListView.as_view(), name='course-list'),
    path('check-routines/', RoutineCheckView.as_view(), name='check-routines'),
    path('course-sections/', CourseSectionListView.as_view(), name='course-section-list'),
    path('generate-routines/', GenerateRoutinesView.as_view(), name='generate_routines'),
    path('sections/<str:course_code>/', CourseSectionsView.as_view(), name='course-sections'),
    path('course-code-suggestions/', CourseCodeSuggestionsAV.as_view(), name='course-code-suggestions'),
    path('all-course-codes/', AllCourseCodesView.as_view(), name='all-course-codes'),

]
