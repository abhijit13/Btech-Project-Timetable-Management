#! /usr/bin/python

#globals to store all objects
all_teachers = []
all_venues = []
all_classes = []

#fetch this data from UI
subjects = {'dsa':3, 'ds':3, 'os':3, 'daa':3,'dbms':4}

days_per_week = None
lectures_per_day = None
daily_max = None
daily_min = None
class_max = None
class_min = None
weekly_max = None
weekly_min = None
#	each entry in tables is of the form :
#	attr1 attr2 None : here None means whole of this object
# 	attr1 attr2 b1 : here b1 means part of this object not whole Object 
# 	this is done for creating batches.
# 
# you can create  batches of teachers, venues or classes in similar way
# 	syc-b1 means b1 batch of syc class
# 	ac201-a1 means part of ac201 (this way classroom can be shared at same time)
# 	teacher-t1 means part of teacher (this way same teacher can teach on two classes at same time)
#

class ExistingEntry(Exception):
	def __init__(self, value):
		self.value = value

class ExtraWorkLoad(Exception):
	def __init__(self, value):
		self.value = value

class LimitForSubject(Exception):
	def __init__(self, value):
		self.value = value

class DailyWorkLoadLimit(Exception):
	def __init__(self, value):
		self.value = value

#Base class (rename it)
class Object(object):

	def __init__(self, name):	

		self.mat = [[None for i in range(0, lectures_per_day)] for i in range(0, days_per_week)]
		self.name = name

	#update existing object in case of days/week , lectures/day are changed.
	def resize_matrix(self):
		global days_per_week, lectures_per_day

		old_days = len(self.mat)
		old_lectures = len(self.mat[0])

		#fixed rows
		if old_days >= days_per_week:
			for i in range(days_per_week, old_days):
				del self.mat[-1]
		else :
			for i in range(old_days, days_per_week):
				self.mat.append([None for j in range(0, old_lectures)]) 
		
		#fixed cols
		if old_lectures >= lectures_per_day :
			for i in range(0, days_per_week):
				for j in range(lectures_per_day, old_lectures):
						del self.mat[i][-1]
		else:
			for i in range(0, days_per_week):
				for j in range(old_lectures, lectures_per_day):
					self.mat[i].append(None)

	def __repr__(self):
		return str(self.name)

	def __eq__(self, other):
		return self.name == other

	def __getitem__(self):
		return self.name

	def can_add(self, day, lecture):
		if self.mat[day][lecture] == None:
			return True
		else:
			return False

	def remove_entry(self, day, lecture, values=''):
		if len(values) > 1:
			batch = values[-1]
			a = [x for x in self.mat[day][lecture] if x[-1] == batch]
			if len(self.mat[day][lecture]) > 1:
				self.mat[day][lecture].remove(a[0])
				return False
			else:
				self.mat[day][lecture] = None
				return True	
		else:		
			self.mat[day][lecture] = None
			return True	

class Teacher(Object):
	def __init__(self, name):
		super(Teacher, self).__init__(name)
		self.max_work_load = weekly_max
		self.min_work_load = weekly_min
		self.max_daily_load = daily_max
		self.min_daily_load = daily_min
		self.current_work_load = 0

	def remove_entry(self, day, lecture, values=''):
		self.current_work_load  -= 1
		super(Teacher, self).remove_entry(day, lecture, values)

	def print_table(self):
		for i in range(0, days_per_week):
			print i, 
			for j in range(0, lectures_per_day):
				try:
					for data in self.mat[i][j]:
						print data[1], '-',data[0], 
					print " ",
				except:
					print "None\t",
			print
		print	

	def check_daily_workload(self):
		errors = []
		i = 0
		for row in self.mat:
			count = 0
			for entry in row:
				if entry != None:
					count += 1
			if count > self.max_daily_load:
				errors.append(i)
			i += 1
		if len(errors) > 0 :
			return errors
		else:
			return True

	def check_workload(self):
		#work load should be greater than min and less than max
		if self.current_work_load <= self.max_work_load and self.current_work_load >= self.min_work_load:
			return True
		else:
			return False

	def add_entry(self, venue, Class, day, lecture, sub, List=''):
		#check if we dont exceed max work load
		if self.current_work_load >= self.max_work_load:
			raise ExtraWorkLoad(self.max_work_load)
		
		temp = self.check_daily_workload()
		if temp != True:
			raise DailyWorkLoadLimit(temp)
		
		batch = None
		if len(List) > 1:
			batch = List[1]
		if self.can_add(day, lecture):
			self.mat[day][lecture] = [(venue, Class, sub, batch)]
		else:
			errors = []
			entries = self.mat[day][lecture]
			for entry in entries:
				if entry[-1] == None or entry[-1] == batch or batch == None:
					errors.append(entry)
			if len(errors) > 0:
				raise ExistingEntry(errors)				
			self.mat[day][lecture].append((venue, Class, sub, batch))

		self.current_work_load += 1

class Venue(Object):
	def __init__(self, name):
		super(Venue, self).__init__(name)

	def print_table(self):
		for i in range(0, days_per_week):
			print i,
			for j in range(0, lectures_per_day):
				try:
					for data in self.mat[i][j]:
						print data[1], '-', data[2],
					print " ",
				except:
					print "None\t",
			print
		print	

	def add_entry(self, teacher, Class, day, lecture, sub, List=''):
		batch = None
		if len(List) > 1:
			batch = List[1]
		if self.can_add(day, lecture):
			self.mat[day][lecture] = [(teacher, Class, sub, batch)]
		else:
			errors = []
			entries = self.mat[day][lecture]
			for entry in entries:
				if entry[-1] == None or entry[-1] == batch or batch == None:
					errors.append(entry)
			if len(errors) > 0:
				raise ExistingEntry(errors)
			self.mat[day][lecture].append((teacher, Class, sub, batch))

class Classes(Object):
	def __init__(self, name):
		super(Classes, self).__init__(name)
		self.subjects = {}
		self.batches = []
		self.max_work_load = class_max
		self.min_work_load = class_min
		self.current_work_load = 0
	

	def remove_entry(self, day, lecture, values=''):
		#reduce the no of lectures of that subject
		#for subject of a batch
		if len(values) > 1:
			batch = values[-1]
			a = [x for x in self.mat[day][lecture] if x[-1] == batch]
		#for subject of entire class
		else:
			a = self.mat[day][lecture]
		try:
			self.subjects[a[0][2]] -= 1
		except:
			pass #if its a lunch entry
		#remove entry from matrix				
		if super(Classes, self).remove_entry(day, lecture, values) == True :
			#reduce workload of the class
			try:
				self.current_work_load  -= 1
			except:
				pass #if its lunch entry
	
	def check_workload(self):
		#work load should be greater than min and less than max
		if self.current_work_load <= self.max_work_load and self.current_work_load >= self.min_work_load:
			return True
		else:
			return False

	def print_table(self):
		for i in range(0, days_per_week):
			print i, 
			for j in range(0, lectures_per_day):
				try:
					for data in self.mat[i][j]:
						if 'LUNCH' in data :
							print data[0], '-', data[1],
						else:
							print data[2], '-', data[1],
					print " ",
				except:
					print "None\t",
			print
		print	

	#Constraints (compulsary lunch break) 
	def valid_lunch_break(self):
		errors = []
		for row in self.mat:
			if [('LUNCH', None)] in row:
				continue
			else:
				entries = []
				for entry in row:
					if entry != None:
						# print entry, 'yo'
						entries.extend(entry)

				if len(entries) != 0:
					if len(self.batches) != 0 : 
						for batch in self.batches:
							# print ('LUNCH', batch)
							if ('LUNCH', batch) not in entries:
								# print ('LUNCH', batch), 'not in ' ,entries
								if batch not in errors:
									errors.append(batch)
					else:
						batch = None
						if ('LUNCH', batch) not in entries:
							# print ('LUNCH', batch), 'not in ' ,entries
							if self.name not in errors:
								errors.append(self.name)

	#every day should have (LUNCH, batch) entry for all batches else its like that day doesnt have
	#lunch for that batch, None is treated as busy slot

		if len(errors) > 0:
			return errors
		else:
			return True

	def add_lunch(self, day, lecture, batch):
		if len(batch) > 1:
			batch = batch[1]
			if batch not in self.batches:
				self.batches.append(batch)
		else:
			batch = None 
		if self.can_add(day, lecture):
			self.mat[day][lecture] = [('LUNCH', batch)]
		else:
			errors = []
			entries = self.mat[day][lecture]
			for entry in entries:
				if entry[-1] == None or entry[-1] == batch or batch == None:
					errors.append(entry)
			if len(errors) > 0:
				raise ExistingEntry(errors)		
			self.mat[day][lecture].append(('LUNCH', batch))

	def add_entry(self, teacher, venue, day, lecture, sub, List=''):
		#check if we dont exceed max work load
		if self.current_work_load >= self.max_work_load:
			raise ExtraWorkLoad(self.max_work_load)
		if sub in subjects:
			if sub in self.subjects:
				if self.subjects[sub] >= subjects[sub]:
					raise LimitForSubject(subjects[sub])
				else:
					self.subjects[sub] += 1;
			else:
				self.subjects[sub] = 1;
		batch = None
		if len(List) > 1:
			batch = List[1]
			if batch not in self.batches:
				self.batches.append(batch)

		if self.can_add(day, lecture):
			self.mat[day][lecture] = [(teacher, venue, sub, batch)]
		else:
			entries = self.mat[day][lecture]
			errors = []
			for entry in entries:
				if entry[-1] == None or entry[-1] == batch or batch == None:
					errors.append(entry)
			if len(errors) > 0:
				raise ExistingEntry(errors)
			self.mat[day][lecture].append((teacher, venue, sub, batch))
		
		if batch == None:
			self.current_work_load += 1
		else:
			temp = [t[-1] for t in self.mat[day][lecture]]
			for batch in self.batches:
				if batch not in temp:
					return
			self.current_work_load += 1			


def get_object(List, name, BaseClass=None):
	entries = [t for t in List if t.name == name]
	entry = None
	if len(entries) == 0 :
		if BaseClass != None:
			entry = BaseClass(name)
			List.append(entry)
	else:
		entry = entries[0]
	return entry


def insert_entry(teacher, venue, Class, sub, day, lecture):
	global all_teachers, all_venues, all_classes
	teacher = teacher.split('-')
	teacher[0] = get_object(all_teachers, teacher[0], Teacher)
	venue = venue.split('-')
	venue[0] = get_object(all_venues, venue[0], Venue)
	Class = Class.split('-')
	Class[0] = get_object(all_classes, Class[0], Classes)

	try:
		teacher[0].add_entry(venue[0], Class[0], day, lecture, sub, teacher)
	except ExistingEntry as e:
		print 'Entry already Exists '
		print e.value
		raise 	
	except ExtraWorkLoad as e:
		print 'Teacher has got Extra WorkLoad '
		print e.value
		raise
	except DailyWorkLoadLimit as e:
		print 'Daily Limit for Teacher crossed on :'
		print e.value
		raise
	else:
		try:
			venue[0].add_entry(teacher[0], Class[0], day, lecture, sub, venue)
		except ExistingEntry as e:
			print 'Entry already Exists '
			print e.value
			teacher[0].remove_entry(day, lecture, teacher)
			raise
		else:
			try:
				Class[0].add_entry(teacher[0], venue[0], day, lecture, sub, Class)
			except ExistingEntry as e:
				print 'Entry already Exists '
				print e.value
				venue[0].remove_entry(day, lecture, venue)
				teacher[0].remove_entry(day, lecture, teacher)
				raise
			except ExtraWorkLoad as e:
				print ' Class has got Extra WorkLoad '
				print e.value
				venue[0].remove_entry(day, lecture, venue)
				teacher[0].remove_entry(day, lecture, teacher)
				raise
			except LimitForSubject as e:
				print ' Lecture Limit for Subject reached '
				print e.value
				venue[0].remove_entry(day, lecture, venue)
				teacher[0].remove_entry(day, lecture, teacher)
				raise

def insert_lunch(batch, day, lecture):
	global all_classes
	batch = batch.split('-')
	batch[0] = get_object(all_classes, batch[0], Classes)
	try:
		batch[0].add_lunch(day, lecture, batch)
	except ExistingEntry as e:
		print 'Entry already exists '
		print e.value

def remove_lunch(Class, day, lecture):
	global all_classes
	Class = Class.split('-')
	Class[0] = get_object(all_classes, Class[0], Classes)
	Class[0].remove_entry(day, lecture, Class)
	Class[0].current_work_load += 1 	#very dirty fix this; dont change attributes of object from non member function.

# def print_table(choice):
# 	global all_classes, all_teachers, all_venues

# 	teacher = get_object(all_teachers, choice)
# 	try:
# 		teacher.print_table()
# 	except:
# 		venue = get_object(all_venues, choice)
# 		try:
# 			venue.print_table()
# 		except:
# 			Class = get_object(all_classes, choice)
# 		try:
# 			Class.print_table()
# 			print 'Lunch Break for Class:'
# 			print Class.valid_lunch_break()
# 		except:
# 			pass

def print_all_tables():
	global all_teachers, all_classes, all_venues

	print 'Teachers:'
	for teacher in all_teachers:
		print teacher
		teacher.resize_matrix()
		teacher.print_table()

	print 'Classes:'
	for Class in all_classes:
		print Class
		Class.resize_matrix()
		res = Class.valid_lunch_break()
		if res == True :
			print 'Valid Lunch break for Class'
		else:
			print 'Invalid Lunch break'
			print res
		Class.print_table()

	print 'Venues:'
	for venue in all_venues:
		print venue
		venue.resize_matrix()
		venue.print_table()

	print days_per_week, lectures_per_day


def remove_all(teacher, venue, Class, day, lecture):
	global all_teachers, all_venues, all_classes
	teacher = teacher.split('-')
	teacher[0] = get_object(all_teachers, teacher[0], Teacher)
	venue = venue.split('-')
	venue[0] = get_object(all_venues, venue[0], Venue)
	Class = Class.split('-')
	Class[0] = get_object(all_classes, Class[0], Classes)

	teacher[0].remove_entry(day, lecture, teacher)
	venue[0].remove_entry(day, lecture, venue)
	Class[0].remove_entry(day, lecture, Class)

# poor argument fetching - change the way its done
def main(args): 
	global days_per_week, lectures_per_day
	args = args.split()
	print args
	if len(args) == 6:
		try:
			insert_entry(args[0], args[1], args[2], args[3], int(args[4]), int(args[5]))
		except:
			raise
	elif len(args) == 4:
		insert_lunch(args[1], int(args[2]), int(args[3]))
	elif len(args) == 5:
		days_per_week = int(args[1])
		lectures_per_day = int(args[2])
		print days_per_week, lectures_per_day
	else:
		args = args[0].split('#')
		if len(args) == 6:
			remove_all(args[0], args[1], args[2], int(args[4]), int(args[5]))
		else:
			remove_lunch(args[1], int(args[2]), int(args[3]))


	# while(True):
	# 	choice = input('choice>>')
	# 	if choice == 1:
	# 		print 'Teacher, Venue, Class, day, lecture'
	# 		t = raw_input()
	# 		v = raw_input()	
	# 		c = raw_input()	
	# 		d = input()	
	# 		l = input()	
	# 		insert_entry(t, v, c, d, l)

	# 	elif choice == 2:
	# 		print 'day, lecture, batch'
	# 		d = input()
	# 		l = input()
	# 		batch = raw_input()
	# 		insert_lunch(d, l, batch)

	# 	elif choice == 3:
	# 		print_all_tables()

	# 	else:	
	# 		choice = raw_input('which table to show\n')
	# 		print_table(choice)

if __name__ == "__main__":
	main()