from django.db import models

class CourseSection(models.Model):
    id = models.IntegerField(primary_key=True)
    academicSectionId = models.IntegerField()
    courseId = models.IntegerField()
    academicSessionId = models.IntegerField()
    courseCode = models.CharField(max_length=10)
    courseTitle = models.CharField(max_length=255)
    courseDetails = models.CharField(max_length=255)
    empName = models.CharField(max_length=255)
    empShortName = models.CharField(max_length=10)
    deptName = models.CharField(max_length=255)
    classSchedule = models.TextField()
    classLabSchedule = models.TextField()
    preRequisiteCourses = models.TextField(blank=True)
    defaultSeatCapacity = models.IntegerField()
    availableSeat = models.IntegerField()
    totalFillupSeat = models.IntegerField()
    courseCredit = models.DecimalField(max_digits=3, decimal_places=1)
    dayNo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.courseCode} - {self.id}"
