ObjectData = op('IDC').module.ObjectData

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
		

	@property
	def Floatpar(self):
		return self.ownerComp.par.Floatpar.eval()

	@Floatpar.setter
	def Floatpar(self, value):
	
		print('Floatpar Set:', value)
		self.ownerComp.par.Floatpar = value
