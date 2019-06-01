class ParProperty(object):

	def __init__(	self, obj, name, pargroup, fget=None, 
					fset=None, fpostset=None, fdelete=None, 
					fcallback=None, doc=None):

		self.obj = obj
		self.name = name
		self.pargroup = pargroup
		self.fget = fget
		self.fset = fset
		self.fpostset = fpostset
		self.fdelete = fdelete
		self.fcallback = fcallback

		if doc is None and fget is not None:
			doc = fget.__doc__
		self.__doc__ = doc

	def __get__(self, obj, objType=None):

		if obj is None:
			return self

		value = getattr(obj.ownerComp.par, self.name).eval()

		if self.fget is not None and self.pargroup.execGetCallback:
			self.fget(value)

		return value

	def __set__(self, obj, value):

		if self.fset is not None and self.pargroup.execSetCallback:
			value = self.fset(value)
		
		setattr(obj.ownerComp.par, self.name, value)
	
		if self.fpostset is not None and self.pargroup.execPostSetCallback:
			self.fpostset(value)

	def __delete__(self, obj):

		print(	'ParProperty:', self.name, 'has been deleted')
		if self.fdelete is not None:
			self.fdelete(obj)

	def callback(self, par):

		if self.fcallback is not None:
			self.fcallback(par)

def parProperty(obj, name, parGroup=None, ownerComp=None, 
				fGet=None, fSet=None, fPostSet=None,
				deleter=None, fCallback=None):

	if not parGroup:
		parGroup = 'PARS'

	if not hasattr(obj, parGroup):
		setattr(obj, parGroup, ParGroup(obj, ownerComp=ownerComp))

	parGroup = getattr(obj, parGroup)

	parProperty = ParProperty(
		obj, name, pargroup=parGroup,
		fget=fGet, fset=fSet, fpostset=fPostSet,
		fdelete=deleter)

	setattr(obj.__class__, name, parProperty)
	parp = getattr(obj.__class__, name)
	parGroup.appendPar(name, parp, fcallback=fCallback)

	return parp


def createParProperties(
		obj, parNames=None, parGroup=None, filterPars=[], 
		customPars=True, builtinPars=False, printInfo=False,
		setPropertyAttr=True, ownerComp=None):

	if printInfo:
		print('\nCreateParProperties in:', obj.ownerComp.path)

	if not parGroup:
		parGroup = 'PARS'

	if not hasattr(obj, parGroup):
		setattr(obj, parGroup, ParGroup(obj, ownerComp=ownerComp))
		
	if parNames:
		for name in parNames:
		
			if name not in filterPars:
				parProp = parProperty(obj, name, parGroup=parGroup)
				if setPropertyAttr:
					setattr(obj, name + 'Parp', parProp)	

				if printInfo:
					print('\t\tParProperty:\t', name)

	else:

		pars = []
		if customPars and builtinPars: pars = obj.ownerComp.pars()
		elif customPars: pars = obj.ownerComp.customPars
		elif builtinPars: 
			for par in obj.ownerComp.pars():
				if not par.isCustom:
					pars.append(par)

		for par in pars:
			
			if par.tupletName not in filterPars:
				parProp = parProperty(obj, par.name, parGroup=parGroup)
				if setPropertyAttr:
					setattr(obj, par.name + 'Parp', parProp)	

				if printInfo:
					print('\t\tParProperty:\t', par.name)

	parg = getattr(obj, parGroup)					

	return parg


class Par(object):

	def __init__(self, ownerComp, name, parp=None, fcallback=None):
		self.name = name
		self.par = getattr(ownerComp.par, name)
		self.parp = parp
		self._fcallback = fcallback
	
	@property
	def fget(self):
		return self.parp.fget
	
	@fget.setter
	def fget(self, func):
		self.parp.fget = func

	@property
	def fset(self):
		return self.parp.fset
	
	@fset.setter
	def fset(self, func):
		self.parp.fset = func

	@property
	def fpostset(self):
		return self.parp.fpostset
	
	@fpostset.setter
	def fpostset(self, func):
		self.parp.fpostset = func

	@property
	def fdelete(self):
		return self.parp.fdelete
	
	@fdelete.setter
	def fdelete(self, func):
		self.parp.fdelete = func


	################################################
	# callback called in Par object - faster than property?
	@property
	def fcallback(self):
		return self._fcallback
	
	@fcallback.setter
	def fcallback(self, func):
		self._fcallback = func

	def callback(self, par):
		if self._fcallback is not None:
			self.fcallback(par)


	################################################
	# callback called in property - more consistent than internal call?
	# @property
	# def fcallback(self):
	# 	return self.parp.fcallback
	
	# @fcallback.setter
	# def fcallback(self, func):
	# 	self.parp.fcallback = func	

	# @property
	# def callback(self):
	# 	return self.parp.callback


class ParGroup(object):

	def __init__(self, obj, parNames=[], ownerComp=None):

		if not ownerComp:
			if hasattr(obj, 'ownerComp'):
				ownerComp = obj.ownerComp
			else:
				raise AttributeError (	'Extension does not have "ownerComp" ' +
										'attribute, specify extension ownerComp ' +
										'attribute via ownerComp argument')

		self.ownerComp = ownerComp
		self.parNames = parNames
		self.execCallbacks = True
		self._execGetCallback = True
		self._execSetCallback = True
		self._execPostSetCallback = True
		self._execParCallback = True

	def appendPar(self, name, parp=None, fcallback=None):

		par = Par(self.ownerComp, name, parp=parp, fcallback=fcallback)
		setattr(self, par.name, par)

		if name not in self.parNames:
			self.parNames.append(name)


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
		return self._execParCallback and self.execCallbacks

	@execParCallback.setter
	def execParCallback(self, value):
		self._execParCallback = value
