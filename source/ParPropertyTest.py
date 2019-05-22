
ParProperty = op('ParProperty').module.ParProperty

class ParPropertyTest(ParProperty):
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		ParProperty.__init__(self, ownerComp)

	def parPropertiesCreate(self):

		for par in self.ownerComp.customPars:

			self.parPropertyCreate(par)

		pass

	def parSetter(self, par, value):

		par = value


	def parPropertyCreate(self, par):

		#setattr(self.__class__, par.name, property(lambda self: self.)

		pass