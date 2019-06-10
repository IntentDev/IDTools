ObjectData = op('IDC').module.ObjectData

class Position:

	def __init__(self):
	
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		


class ExtDataTestExt(ObjectData):
	"""
	ExtDataTestExt description
	"""
	def __init__(self, ownerComp):

		ObjectData.__init__(self)

		self.ownerComp = ownerComp
		
		
		# filter attributes so they aren't added to attrDict 
		#self.__FILTER_GET_ATTR__ = ('C', 'D', 'Floatpar')
		self.__FILTER_GET_ATTR__ = ('C', 'D')

		# filter attributes so they aren't set to object when 
		# retrieved from attrDict 
		self.__FILTER_SET_ATTR__ = ('B')
		
		self.A = 0
		self.B = 0
		self.C = 1
		self.D = 2
		
		self.Pos = Position()
		self.Pos.x = 1
		self.Pos.y = 2
		self.Pos.z = 3

		self.TestFunctionAttr = self.testFunc
		self.TestFunctionDict = {'test_func': self.testFunc}
		self.TestFunctionList = [self.testFunc]
		
	def testFunc(self):

		print('This is a test function')

	@property
	def Floatpar(self):
		return self.ownerComp.par.Floatpar.eval()

	@Floatpar.setter
	def Floatpar(self, value):
	
		print('Floatpar Set:', value)
		self.ownerComp.par.Floatpar = value
