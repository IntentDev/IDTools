import ObjectData as OD
ObjectData = OD.ObjectData

IDF = op.IDM.op('IDF').module

class Clip(ObjectData):
	def __init__(self, ownerComp):
		ObjectData.__init__(self)
		self.ownerComp = ownerComp

		self.__FILTER_GET_ATTR__ = ['clipCallbacks']


		# create par propertities for all customPars
		IDF.createParProperties(self, printInfo=True)
		IDF.createParProperty(self, 'Play',
									setterCallback=self.Play_set)

		self.ParCallbacks = IDF.getParCallbacksLookup(self,
							parNames=['Play', 'Start'])

		if self.Callbacksdat:
			self.clipCallbacks = self.Callbacksdat.module



	def Start_parCallback(self, par):

		getattr(self.clipCallbacks, 'onStart')(self)


	def Play_parCallback(self, par):

		self.Play_postSet(par.name, par)

	def Play_set(self, parName, value):

		print('\nPlay_set:\n\tPlay is being set to:', value)

		return value

	def Play_postSet(self, parName, value):

		print('\nPlay_postSet:')
		if type(value) == type(self.ownerComp.par.Play):
			print('\tPlay_postSet called from Play_parCallback')

		print('\tPlay has been set to:', value)

