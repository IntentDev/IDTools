ObjectData = op('ObjectData').module.ObjectData

class ExtDataTestExt(ObjectData):
	"""
	ExtDataTestExt description
	"""
	def __init__(self, ownerComp):

		ObjectData.__init__(self)

		self.ownerComp = ownerComp
		# filter attributes so they aren't added to 
		# data dict by adding to optional instance 
		#attribute called'__filter_attr__'
		#self.__filter_attr__ = ('C', 'D', 'Floatpar')
		self.__filter_attr__ = ('C', 'D')

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
