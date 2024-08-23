from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.models import CourseSection
from courses.serializers import CourseSectionSerializer

class CourseSectionListView(APIView):
    def get(self, request):
        courses = CourseSection.objects.all()
        serializer = CourseSectionSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        if not isinstance(data, list):
            data = [data]

        responses = []
        for item in data:
            id = item.get('id')
            if id:
                # Update existing record
                try:
                    instance = CourseSection.objects.get(id=id)
                    serializer = CourseSectionSerializer(instance, data=item, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        responses.append(serializer.data)
                    else:
                        responses.append({
                            'id': id,
                            'errors': serializer.errors
                        })
                except CourseSection.DoesNotExist:
                    # Create new record if it does not exist
                    serializer = CourseSectionSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()
                        responses.append(serializer.data)
                    else:
                        responses.append({
                            'id': id,
                            'errors': serializer.errors
                        })
            else:
                responses.append({
                    'error': 'ID is required for both creation and update.'
                })

        return Response(responses, status=status.HTTP_200_OK)
