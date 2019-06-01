
IDF = op('IDF').module

class TestIDParsExt():
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
	
		#IDF.createParProperties(self)

		parNames = ['Color', 'Menu', 'Floatpar', 'Top', 'Stringpar']
		self.Pars = IDF.IDPars(ownerComp, parNames)


