import re
import io
import os

class Macro:
	'Macro class, with children marco list'
	
	# data folder
	dataFolder = "C:\workspace\python_workspace"
	
	# re
	p = re.compile('([ \\d]+)\\,([ \\d]+)\\,')
	
	# second level parent
	allowedPid = (2 ,5 ,241 ,333 ,382 ,386)
	pidList = []
	stmtList = []
	
	
	# root of macro tree
	rootMacro = None;
	
	
	def __repr__(self):
		return "%s -> %s"%(self.id, self.childMacroList)
		
	
	def __init__(self, id, stmt):
		self.id = id
		self.stmt = stmt
		self.childMacroList = []
		
	def addChild(self, childMacro):
		self.childMacroList.append(childMacro)
		
	def findById(self, id):
		# find in child first, actually this does no matters
		for c in self.childMacroList:
			node = c.findById(id)
			if node is not None:
				return node
	
		# check self
		if(self.id == id):
			return self
		
	def getStmtList(self):
		result = [];
		
		# add my stmt
		result.append(self.stmt)
		
		# append child stmt
		for c in self.childMacroList:
			result.extend(c.getStmtList())
		
		return result
	
	@classmethod
	def topStmt(cls, *ids):
		result = []
		if len(ids) > 0:
			for id in ids:
				node = cls.rootMacro.findById(id)
				result.append(node)
		else:
			result.append(cls.rootMacro)
			
		return result
		
	
	@classmethod
	def parse(cls):
		# create root macro
		cls.rootMacro = Macro(1, None);
		
		# C:\workspace\python_workspace\macro_sql.txt
		dataFile = os.path.join(cls.dataFolder, "macro_sql.txt")
		with io.open(dataFile, "r", encoding="utf8") as file:
			for line in file:
				cls.addStmt(line)
				
	
	@classmethod
	def save(cls, macroList):
		# collect stmt list
		stmtList = []
		for m in macroList:
			stmtList.extend(m.getStmtList())
		
	
		resultFile = os.path.join(cls.dataFolder, "result.txt")
		with io.open(resultFile, "w", encoding="utf8") as file:
			file.writelines(stmtList)
			
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
	
		childMacro = Macro(id, stmt)
	
		# find parent 
		parent = cls.rootMacro.findById(pid)
		
		if parent is not None:
			parent.addChild(childMacro)
		else:
			print "pid Not found:", pid
	
	

	
	
	
	@classmethod
	def findIds(cls, stmt):
		'''
		
		'''
		result = cls.p.findall(stmt)
		result_tuple = result[0]
		id = int(result_tuple[0])
		pid = int(result_tuple[1])
		
		return id, pid
		
		
		