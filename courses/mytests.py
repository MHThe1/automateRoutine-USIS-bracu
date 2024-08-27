from itertools import product
from datetime import datetime

# Helper function to parse the schedule time
def parse_time(time_str):
    # print(datetime.strptime(time_str, '%I:%M %p'))
    return datetime.strptime(time_str, '%I:%M %p')

def calculate_total_duration(routine):
    daily_start_end_times = {}
    days_covered = set()

    # Collect all time slots from all courses in the routine
    for course in routine:
        schedule = parse_schedule(course['classSchedule'])
        for day, times in schedule.items():
            days_covered.add(day)
            if day not in daily_start_end_times:
                daily_start_end_times[day] = {'start': None, 'end': None}

            for time_slot in times:
                start_time = parse_time(time_slot[0])
                end_time = parse_time(time_slot[1])

                # Update daily start and end times
                if daily_start_end_times[day]['start'] is None or start_time < daily_start_end_times[day]['start']:
                    daily_start_end_times[day]['start'] = start_time
                if daily_start_end_times[day]['end'] is None or end_time > daily_start_end_times[day]['end']:
                    daily_start_end_times[day]['end'] = end_time

    # Calculate the total duration for each day
    total_minutes = 0
    for day, times in daily_start_end_times.items():
        if times['start'] and times['end']:
            duration = (times['end'] - times['start']).total_seconds() / 60
            total_minutes += duration

    return total_minutes, len(days_covered)





# Helper function to check if two time slots overlap
def times_overlap(slot1, slot2):
    start1, end1 = parse_time(slot1[0]), parse_time(slot1[1])
    start2, end2 = parse_time(slot2[0]), parse_time(slot2[1])
    return max(start1, start2) < min(end1, end2)

# Helper function to check for time conflicts in schedules
def has_time_conflict(schedule1, schedule2):
    for day1, times1 in schedule1.items():
        if day1 in schedule2:
            for time_slot1 in times1:
                for time_slot2 in schedule2[day1]:
                    if times_overlap(time_slot1, time_slot2):
                        return True
    return False

# Parse the class schedule into a dictionary
def parse_schedule(schedule_str):
    schedule = {}
    for entry in schedule_str.split(','):
        day, times = entry.split('(')
        times = times[:-1]  # Remove the trailing ')'
        time_parts = times.split('-')
        start_time = time_parts[0].strip()
        end_time = time_parts[1].strip()
        # Adding the parsed time slots to the schedule
        if day not in schedule:
            schedule[day] = []
        schedule[day].append((start_time, end_time))
    
    # print(f"parsed schedule: {schedule}")
    return schedule


# Generate all possible routines without time conflicts
def generate_routines(courses):
    all_combinations = list(product(*courses))
    routines = []
    for combination in all_combinations:
        conflict = False
        for i in range(len(combination)):
            for j in range(i + 1, len(combination)):
                if has_time_conflict(
                    parse_schedule(combination[i]['classSchedule']),
                    parse_schedule(combination[j]['classSchedule'])
                ):
                    conflict = True
                    break
            if conflict:
                break
        if not conflict:
            total_duration, total_days = calculate_total_duration(combination)
            routines.append({
                'courses': combination,
                'total_duration': total_duration,
                'total_days': total_days
            })
    sorted_routines = sorted(routines, key=lambda x: (x['total_days'], x['total_duration']))
    return sorted_routines




cse422 = [ {
        "id": 9934,
        "academicSectionId": 2312510,
        "courseId": 117771,
        "academicSessionId": 627124,
        "courseCode": "CSE422",
        "courseTitle": "ARTIFICIAL INTELLIGENCE",
        "courseDetails": "CSE422-[01]",
        "empName": "Md. Tanzim Reza",
        "empShortName": "TRZ",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Saturday(11:00 AM-12:20 PM-07H-26C),Thursday(11:00 AM-12:20 PM-07H-26C)",
        "classLabSchedule": "Saturday(11:00 AM-12:20 PM-07H-26C),Thursday(11:00 AM-12:20 PM-07H-26C),Wednesday(08:00 AM-09:20 AM-12F-31L),Wednesday(09:30 AM-10:50 AM-12F-31L)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 33,
        "availableSeat": 33,
        "totalFillupSeat": 33,
        "courseCredit": "3.0",
        "dayNo": "ST Day 2 (05-09-2024)"
    },
    {
        "id": 9935,
        "academicSectionId": 2312514,
        "courseId": 117771,
        "academicSessionId": 627124,
        "courseCode": "CSE422",
        "courseTitle": "ARTIFICIAL INTELLIGENCE",
        "courseDetails": "CSE422-[02]",
        "empName": "Md. Tanzim Reza",
        "empShortName": "TRZ",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Saturday(12:30 PM-01:50 PM-07H-26C),Thursday(12:30 PM-01:50 PM-07H-26C)",
        "classLabSchedule": "Saturday(12:30 PM-01:50 PM-07H-26C),Thursday(12:30 PM-01:50 PM-07H-26C),Wednesday(11:00 AM-12:20 PM-12F-31L),Wednesday(12:30 PM-01:50 PM-12F-31L)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 33,
        "availableSeat": 33,
        "totalFillupSeat": 33,
        "courseCredit": "3.0",
        "dayNo": "ST Day 2 (05-09-2024)"
    },
    {
        "id": 9936,
        "academicSectionId": 2312516,
        "courseId": 117771,
        "academicSessionId": 627124,
        "courseCode": "CSE422",
        "courseTitle": "ARTIFICIAL INTELLIGENCE",
        "courseDetails": "CSE422-[03]",
        "empName": "Syed Zamil Hasan Shoumo",
        "empShortName": "ZHS",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Sunday(08:00 AM-09:20 AM-09A-07C),Tuesday(08:00 AM-09:20 AM-09A-07C)",
        "classLabSchedule": "Saturday(11:00 AM-12:20 PM-10E-27L),Saturday(12:30 PM-01:50 PM-10E-27L),Sunday(08:00 AM-09:20 AM-09A-07C),Tuesday(08:00 AM-09:20 AM-09A-07C)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "ST Day 2 (05-09-2024)"
    },
]

cse220 = [
    {
        "id": 9614,
        "academicSectionId": 2312366,
        "courseId": 117658,
        "academicSessionId": 627124,
        "courseCode": "CSE220",
        "courseTitle": "DATA STRUCTURES",
        "courseDetails": "CSE220-[01]",
        "empName": "Avijit Biswas",
        "empShortName": "ABW",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Monday(11:00 AM-12:20 PM-09D-18C),Wednesday(11:00 AM-12:20 PM-09D-18C)",
        "classLabSchedule": "Monday(11:00 AM-12:20 PM-09D-18C),Sunday(11:00 AM-12:20 PM-09B-11L),Sunday(12:30 PM-01:50 PM-09B-11L),Wednesday(11:00 AM-12:20 PM-09D-18C)",
        "preRequisiteCourses": "CSE111,CSE230",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "Reserve Day 2 (01-09-2024)"
    },
    {
        "id": 9615,
        "academicSectionId": 2312370,
        "courseId": 117658,
        "academicSessionId": 627124,
        "courseCode": "CSE220",
        "courseTitle": "DATA STRUCTURES",
        "courseDetails": "CSE220-[02]",
        "empName": "Avijit Biswas",
        "empShortName": "ABW",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Monday(12:30 PM-01:50 PM-09D-18C),Wednesday(12:30 PM-01:50 PM-09D-18C)",
        "classLabSchedule": "Monday(12:30 PM-01:50 PM-09D-18C),Sunday(08:00 AM-09:20 AM-09E-21L),Sunday(09:30 AM-10:50 AM-09E-21L),Wednesday(12:30 PM-01:50 PM-09D-18C)",
        "preRequisiteCourses": "CSE111,CSE230",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "Reserve Day 2 (01-09-2024)"
    },
    {
        "id": 9616,
        "academicSectionId": 2312384,
        "courseId": 117658,
        "academicSessionId": 627124,
        "courseCode": "CSE220",
        "courseTitle": "DATA STRUCTURES",
        "courseDetails": "CSE220-[03]",
        "empName": "Priata Nowshin",
        "empShortName": "PRN",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Monday(09:30 AM-10:50 AM-09A-03C),Wednesday(09:30 AM-10:50 AM-09A-03C)",
        "classLabSchedule": "Monday(09:30 AM-10:50 AM-09A-03C),Sunday(08:00 AM-09:20 AM-09B-09L),Sunday(09:30 AM-10:50 AM-09B-09L),Wednesday(09:30 AM-10:50 AM-09A-03C)",
        "preRequisiteCourses": "CSE111,CSE230",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "Reserve Day 2 (01-09-2024)"
    },
]


cse370 = [
    {
        "id": 9900,
        "academicSectionId": 2312486,
        "courseId": 117732,
        "academicSessionId": 627124,
        "courseCode": "CSE370",
        "courseTitle": "DATABASE SYSTEMS",
        "courseDetails": "CSE370-[01]",
        "empName": "Najeefa Nikhat Choudhury",
        "empShortName": "NNC",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Sunday(08:00 AM-09:20 AM-07H-26C),Tuesday(08:00 AM-09:20 AM-07H-26C)",
        "classLabSchedule": "Monday(02:00 PM-03:20 PM-10E-25L),Monday(03:30 PM-04:50 PM-10E-25L),Sunday(08:00 AM-09:20 AM-07H-26C),Tuesday(08:00 AM-09:20 AM-07H-26C)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "ST Day 1 (04-09-2024)"
    },
    {
        "id": 9901,
        "academicSectionId": 2312490,
        "courseId": 117732,
        "academicSessionId": 627124,
        "courseCode": "CSE370",
        "courseTitle": "DATABASE SYSTEMS",
        "courseDetails": "CSE370-[02]",
        "empName": "Najeefa Nikhat Choudhury",
        "empShortName": "NNC",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Sunday(09:30 AM-10:50 AM-07H-26C),Tuesday(09:30 AM-10:50 AM-07H-26C)",
        "classLabSchedule": "Sunday(09:30 AM-10:50 AM-07H-26C),Tuesday(02:00 PM-03:20 PM-09E-21L),Tuesday(03:30 PM-04:50 PM-09E-21L),Tuesday(09:30 AM-10:50 AM-07H-26C)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "ST Day 1 (04-09-2024)"
    },
    {
        "id": 9902,
        "academicSectionId": 2312537,
        "courseId": 117732,
        "academicSessionId": 627124,
        "courseCode": "CSE370",
        "courseTitle": "DATABASE SYSTEMS",
        "courseDetails": "CSE370-[03]",
        "empName": "Najeefa Nikhat Choudhury",
        "empShortName": "NNC",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Monday(08:00 AM-09:20 AM-09D-18C),Wednesday(08:00 AM-09:20 AM-09D-18C)",
        "classLabSchedule": "Monday(08:00 AM-09:20 AM-09D-18C),Saturday(02:00 PM-03:20 PM-09E-21L),Saturday(03:30 PM-04:50 PM-09E-21L),Wednesday(08:00 AM-09:20 AM-09D-18C)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "ST Day 1 (04-09-2024)"
    },
    {
        "id": 9903,
        "academicSectionId": 2312602,
        "courseId": 117732,
        "academicSessionId": 627124,
        "courseCode": "CSE370",
        "courseTitle": "DATABASE SYSTEMS",
        "courseDetails": "CSE370-[04]",
        "empName": "Najeefa Nikhat Choudhury",
        "empShortName": "NNC",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Monday(09:30 AM-10:50 AM-09D-18C),Wednesday(09:30 AM-10:50 AM-09D-18C)",
        "classLabSchedule": "Monday(09:30 AM-10:50 AM-09D-18C),Tuesday(08:00 AM-09:20 AM-09E-22L),Tuesday(09:30 AM-10:50 AM-09E-22L),Wednesday(09:30 AM-10:50 AM-09D-18C)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "ST Day 1 (04-09-2024)"
    },
    {
        "id": 9904,
        "academicSectionId": 2312650,
        "courseId": 117732,
        "academicSessionId": 627124,
        "courseCode": "CSE370",
        "courseTitle": "DATABASE SYSTEMS",
        "courseDetails": "CSE370-[05]",
        "empName": "Shoaib Ahmed Dipu",
        "empShortName": "DPU",
        "deptName": "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING",
        "classSchedule": "Sunday(08:00 AM-09:20 AM-09H-32C),Tuesday(08:00 AM-09:20 AM-09H-32C)",
        "classLabSchedule": "Sunday(08:00 AM-09:20 AM-09H-32C),Tuesday(08:00 AM-09:20 AM-09H-32C),Wednesday(02:00 PM-03:20 PM-09F-24L),Wednesday(03:30 PM-04:50 PM-09F-24L)",
        "preRequisiteCourses": "CSE221",
        "defaultSeatCapacity": 38,
        "availableSeat": 38,
        "totalFillupSeat": 38,
        "courseCredit": "3.0",
        "dayNo": "ST Day 1 (04-09-2024)"
    },
]


listc = [cse220, cse370, cse422]

# print(f"{listc}/n===================================================/n")
routines = generate_routines(listc)

# print(routines)
i = 0
for routine in routines:
    i += 1
    for section in routine['courses']:
        print(section['courseDetails'], section['classSchedule'])
    print(f"Routine {i}: Total Duration = {routine['total_duration']} minutes, Total Days = {routine['total_days']}")
    print("---")
