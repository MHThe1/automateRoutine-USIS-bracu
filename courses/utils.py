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
        # Parse classLabSchedule instead of classSchedule
        schedule = parse_schedule(course['classLabSchedule'])
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

# Parse the combined classLabSchedule into a dictionary
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
    
    return schedule



# Generate all possible routines without time conflicts
def generate_routines(courses, course_count, page=1, page_size=10, min_days=None, max_days=7):
    all_combinations = list(product(*courses))
    routines = []
    for combination in all_combinations:
        conflict = False
        for i in range(len(combination)):
            for j in range(i + 1, len(combination)):
                if has_time_conflict(
                    parse_schedule(combination[i]['classLabSchedule']),
                    parse_schedule(combination[j]['classLabSchedule'])
                ):
                    conflict = True
                    break
            if conflict:
                break
        if not conflict:
            total_duration, total_days = calculate_total_duration(combination)
            # print(len(courses), len(combination))
            # print(courses, combination)
            if (min_days is None or total_days >= min_days) and (max_days is 7 or total_days <= max_days) and (course_count == len(combination)):
                routines.append({
                    'courses': combination,
                    'total_duration': total_duration,
                    'total_days': total_days
                })
    sorted_routines = sorted(routines, key=lambda x: (x['total_days'], x['total_duration']))

    # Implement pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_routines = sorted_routines[start_index:end_index]

    return {
        'routines': paginated_routines,
        'total_count': len(sorted_routines)
    }
