
IDF = op('IDF').module

class ParPropertyTest():
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
		# create par propertities for all customPars
		IDF.createParProperties(self)

		# create par propertities for custom and builtin pars
		# IDF.createParProperties(self, builtinPars=True)

		# create par propertities for just builtin pars
		# IDF.createParProperties(self, customPars=False, builtinPars=True)

		# filter pars (specify pars not to create properties for)
		# IDF.createParProperties(self, filterPars=['Floatpar', 'Color'])

		# create par property for Floatpar only
		#IDF.createParProperty(self, 'Floatpar')

		# create par property for Floatpar parameter and specify get callback function
		# can also override property set in IDF.createParProperties()
		# IDF.createParProperty(self, 'Floatpar', 
		#  							getterCallback=self.Floatpar_get)

		# IDF.createParProperty(self, 'Floatpar',
		# 							setterCallback=self.Floatpar_set)

		# IDF.createParProperty(self, 'Floatpar',
		# 							postSetterCallback=self.Floatpar_postSet)
		
		IDF.createParProperty(self, 'Floatpar', 
		 							getterCallback=self.Floatpar_get,
									setterCallback=self.Floatpar_set,
									postSetterCallback=self.Floatpar_postSet)


		IDF.createParCallbacksLookup(self, ['Floatpar', 'Menu'])						

	# custom par property callbacks
	# all callbacks need a 'parName' and a 'value' argument
	def Floatpar_get(self, parName, value):
		# value is evaluated from par then passed callback
		# then returned value from this callback is return by getter
		print('Custom Get callback:\t\t', parName, 'has the value:', value)

		return value

	def Floatpar_set(self, parName, value):
		# input value is passed to this function, then the returned value
		# of this callback sets the par.
		
		print('Custom Set callback:\t\t', parName, 'is being set to 4 +', value, '(4 + input value)')

		value += 4

		return value

	def Floatpar_postSet(self, parName, value):
		# this function get it's value post setterCallback and post set par
		# since the par has already been set there is no need to return anything
		print('Custom Post Set callback:\t', parName, 'has been set to:', value)

	def Floatpar_parCallback(self, par):

		print(par.name, 'is being set to:', par.eval(), '(printed from parCallback)')

	def Menu_parCallback(self, par):

		print(par.name, 'is being set to:', par.eval(), '(printed from parCallback)')
