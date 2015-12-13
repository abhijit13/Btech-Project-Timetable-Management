#! /usr/bin/python

#globals to store all objects
all_teachers = []
all_venues = []
all_classes = []
days_per_week = 7
lectures_per_day = 10

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

#we'll use it later maybe
class ExtraWorkLoad(Exception):
	def __init__(self, value):
		self.value = value

#Base class (rename it)
class Object(object):
	def __init__(self, name):	

		self.mat = [[None for i in range(0, lectures_per_day)] for i in range(0, days_per_week)]
		self.name = name

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
			else:
				self.mat[day][lecture] = None	
		else:		
			self.mat[day][lecture] = None


class Teacher(Object):
	def __init__(self, name, load=5):
		super(Teacher, self).__init__(name)
		self.max_work_load = load

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

	#work on it later (constraints)	
	def check_workload(self):
		count = 0
		for row in self.mat:
			for entry in row:
				if entry != None:
					count += 1
		if count < self.max_work_load:
			return True
		else:
			return False

	def add_entry(self, venue, Class, day, lecture, sub, List=''):

		if self.check_workload() == False:
			raise ExtraWorkLoad(self.max_work_load)
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

class Venue(Object):
	def __init__(self, name):
		super(Venue, self).__init__(name)

	def print_table(self):
		for i in range(0, days_per_week):
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
		self.batches = []

	def print_table(self):
		for i in range(0, days_per_week):
			print i, 
			for j in range(0, lectures_per_day):
				try:
					for data in self.mat[i][j]:
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
						entries.extend(entry)

				for batch in self.batches:
					print ('LUNCH', batch)

					if ('LUNCH', batch) not in entries:
						if batch not in errors:
							errors.append(batch)

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

def insert_lunch(batch, day, lecture):
	global all_classes
	batch = batch.split('-')
	batch[0] = get_object(all_classes, batch[0], Classes)
	try:
		batch[0].add_lunch(day, lecture, batch)
	except ExistingEntry as e:
		print 'Entry already exists '
		print e.value

def print_table(choice):
	global all_classes, all_teachers, all_venues

	teacher = get_object(all_teachers, choice)
	try:
		teacher.print_table()
	except:
		venue = get_object(all_venues, choice)
		try:
			venue.print_table()
		except:
			Class = get_object(all_classes, choice)
		try:
			Class.print_table()
			print 'Lunch Break for Class:'
			print Class.valid_lunch_break()
		except:
			pass

def print_all_tables():
	global all_teachers, all_classes, all_venues

	print 'Teachers:'
	for teacher in all_teachers:
		print teacher
		teacher.print_table()

	print 'Classes:'
	for Class in all_classes:
		print Class
		Class.print_table()

	print 'Venues:'
	for venue in all_venues:
		print venue
		venue.print_table()

def remove_lunch(Class, day, lecture):
	global all_classes
	Class = Class.split('-')
	Class[0] = get_object(all_classes, Class[0], Classes)

	Class[0].remove_entry(day, lecture, Class)

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
	args = args.split()
	print args
	if len(args) == 6:
		try:
			insert_entry(args[0], args[1], args[2], args[3], int(args[4]), int(args[5]))
		except:
			raise
	elif len(args) == 4:
		insert_lunch(args[1], int(args[2]), int(args[3]))
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