import json
import pprint

ObjectData = op('ObjectData').module.ObjectData

class Position:

	def __init__(self):
	
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		
		

class MyClass(ObjectData):

	c = 3 # class attribute
	d = Position()
	StestOP = op('level1')
	StestPar = StestOP.par.opacity
	#Spos3 = Position()
	#SposList = [Position(), Position()]
	#SposTuple = (Position(), Position())
	#SposDict = {'pos1': Position(), 'pos2': Position()}
	#SposDict2 = {'pos1': SposList, 'pos2': SposTuple}
	#SposList2 = [SposTuple, SposDict2]	
	

	def __init__(self):
		ObjectData.__init__(self)
		self.a = 0 # instance attribute
		self.b = 1
		self.l = [0, 1, 2]
		self.basicDict = {'a': 0, 'b': 1, 'c': 2}
		self._p = None
		self._p2 = None
		
		self.pos = Position()
		self.pos.x = Position()
		self.posList = [Position(), Position()]
		self.posList1 = [Position(), Position()]
		self.posList2 = [self.posList, self.posList1]
		self.posTuple = (Position(), Position())
		self.posTuple2 = (self.posList, self.posTuple)
		self.posDict = {'pos1': Position(), 'pos2': Position()}
		self.posTuple3 = (self.posDict, self.posTuple)
		self.posDict2 = {'pos1': self.posList, 'pos2': self.posTuple2}
		self.posList2 = [self.posTuple2, self.posDict]
		self.posDict3 = {'pos1': self.l, 'pos2': self.l}

		self.matrix = tdu.Matrix()
		self.matrix2 = tdu.Matrix().vals
		self.testOP = op('level1')
		self.testOPPath = self.testOP.path
		self.testPar = self.testOP.par.opacity

		# should now be only implemented as properties so 
		# SetAttrs() doens't overwrite with value
		self.testPar2 = self.testOP.par.opacity.eval()

		# to recall actual par set par as attribute
		self.testPar3 = self.testOP.par.brightness1
				
	def myfunc(self):      # non-static method
		return self.a		
	
	@staticmethod
	def mystatic():        # static method
		return MyClass.a
		
	@classmethod
	def myclass():        # class method
		return MyClass.b		
		
	@property # class attribute
	def p(self):
		return self._p
		
	@p.setter
	def p(self, value):
		self._p = value
	'''
	@property # class attribute
	def p2(self):
		return self._p2'''
		
print('///////////////////////////////////////////////////////////////////////////////')
print('\nInitialize inst1\n')
print('///////////////////////////////////////////////////////////////////////////////')
print()			
inst1 = MyClass()

# set some values in inst1
inst1.a = 5
inst1.b = 6
inst1.p =  Position()
inst1.p.x = 4
inst1.pos.x = 3.0
inst1.pos.y = 4.0
inst1.pos.z = Position()
inst1.pos.z.x = 55

inst1.posList[0].x = 6.0
inst1.posList[0].y = 6.1
inst1.posList[0].z = 6.2

inst1.posTuple[0].x = 7.0
inst1.posTuple[0].y = 7.1
inst1.posTuple[0].z = 7.2

inst1.posDict['pos2'].x = 8.0
inst1.posDict['pos2'].y = 8.1
inst1.posDict['pos2'].z = 8.2

# serialize inst1 non callable attributes
inst1Data = inst1.GetAttrs()
pprint.pprint(inst1Data)
inst1DataJSON = json.dumps(inst1Data)

print()
print('///////////////////////////////////////////////////////////////////////////////')
print('///////////////////////////////////////////////////////////////////////////////')
print('\nInitialize inst2\n')
print('///////////////////////////////////////////////////////////////////////////////')

inst2 = MyClass()

# delete some attributes in inst2
delattr(inst2, 'a')
delattr(inst2, 'b')
delattr(inst2, 'basicDict')
delattr(inst2, 'pos')
delattr(inst2, 'posList2')
delattr(inst2, 'posList1')
delattr(inst2, 'posList')
delattr(inst2, 'posTuple')
delattr(inst2, 'posTuple2')
delattr(inst2, 'posDict')
delattr(inst2, 'posDict2')
delattr(inst2, 'posTuple3')
#pprint.pprint(inst2.GetAttrs())

print('\nSet Inst2\n')	
print('///////////////////////////////////////////////////////////////////////////////')	
# set attributes of inst2 with serialized attributes of inst1	
inst2.SetAttrs(json.loads(inst1DataJSON)) 


print('\nGet Inst2\n')
print('///////////////////////////////////////////////////////////////////////////////')
print()		
# get and print updated inst2 attributes
inst2Data = inst2.GetAttrs()
pprint.pprint(inst2Data)

# are inst1 and inst2 attribute equal?
print()
print('///////////////////////////////////////////////////////////////////////////////')
instAttrsEqual = inst1.GetAttrs() == inst2.GetAttrs()
print('\ninst1Attrs == inst2Attrs:', instAttrsEqual)

if not instAttrsEqual:

	for attrName, attrVal in inst1Data.items():

		inst2AttrVal = inst2Data[attrName]

		if attrVal != inst2AttrVal:

			print(attrName)
			print('inst1 attr', attrName)
			pprint.pprint(attrVal)
			print('inst2 attr', attrName)
			pprint.pprint(inst2AttrVal)
