import ParProperties as ParProps

class ParpTestExt():
	"""
	ParPropertyTest description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		#self.__FILTER_GET_ATTR__ = ['ParPTestExt']

		self.X = tdu.Dependency(0)

		# create par propertities for all customPars and
		# return parpGroup
		# 
		parg = ParProps.createParProperties(self)
		for parName in parg.parNames:
			print()
			print(parName.ljust(9), '\t\t\t\t\t', getattr(self, parName))

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


		# set functions for self.Float parp after it has been
		# created via the ParpGroup the parp belongs to. 
		# The default name for a ParpGroup if not explicity 
		# set in createParProperty() or createParProperties() 
		# is 'ParpGrp'
		#
		# assign function to be called whenever the parp 
		# returns its value. see self.FloatGetter() below
		#
		self.ParpGrp.Float.fget = self.FloatGetter

		# assign function to be called before the parp
		# set its value. see self.FloatSetter() below	
		#
		self.ParpGrp.Float.fset = self.FloatSetter

		# assign function to be called after the parp sets
		# its value. see self.FloatPostSetter() below
		#
		self.ParpGrp.Float.fpostset = self.FloatPostSetter

		# assign function to be called by parexec onValue() or
		# onPulse(). see self.FloatParCallback() below
		#
		self.ParpGrp.Float.fcallback = self.FloatParCallback

		# peek into the par via the parp
		# 
		print(	'\nself.ParpGrp.Float.par\t\t', 
				type(self.ParpGrp.Float.par), 
				'value =', self.ParpGrp.Float.par.eval())

		# assign function to be called on delete of parp
		# see self.MomentaryDeleter() below
		#
		self.ParpGrp.Momentary.fdelete = self.MomentaryDeleter
		# delete Parp # todo need to delete from parpGroup in parp deleter function
		#
		delattr(self, 'Momentary')
		

		# create par property for 'Float' par only and 
		# specify function attributes during creation
		# 
		# self.FloatParp = ParProps.parProperty(self, 'Float', parpGroup='ParpGrp',
		# 										fGet=self.FloatGetter,
		# 										fSet=self.FloatSetter,
		# 										fPostSet=self.FloatPostSetter,
		# 										fCallback=self.FloatParCallback)

		# create 'Float' parp and add FloatParp attribute to self 
		# Note there is difference between the property (self.Float) 
		# and the property object (self.FloatParp). self.Float is
		# the parProperty instance set on the class of the extension
		# while self.FloatParp is the parProperty instance set on the
		# class instance that then provides an interface into the
		# parProperty set on the class. ie. set and get and the 
		# attributes of the parProperty itself rather than the object
		# the property is referencing.
		#
		# set functions for self.FloatParp after it has been explicitly created
		# note self.FloatParp == self.ParpGrp.Float
		#
		self.FloatParp = ParProps.parProperty(self, 'Float')
		self.FloatParp.fget = self.FloatGetter
		self.FloatParp.fset = self.FloatSetter
		self.FloatParp.fpostset = self.FloatPostSetter
		self.FloatParp.fcallback = self.FloatParCallback
		
		# set and get some parps!
		# 
		x = self.Float
		self.Float = 6	
		self.String = 'Hello!'
		self.Menu = 1

	############################################################################
	# custom ParProperty callbacks
	# all callbacks need a 'value' argument
	
	def FloatGetter(self, value):
		# value is evaluated from par then passed callback
		# then returned value from this callback is return by getter
		print('\nFloatGetter:\t\t\t\t Float par has the value:', value)
		return value

	def FloatSetter(self, value):
		# input value is passed to this function, then the returned value
		# of this callback sets the par.
		print('\nFloatSetter:\t\t\t\t Float par is being set to:', value)
		return value

	def FloatPostSetter(self, value):
		# this function get it's value post setterCallback and post set par
		# since the par has already been set there is no need to return anything
		print('\nFloatPostSetter:\t\t\t Float par has been set to:', value)
		self.X.val = value

	def FloatParCallback(self, *args):
		val = args[0].eval()	
		print('\nFloatParCallback:\t\t\t Float par has been set to:', val)
		self.ownerComp.op('constant1').par.value0 = val
		self.ownerComp.op('../constant1').par.value1 = val

	def MomentaryDeleter(self, value):
		# use deleter callback if some function needs to be called on
		# attribute delete
		print('\nMomentaryDeleter:\t\t\t Momentary parp has been deleted')

