header1 = ''
header2 = ''
header3 = ''

clipboard = ''
#globals to store all objects
all_teachers = []
all_venues = []
all_classes = []

subjects = {}

days_per_week = 0
lectures_per_day = 0
daily_max = 0
daily_min = 0
class_max = 0
class_min = 0
weekly_max = 0
weekly_min = 0
venueCapacity = 0
classCapacity = 0

rowLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
colLabels = ['9-10','10-11', '11-12', '12-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7']

teacher_fullnames = []
teacher_shortnames = ['ADD NEW']
teacher_weeklymax = []
teacher_dailymax = []

venue_fullnames = []
venue_shortnames = ['ADD NEW']
venue_capacity = []

class_fullnames = []
class_shortnames = ['ADD NEW']
class_capacity = []

subject_fullnames = []
subject_shortnames = ['ADD NEW']
subject_credits = []

teacher_class_map = {}
class_teacher_map = {}
teacher_subject_map = {}
subject_teacher_map = {}
venue_class_map = {}
class_venue_map = {}