from rest_framework import serializers
from courses.models import CourseSection

class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = [
            'id',
            'academicSectionId',
            'courseId',
            'academicSessionId',
            'courseCode',
            'courseTitle',
            'courseDetails',
            'empName',
            'empShortName',
            'deptName',
            'classSchedule',
            'classLabSchedule',
            'preRequisiteCourses',
            'defaultSeatCapacity',
            'availableSeat',
            'totalFillupSeat',
            'courseCredit',
            'dayNo'
        ]
