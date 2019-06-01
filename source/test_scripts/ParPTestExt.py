import ParProperties as ParProps

IDF = op('IDF').module

class ParPTestExt():
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		#self.__FILTER_GET_ATTR__ = ['ParPTestExt']

		self.X = tdu.Dependency(0)

		# create par propertities for all customPars (return parGroup)
		parg = ParProps.createParProperties(self)
		for parpName in parg.parNames:
			print(parpName)

		# create par property for 'Float' par only and specify functions
		# self.FloatParp = ParProps.parProperty(self, 'Float', parGroup='PARS',
		# 										fGet=self.FloatGetter,
		# 										fSet=self.FloatSetter,
		# 										fPostSet=self.FloatPostSetter,
		# 										fCallback=self.FloatParCallback)

		# create par property for 'Float' par only
		#self.FloatParp = ParProps.parProperty(self, 'Float')

		# set functions for self.FloatParp after it has been created
		# self.FloatParp.fget = self.FloatGetter
		# self.FloatParp.fset = self.FloatSetter
		# self.FloatParp.fpostset = self.FloatPostSetter
		# self.FloatParp.fcallback = self.FloatParCallback
				
		# set functions for self.FloatParp after it has been created via parGroup
		# default name for parGroup (if not explicity set) is 'PARS'
		self.PARS.Float.fget = self.FloatGetter
		self.PARS.Float.fset = self.FloatSetter
		self.PARS.Float.fpostset = self.FloatPostSetter
		self.PARS.Float.fcallback = self.FloatParCallback

		print('self.PARS.Float.par type =', type(self.PARS.Float.par), 'value =', self.PARS.Float.par)

		# create par properties for custom and builtin pars
		# parps = ParProps.createParProperties(self, builtinPars=True)
		# for parp in parps:
		# 	print(parp.name)

		# create par propertities for just builtin pars
		# parps = ParProps.createParProperties(self, customPars=False, builtinPars=True)
		# for parp in parps:
		# 	print(parp.name)

		# filter pars (specify pars to not create properties for)
		# parps = ParProps.createParProperties(self, filterPars=['Float', 'Color'])
		# for parp in parps:
		# 	print(parp.name)

		# delete Parp
		# self.StringParp.fdelete = self.String_deleter
		# delattr(self, 'String')


	############################################################################
	# custom ParProperty callbacks
	# all callbacks need a 'value' argument
	
	def FloatGetter(self, value):
		# value is evaluated from par then passed callback
		# then returned value from this callback is return by getter
		print('Float getter:\t\t\tFloat par has the value:', value)
		return value

	def FloatSetter(self, value):
		# input value is passed to this function, then the returned value
		# of this callback sets the par.
		print('Float setter:\t\t\tFloat par is being set to:', value)
		return value

	def FloatPostSetter(self, value):
		# this function get it's value post setterCallback and post set par
		# since the par has already been set there is no need to return anything
		print('Float postsetter:\t\tFloat par has been set to:', value)
		self.X.val = value

	def FloatParCallback(self, *args):
		val = args[0].eval()	
		print('Float callback:\t\t\tFloat par has been set to:', val)
		self.ownerComp.op('constant1').par.value0 = val
		self.ownerComp.op('../constant1').par.value1 = val

	def String_deleter(self, value):
		# use deleter callback if some function needs to be called on
		# attribute delete
		print('String deleter:\t\t\tString ParProperty has been deleted')

