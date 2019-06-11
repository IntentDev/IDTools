
class Position:

	def __init__(self):
	
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		

class ExtDataTestExt():
	"""
	ExtDataTestExt description
	"""
	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		
		self.A = 0
		self.B = 0
		self.C = 1
		self.D = 2
	
		self.Pos = Position()
		self.Pos.x = 0.0
		self.Pos.y = 0.0
		self.Pos.z = 0.0	
		
	def testFunc(self):

		print('This is a test function')		

	@property
	def Floatpar(self):
		return self.ownerComp.par.Floatpar.eval()

	@Floatpar.setter
	def Floatpar(self, value):
	
		print('Floatpar Set:', value)
		self.ownerComp.par.Floatpar = value
