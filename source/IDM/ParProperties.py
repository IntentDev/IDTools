class ParProperty(object):

	def __init__(	self, obj, parName, parGroup=None, fget=None, 
					fset=None, fpostSet=None, fdelete=None, 
					fparCallback=None, doc=None):

		self.obj = obj
		self.parName = parName
		self.fget = fget
		self.fset = fset
		self.fpostSet = fpostSet
		self.fdelete = fdelete
		self.fparCallback = fparCallback

		if parGroup:
			if hasattr(obj, parGroup):
				self.parGroup = getattr(obj, parGroup)
		else:
			self.parGroup = None

		if doc is None and fget is not None:
			doc = fget.__doc__
		self.__doc__ = doc

	def __get__(self, obj, objType=None):

		if obj is None:
			return self

		value = getattr(obj.ownerComp.par, self.parName).eval()

		execGetCallback = True
		if self.parGroup:
			execGetCallback = self.parGroup.execGetCallback

		if self.fget is not None and execGetCallback:
			self.fget(value)

		return value

	def __set__(self, obj, value):

		execSetCallback = True
		execPostSetCallback = True
		if self.parGroup:
			execSetCallback = self.parGroup.execSetCallback
			execPostSetCallback = self.parGroup.execPostSetCallback
		

		if self.fset is not None and execSetCallback:
			value = self.fset(value)
		
		setattr(obj.ownerComp.par, self.parName, value)
	
		if self.fpostSet is not None and execPostSetCallback:
			self.fpostSet(value)

	def __delete__(self, obj):
		print(	'ParProperty:', self.parName, 'has been deleted')
		if self.fdelete is not None:
			self.fdelete(obj)

def parProperty(obj, parName, parGroup=None, 
				getter=None, setter=None, postSetter=None,
				deleter=None):

	if not parGroup:
		parGroup = 'PARS'

	if not hasattr(obj, parGroup):
		setattr(obj, parGroup, ParGroup([parName]))

	else:
		parGroupAttr = getattr(obj, parGroup)
		if parName not in parGroupAttr.parNames:
			parGroupAttr.parNames.append(parName)	


	setattr(obj.__class__, parName, 
			ParProperty(obj, parName, parGroup=parGroup,
						fget=getter, fset=setter, fpostSet=postSetter,
						fdelete=deleter))

def parPropGetter(obj, attr, func):
	getattr(obj.__class__, attr).fget = func

def parPropSetter(obj, attr, func):
	getattr(obj.__class__, attr).fset = func

def parPropPostSetter(obj, attr, func):
	getattr(obj.__class__, attr).fpostSet = func

def parPropDeleter(obj, attr, func):
	getattr(obj.__class__, attr).fdelete = func

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
		self.execCallbacks = True
		self._execGetCallback = True
		self._execSetCallback = True
		self._execPostSetCallback = True
		self._execParCallback = True

	@property
	def execGetCallback(self):
		return self._execGetCallback and self.execCallbacks

	@execGetCallback.setter
	def execGetCallback(self, value):
		self._execGetCallback = value
	
	@property
	def execSetCallback(self):
		return self._execSetCallback and self.execCallbacks

	@execSetCallback.setter
	def execSetCallback(self, value):
		self._execSetCallback = value

	@property
	def execPostSetCallback(self):
		return self._execPostSetCallback and self.execCallbacks

	@execPostSetCallback.setter
	def execSetCallback(self, value):
		self._execPostSetCallback = value

	@property
	def execParCallback(self):
		return self._execPostSetCallback and self.execCallbacks

	@execParCallback.setter
	def execSetCallback(self, value):
		self._execParCallback = value
