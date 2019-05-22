ObjectData = op('ObjectData').module.ObjectData

class Position:

	def __init__(self):
	
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		
		

class MyClass(ObjectData):

	c = 3 # class attribute
	d = Position()
	#pos3 = Position()
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
		self.dict = {'a': 0, 'b': 1, 'c': 2}
		self._p = None
		self._p2 = None
		
		self.pos = Position()
		#self.pos.x = Position()
		self.posList = [Position(), Position()]
		self.posTuple = (Position(), Position())
		#self.posTuple2 = (self.posList, self.posTuple)
		self.posDict = {'pos1': Position(), 'pos2': Position()}
		#self.posDict2 = {'pos1': self.posList, 'pos2': self.posTuple2}
		#self.posList2 = [self.posTuple2, self.posDict]
		#self.posDict3 = {'pos1': self.l, 'pos2': self.l}
				
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
		

		
inst1 = MyClass()

inst1.a = 5
inst1.b = 6
inst1.p =  Position()
inst1.p.x = 4
inst1.pos.x = 3.0
inst1.pos.y = 4.0
inst1.pos.z = Position()


inst1.posList[0].x = 6.0
inst1.posList[0].y = 6.1
inst1.posList[0].z = 6.2


inst1.posTuple[0].x = 7.0
inst1.posTuple[0].y = 7.1
inst1.posTuple[0].z = 7.2

inst1.posDict['pos2'].x = 8.0
inst1.posDict['pos2'].y = 8.1
inst1.posDict['pos2'].z = 8.2


#inst1.printAttrs()

import json
import pprint
inst1Data = inst1.GetAttrs()
pprint.pprint(inst1Data)
inst1Data = json.dumps(inst1Data)



inst2 = MyClass()
print('\nInitialize Inst2')
#pprint.pprint(inst2.GetAttrs())

inst2.SetAttrs(json.loads(inst1Data)) 
#inst2.SetAttrs(inst1Data)
#inst2.SetAttrs(json.loads(inst1Data), setProperty=False)

print('\nSet Inst2')	
print('Inst2 p:', inst2.p)
pprint.pprint(inst2.GetAttrs())
#pprint.pprint(inst2.posList)
#pprint.pprint(inst2.posDict)
'''
pos = Position()

objData = ObjectData()

posData = objData.GetAttrs(obj=pos)
print(posData)'''

'''
l = []

l.append(Position())
l.append(type('Position', (), {})())
print(l)'''
