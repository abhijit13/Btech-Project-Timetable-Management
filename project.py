#! /usr/bin/python
import globaldata

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
class BaseStructure(object):

	def __init__(self, name):	

		self.mat = [[None for i in range(0, globaldata.lectures_per_day)] for i in range(0, globaldata.days_per_week)]
		self.name = name

	#update existing object in case of days/week , lectures/day are changed.
	def resize_matrix(self):

		old_days = len(self.mat)
		old_lectures = len(self.mat[0])

		#fixed rows
		if old_days >= globaldata.days_per_week:
			for i in range(globaldata.days_per_week, old_days):
				del self.mat[-1]
		else :
			for i in range(old_days, globaldata.days_per_week):
				self.mat.append([None for j in range(0, old_lectures)]) 
		
		#fixed cols
		if old_lectures >= globaldata.lectures_per_day :
			for i in range(0, globaldata.days_per_week):
				for j in range(globaldata.lectures_per_day, old_lectures):
						del self.mat[i][-1]
		else:
			for i in range(0, globaldata.days_per_week):
				for j in range(old_lectures, globaldata.lectures_per_day):
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

class Teacher(BaseStructure):
	def __init__(self, name, weekly_max=globaldata.weekly_max, daily_max=globaldata.daily_max):
		super(Teacher, self).__init__(name)
		self.max_work_load = weekly_max
		self.min_work_load = globaldata.weekly_min
		self.max_daily_load = daily_max
		self.min_daily_load = globaldata.daily_min
		self.current_work_load = 0

	def remove_entry(self, day, lecture, values=''):
		self.current_work_load  -= 1
		super(Teacher, self).remove_entry(day, lecture, values)

	# def print_table(self):
	# 	for i in range(0, globaldata.days_per_week):
	# 		print i, 
	# 		for j in range(0, globaldata.lectures_per_day):
	# 			try:
	# 				for data in self.mat[i][j]:
	# 					print data[1], '-',data[0], 
	# 				print " ",
	# 			except:
	# 				print "None\t",
	# 		print
	# 	print	

	def check_daily_workload(self):
		errors = []
		i = 0
		for row in self.mat:
			count = 0
			for entry in row:
				if entry != None:
					count += 1
			if count >= self.max_daily_load:
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
			raise ExtraWorkLoad([(self.name, self.max_work_load)])
		
		temp = self.check_daily_workload()
		if temp != True and day in temp:
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

class Venue(BaseStructure):
	def __init__(self, name, capacity=globaldata.venueCapacity, placeholder=None):
		super(Venue, self).__init__(name)
		self.capacity = capacity

	def print_table(self):
		for i in range(0, globaldata.days_per_week):
			print i,
			for j in range(0, globaldata.lectures_per_day):
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

class Classes(BaseStructure):
	def __init__(self, name,capacity=globaldata.classCapacity, placeholder=None):
		super(Classes, self).__init__(name)
		self.subjects = {}
		self.batches = []
		self.max_work_load = globaldata.class_max
		self.min_work_load = globaldata.class_min
		self.current_work_load = 0
		self.capacity = capacity
	

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
		for i in range(0, globaldata.days_per_week):
			print i, 
			for j in range(0, globaldata.lectures_per_day):
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
									i = self.mat.index(row)
									day = globaldata.rowLabels[i]
									errors.append({batch:day})
					else:
						batch = None
						if ('LUNCH', batch) not in entries:
							# print ('LUNCH', batch), 'not in ' ,entries
							if self.name not in errors:
								i = self.mat.index(row)
								errors.append({self.name:globaldata.rowLabels[i]})

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
			raise ExtraWorkLoad([(self.name, self.max_work_load)])
		if sub in globaldata.subjects:
			if sub in self.subjects:
				if self.subjects[sub] >= globaldata.subjects[sub]:
					raise LimitForSubject(globaldata.subjects[sub])
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


def get_object(List, name, BaseClass=None, batch=None):
	entries = [t for t in List if t.name == name]
	entry = None
	if len(entries) == 0 :
		if batch != None and len(batch) != 0:
			listname = name + '-' + batch[0]
		else :
			listname = name

		if BaseClass == Teacher:
			i = globaldata.teacher_shortnames.index(listname)
			entry = BaseClass(name, globaldata.teacher_weeklymax[i-1], globaldata.teacher_dailymax[i-1])
			List.append(entry)
		elif BaseClass == Venue:
			i = globaldata.venue_shortnames.index(listname)
			entry = BaseClass(name, globaldata.venue_capacity[i-1])
			List.append(entry)
		elif BaseClass == Classes:
			i = globaldata.class_shortnames.index(listname)
			entry = BaseClass(name, globaldata.class_capacity[i-1])
			List.append(entry)
	else:
		entry = entries[0]
	return entry


def push_object(listname, typeOf):

	if typeOf == 'Teacher':
		i = globaldata.teacher_shortnames.index(listname)
		entry = Teacher(listname, globaldata.teacher_weeklymax[i-1], globaldata.teacher_dailymax[i-1])
		globaldata.all_teachers.append(entry)
	if typeOf == 'Venue':
		i = globaldata.venue_shortnames.index(listname)
		entry = Venue(listname, globaldata.venue_capacity[i-1])		
		globaldata.all_venues.append(entry)
	if typeOf == 'Class':
		i = globaldata.class_shortnames.index(listname)
		entry = Classes(listname, class_capacity[i-1])		
		globaldata.all_classes.append(entry)

def insert_entry(teacher, venue, Class, sub, day, lecture):
	t = teacher
	v = venue
	C = Class
	teacher = teacher.split('-')
	teacher[0] = get_object(globaldata.all_teachers, teacher[0], Teacher, teacher[1:])
	venue = venue.split('-')
	venue[0] = get_object(globaldata.all_venues, venue[0], Venue, venue[1:])
	Class = Class.split('-')
	Class[0] = get_object(globaldata.all_classes, Class[0], Classes, Class[1:])

	try:
		teacher[0].add_entry(v, C,  day, lecture, sub, teacher)
	except ExistingEntry as e:
		print 'Entry already Exists '
		print e.value
		raise e	
	except ExtraWorkLoad as e:
		print 'Teacher has got Extra WorkLoad '
		print e.value
		raise e
	except DailyWorkLoadLimit as e:
		print 'Daily Limit crossed for :', e.value
		raise e
	else:
		try:
			venue[0].add_entry(t, C, day, lecture, sub, venue)
		except ExistingEntry as e:
			print 'Entry already Exists '
			print e.value
			teacher[0].remove_entry(day, lecture, teacher)
			raise e
		else:
			try:
				Class[0].add_entry(t, v, day, lecture, sub, Class)
			except ExistingEntry as e:
				print 'Entry already Exists '
				print e.value
				venue[0].remove_entry(day, lecture, venue)
				teacher[0].remove_entry(day, lecture, teacher)
				raise e
			except ExtraWorkLoad as e:
				print ' Class has got Extra WorkLoad '
				print e.value
				venue[0].remove_entry(day, lecture, venue)
				teacher[0].remove_entry(day, lecture, teacher)
				raise e
			except LimitForSubject as e:
				print ' Lecture Limit for Subject reached '
				print e.value
				venue[0].remove_entry(day, lecture, venue)
				teacher[0].remove_entry(day, lecture, teacher)
				raise e

def insert_lunch(batch, day, lecture):
	batch = batch.split('-')
	batch[0] = get_object(globaldata.all_classes, batch[0], Classes, batch[1:])
	try:
		batch[0].add_lunch(day, lecture, batch)
	except ExistingEntry as e:
		print 'Entry already exists '
		print e.value
		raise e

def remove_lunch(Class, day, lecture):
	Class = Class.split('-')
	Class[0] = get_object(globaldata.all_classes, Class[0], Classes, Class[1:])
	Class[0].remove_entry(day, lecture, Class)
	Class[0].current_work_load += 1 	#very dirty fix this; dont change attributes of object from non member function.

# def print_table(choice):

# 	teacher = get_object(globaldata.all_teachers, choice)
# 	try:
# 		teacher.print_table()
# 	except:
# 		venue = get_object(globaldata.all_venues, choice)
# 		try:
# 			venue.print_table()
# 		except:
# 			Class = get_object(globaldata.all_classes, choice)
# 		try:
# 			Class.print_table()
# 			print 'Lunch Break for Class:'
# 			print Class.valid_lunch_break()
# 		except:
# 			pass

def print_all_tables():
	print 'Teachers:'
	for teacher in globaldata.all_teachers:
		print teacher
		teacher.resize_matrix()
		teacher.print_table()

	print 'Classes:'
	for Class in globaldata.all_classes:
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
	for venue in globaldata.all_venues:
		print venue
		venue.resize_matrix()
		venue.print_table()

	print globaldata.days_per_week, globaldata.lectures_per_day

def FindVenueUtilization():
	result = {}
	for v in globaldata.all_venues:
		res = []
		total = 0
		# print len(v.mat)
		for day in range(len(v.mat)):
			count = 0
			for entry in v.mat[day]:
				if entry != None:
					count += 1
			res.append(count)
			total += count
		res.append(str(total) + ' / ' + str(len(v.mat) * len(v.mat[0])))
		result[v.name] = res
	# print result
	return result

def remove_all(teacher, venue, Class, day, lecture):
	teacher = teacher.split('-')
	teacher[0] = get_object(globaldata.all_teachers, teacher[0], Teacher,teacher[1:])
	venue = venue.split('-')
	venue[0] = get_object(globaldata.all_venues, venue[0], Venue, venue[1:])
	Class = Class.split('-')
	Class[0] = get_object(globaldata.all_classes, Class[0], Classes, Class[1:])

	teacher[0].remove_entry(day, lecture, teacher)
	venue[0].remove_entry(day, lecture, venue)
	Class[0].remove_entry(day, lecture, Class)

# poor argument fetching - change the way its done
def main(args): 
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
		globaldata.days_per_week = int(args[1])
		globaldata.lectures_per_day = int(args[2])
		print globaldata.days_per_week, globaldata.lectures_per_day
	else:
		args = args[0].split('#')
		if len(args) == 6:
			remove_all(args[0], args[1], args[2], int(args[4]), int(args[5]))
		else:
			remove_lunch(args[1], int(args[2]), int(args[3]))


if __name__ == "__main__":
	pass
	# main()
	# main("ABHI AC201 SYC DSA 0 1")