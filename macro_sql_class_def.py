import re
import io
import os

class Macro:
	'Macro class, with children marco list'
	
	# data folder
	dataFolder = "C:\workspace\python_workspace"
	
	# re
	p = re.compile('([ \\d]+)\\,([ \\d]+)\\,')
	
	# hold all parent macro
	allowedPid = (1, 2 ,5 ,241 ,333 ,382 ,386)
	pidList = []
	stmtList = []
	
	
	
	def __init__(self, id, stmt):
		self.id = id
		self.stmt = stmt
		childs = []
	
	@classmethod
	def parse(cls):
		# C:\workspace\python_workspace\macro_sql.txt
		dataFile = os.path.join(cls.dataFolder, "macro_sql.txt")
		with io.open(dataFile, "r", encoding="utf8") as file:
			for line in file:
				cls.addStmt(line)
	
	@classmethod
	def save(cls):
		resultFile = os.path.join(cls.dataFolder, "result.txt")
		with io.open(resultFile, "w", encoding="utf8") as file:
			file.writelines(cls.stmtList)
			
		print "Done"
	
	@classmethod
	def addStmt(cls, stmt):
		'''
		Add statement, parse out pid and id.
		find parent by pid in pidList:
			if pid exist in pidList:
				add stmt
			if not exist:
				check if exist in allowedPid:
					if exist: 
						add pid & stmt
					else:
						do nothing
		'''
		ids = cls.findIds(stmt);
		id = ids[0]
		pid = ids[1]
	
		if pid in cls.pidList:
			# add pid & stmt
			cls.pidList.append(id)
			cls.stmtList.append(stmt)
			#print ids, "in pidList", cls.pidList
		else:
			if pid in cls.allowedPid:
				# add pid & stmt
				cls.pidList.append(pid)
				cls.pidList.append(id)
				
				cls.stmtList.append(stmt)
				
				#print ids, "not in pidlist, but in allowedPid", cls.allowedPid, "appended", cls.pidList
			#else:
				#print ids, "do nothing", cls.allowedPid, cls.pidList
	
	
	
	@classmethod
	def findIds(cls, stmt):
		'''
		
		'''
		result = cls.p.findall(stmt)
		result_tuple = result[0]
		id = int(result_tuple[0])
		pid = int(result_tuple[1])
		
		return id, pid
		
		
		