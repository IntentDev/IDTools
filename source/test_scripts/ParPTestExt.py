import ParProperties as ParProps

ParP = ParProps.ParProperty
IDF = op('IDF').module

class ParPTestExt():
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.X = tdu.Dependency(0)
		# create par propertities for all customPars
		#IDF.createParProperties(self)

		ParProps.parProperty(self, 'Float')
		#self.__class__.Float.fset = self.Float_set
		#ParProps.parPropGetter(self, 'Float', self.Float_getter)
		#ParProps.parPropSetter(self, 'Float', self.Float_setter)
		ParProps.parPropPostSetter(self, 'Float', self.Float_postSetter)
		
		# ParProps.parProperty(	self, 'Float', parGroup='TEST1',
		# 						getter=self.Float_getter,
		# 						setter=self.Float_setter,
		# 						postSetter=self.Float_postSetter)

		ParProps.parProperty(self, 'String', parGroup='TEST2')
		ParProps.parPropDeleter(self, 'String', self.String_deleter)
		delattr(self, 'String')

		#self.TEST1.parExecSet = False


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
		
		# IDF.createParProperty(self, 'Floatpar', 
		#  							getterCallback=self.Floatpar_get,
		# 							setterCallback=self.Floatpar_set,
		# 							postSetterCallback=self.Floatpar_postSet)

	############################################################################
	# custom ParProperty callbacks
	# all callbacks need a 'value' argument
	
	def Float_getter(self, value):
		# value is evaluated from par then passed callback
		# then returned value from this callback is return by getter
		print('Float Get callback:\t\t\tFloat par has the value:', value)
		return value

	def Float_setter(self, value):
		# input value is passed to this function, then the returned value
		# of this callback sets the par.
		print('Float Set callback:\t\t\tFloat par is being set to:', value)
		return value

	def Float_postSetter(self, value):
		# this function get it's value post setterCallback and post set par
		# since the par has already been set there is no need to return anything
		#print('Float PostSet callback:\t\tFloat par has been set to:', value)
		self.X.val = value

	def String_deleter(self, value):
		# use deleter callback if some function needs to be called on
		# attribute delete
		print('String Delete callback:\t\tString ParProperty has been deleted')

