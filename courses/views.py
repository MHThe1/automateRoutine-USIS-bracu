from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import CourseSection, CourseCode, CourseSectionInfo
from courses.serializers import CourseSectionSerializer
from collections import defaultdict
from .utils import generate_routines


from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.permissions import IsAdminOrReadOnly
from courses.faculties_data import faculties
from courses.course_data import course_data 


class AllCourseFacultiesView(APIView):
    def get(self, request):
        output_faculties = faculties
        return Response(output_faculties, status=status.HTTP_200_OK)
    
class AllCourseCodesView(APIView):
    def get(self, request):
        course_codes = list(course_data.keys())
        return Response(course_codes, status=status.HTTP_200_OK)

class CourseCodeSuggestionsAV(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            filtered_course_codes = [code for code in course_data if query.lower() in code.lower()]
            return Response(filtered_course_codes)
        return Response([])

class CourseSectionsView(APIView):
    def get(self, request, course_code):
        sections = course_data.get(course_code, [])
        sections_data = [
            {
                'courseDetails': section
            }
            for section in sections
        ]
        return Response(sections_data, status=status.HTTP_200_OK)


class GenerateRoutinesView(APIView):
    def post(self, request):
        data = request.data.get('courses', [])
        min_days = int(request.query_params.get('min_days', 2))
        max_days = int(request.query_params.get('max_days', 6))
        avoid_faculty = request.data.get('avoid_faculty', [])
        avoid_time = request.data.get('avoid_time', [])
        avoid_day = request.data.get('avoid_day', [])
        course_count = len(data)

        # print(f"avoid_faculty: {avoid_faculty}")
        # print(f"avoid_time: {avoid_time}")
        # print(f"min_days: {min_days}")
        # print(f"max_days: {max_days}")
        # print(f"course_details: {data}")

        sections_data = defaultdict(list)
        for entry in data:
            course_code = entry.get("courseCode")
            sections = entry.get("sections", [])
            faculties = entry.get("faculties", [])
            # print(sections)

            if sections:
                final_sections = CourseSection.objects.none()  # Start with an empty queryset
                for section in sections:
                    filtered_section = CourseSection.objects.filter(courseDetails=section)
                    final_sections = final_sections | filtered_section  # Accumulate sections using OR
                sections = final_sections  # Use the combined queryset
            else:
                sections = CourseSection.objects.filter(courseCode=course_code)
                
            if faculties:
                final_faculties = CourseSection.objects.none()  # Start with an empty queryset for faculties
                for faculty in faculties:
                    filtered_faculty = sections.filter(empShortName=faculty)
                    final_faculties = final_faculties | filtered_faculty  # Accumulate faculties using OR
                sections = final_faculties

            if avoid_faculty:
                for faculty in avoid_faculty:
                    sections = sections.exclude(empShortName=faculty)
                    
            if avoid_time:
                for time_period in avoid_time:
                    # print(f"time_period: {time_period}")
                    sections = sections.exclude(classLabSchedule__contains=time_period)
            if avoid_day:
                for day in avoid_day:
                    sections = sections.exclude(classLabSchedule__contains=day)

            for section in sections:
                sections_data[section.courseCode].append({
                    'id': section.id,
                    'academicSectionId': section.academicSectionId,
                    'courseId': section.courseId,
                    'academicSessionId': section.academicSessionId,
                    'courseCode': section.courseCode,
                    'courseTitle': section.courseTitle,
                    'courseDetails': section.courseDetails,
                    'empName': section.empName,
                    'empShortName': section.empShortName,
                    'deptName': section.deptName,
                    'classSchedule': section.classSchedule,
                    'classLabSchedule': section.classLabSchedule,
                    'preRequisiteCourses': section.preRequisiteCourses,
                    'defaultSeatCapacity': section.defaultSeatCapacity,
                    'availableSeat': section.availableSeat,
                    'totalFillupSeat': section.totalFillupSeat,
                    'courseCredit': section.courseCredit,
                    'dayNo': section.dayNo,
                })

        sections_data_list = list(sections_data.values())
        routines_data = generate_routines(sections_data_list, course_count, min_days, max_days)

        return Response(routines_data, status=status.HTTP_200_OK)


class CourseSectionListView(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):        
        course_code = request.query_params.get('courseCode')
        
        if course_code:
            courses = CourseSection.objects.filter(courseCode=course_code)
        else:
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



class RoutineCheckView(APIView):
    def post(self, request):
        course_codes = request.data.get('courseCodes', [])
        if not isinstance(course_codes, list):
            return Response({'error': 'courseCodes must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(course_codes) != 4:
            return Response({'error': 'Exactly 4 course codes must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter courses by the given course codes
        courses = CourseSection.objects.filter(courseCode__in=course_codes)
        serializer = CourseSectionSerializer(courses, many=True)
        
        # Check for time conflicts
        routines = self.find_conflict_free_routines(serializer.data)
        
        return Response(routines, status=status.HTTP_200_OK)
    
    def find_conflict_free_routines(self, courses):
        routines = []
        # Helper function to parse schedule strings into a list of tuples (day, start_time, end_time, location)
        def parse_schedule(schedule):
            parsed_schedule = []
            for item in schedule:
                if len(item) == 2:  # Ensure the item has exactly 2 elements
                    day, time = item
                    parsed_schedule.append((day, time))
                else:
                    # Handle or log unexpected item format
                    print(f"Unexpected item format: {item}")
            return parsed_schedule

        
        # Check if two schedules conflict
        def has_conflict(schedule1, schedule2):
            times1 = parse_schedule(schedule1)
            times2 = parse_schedule(schedule2)
            for time1 in times1:
                for time2 in times2:
                    if time1[0] == time2[0] and not (time1[2] <= time2[1] or time2[2] <= time1[1]):
                        return True
            return False
        
        # Check all combinations
        def find_combinations(index, current_combination):
            if index == len(courses):
                if len(current_combination) > 1:
                    routines.append(current_combination)
                return
            
            find_combinations(index + 1, current_combination)
            
            conflict = False
            for item in current_combination:
                if has_conflict(courses[index]['classSchedule'], item['classSchedule']) or \
                   has_conflict(courses[index]['classLabSchedule'], item['classLabSchedule']):
                    conflict = True
                    break
            
            if not conflict:
                find_combinations(index + 1, current_combination + [courses[index]])
        
        find_combinations(0, [])
        return routines
    
    
