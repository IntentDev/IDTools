
ParProperty = op('parProperty').module

class ParPropertyTest():
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		

		#ParProperty.createParProperties(self)
		ParProperty.createParProperty(self, 'Floatpar', 
		 							getCallback=self.Floatpar_get,
									setCallback=self.Floatpar_set,
									postSetCallback=self.Floatpar_postSet)

	def Floatpar_get(self, value):

		print('Get callback!')

		return value

	def Floatpar_set(self, value):

		print('Set callback!')

		return value

	def Floatpar_postSet(self, value):

		print('postSet callback!')

		return value

	@property
	def Floatpar(self):
		print('get Floatpar')
		return self.ownerComp.par.Floatpar.eval()

	@Floatpar.setter
	def Floatpar(self, value):
		print('set Floatpar')
		self.ownerComp.par.Floatpar = value
