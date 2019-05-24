ObjectData = op('ObjectData').module.ObjectData

class ExtDataTestExt(ObjectData):
	"""
	ExtDataTestExt description
	"""
	def __init__(self, ownerComp):

		ObjectData.__init__(self)

		self.ownerComp = ownerComp

		self.A = 0
		self.B = 0

	@property
	def Floatpar(self):
		return self.ownerComp.par.Floatpar.eval()

	@Floatpar.setter
	def Floatpar(self, value):
		self.ownerComp.par.Floatpar = value
