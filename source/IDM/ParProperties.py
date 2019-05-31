class ParProperty(object):

	def __init__(	self, parName, parGroup=None, fget=None, 
					fset=None, fpostSet=None, doc=None):

		self.parName = parName
		self.fget = fget
		self.fset = fset
		self.fpostSet = fpostSet
		self.fdel = None
		self.parGroup = parGroup
		if doc is None and fget is not None:
			doc = fget.__doc__
		self.__doc__ = doc

	def __get__(self, obj, objType=None):

		if obj is None:
			return self

		value = getattr(obj.ownerComp.par, self.parName).eval()

		if self.fget is not None:
			self.fget(self.parName, value)

		return value

	def __set__(self, obj, value):

		if self.fset is not None:
			value = self.fset(self.parName, value)
		
		setattr(obj.ownerComp.par, self.parName, value)
	
		if self.fpostSet is not None:
			self.fpostSet(self.parName, value)

	def __delete__(self, obj):
		raise AttributeError(	'Unable to delete ParProperty:',
								self.parName)

def parProperty(inst, parName, parGroup=None, 
				getter=None, setter=None, postSetter=None):

	setattr(inst.__class__, parName, 
			ParProperty(parName, parGroup=parGroup,
						fget=getter, fset=setter, fpostSet=postSetter))

	if parGroup:
		if not hasattr(inst, parGroup):
			setattr(inst, parGroup, ParGroup([parName]))

		else:
			parGroup = getattr(inst, parGroup)
			if parName not in parGroup.parNames:
				parGroup.parNames.append(parName)	

def createParProperties(inst, parNames=None, parGroup=None, 
						filterPars=[], customPars=True, 
						builtinPars=False, printInfo=False):

	if printInfo:
		print('\nCreateParProperties in:', inst.ownerComp.path)

	if parNames:
		for name in parNames:
		
			if name not in filterPars:
				parProperty(inst, name, parGroup=parGroup)

				if printInfo:
					print('\t\tParProperty:\t', name)

	else:

		pars = []
		if customPars and builtinPars: pars = inst.ownerComp.pars()
		elif customPars: pars = inst.ownerComp.customPars
		elif builtinPars: 
			for par in inst.ownerComp.pars():
				if not par.isCustom:
					pars.append(par)
				

		for par in pars:
			
			if par.tupletName not in filterPars:
				parProperty(inst, name, parGroup=parGroup)

				if printInfo:
					print('\t\tParProperty:\t', par.name)


class ParGroup(object):

	def __init__(self, parNames=[]):

		self.parNames = parNames
		self.parExecSet = True

	



def getParCallbacksLookup(inst, parNames=[]):

	parCallbacks = {}

	for parName in parNames:
		callbackName = parName + '_parCallback'	

		if hasattr(inst, callbackName):
			parCallbacks[parName] = getattr(inst, callbackName)

	return parCallbacks


class IDPars(object):

	def __init__(self, ownerComp, parNames):

		self.ownerComp = ownerComp
		self.parNames = parNames
		createParProperties(self, parNames=parNames, printInfo=True)

		self.ParCallbacks = getParCallbacksLookup(
			self, parNames=parNames)