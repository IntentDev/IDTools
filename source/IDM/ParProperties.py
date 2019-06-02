class ParProperty(object):

	def __init__(	self, obj, name, ownerComp, parpgroup, fget=None, 
					fset=None, fpostset=None, fdelete=None, 
					fcallback=None, doc=None):

		self.obj = obj
		self.name = name
		self.ownerComp = ownerComp
		self.par = getattr(self.ownerComp.par, self.name)
		self.parpgroup = parpgroup
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

		value = getattr(self.ownerComp.par, self.name).eval()

		if self.fget is not None and self.parpgroup.execGetCallback:
			self.fget(value)

		return value

	def __set__(self, obj, value):

		if self.fset is not None and self.parpgroup.execSetCallback:
			value = self.fset(value)
		
		setattr(self.ownerComp.par, self.name, value)
	
		if self.fpostset is not None and self.parpgroup.execPostSetCallback:
			self.fpostset(value)

	def __delete__(self, obj):

		print('\nParProperty:\t\t\t\t', self.name, 'has been deleted')
		if self.fdelete is not None:
			self.fdelete(obj)

	def callback(self, par):

		if self.fcallback is not None:
			self.fcallback(par)

def parProperty(obj, name, ownerComp=None, parpGroup=None, 
				fGet=None, fSet=None, fPostSet=None,
				deleter=None, fCallback=None, doc=None):

	ownerComp = getOwnerComp(obj, ownerComp)

	if not parpGroup:
		parpGroup = 'ParpGrp'

	if not hasattr(obj, parpGroup):
		setattr(obj, parpGroup, ParpGroup(obj, ownerComp, parpGroup))

	parpGroup = getattr(obj, parpGroup)

	parp = ParProperty(	obj, name, ownerComp, parpGroup,
						fget=fGet, fset=fSet, fpostset=fPostSet,
						fdelete=deleter, fcallback=fCallback,
						doc=doc)

	setattr(obj.__class__, name, parp)
	parp = getattr(obj.__class__, name)
	parpGroup.appendParp(name, parp, fcallback=fCallback)

	return parp


def createParProperties(obj, parNames=None, parpGroup=None, 
						ownerComp=None, filterPars=[], customPars=True, 
						builtinPars=False):

	ownerComp = getOwnerComp(obj, ownerComp)

	if not parpGroup:
		parpGroup = 'ParpGrp'

	if not hasattr(obj, parpGroup):
		setattr(obj, parpGroup, ParpGroup(obj, ownerComp, parpGroup))
		
	if parNames:
		for name in parNames:
		
			if name not in filterPars:
				parProp = parProperty(
							obj, name, ownerComp, parpGroup)

	else:

		pars = []
		if customPars and builtinPars: pars = ownerComp.pars()
		elif customPars: pars = ownerComp.customPars
		elif builtinPars: 
			for par in ownerComp.pars():
				if not par.isCustom:
					pars.append(par)

		for par in pars:
			
			if par.tupletName not in filterPars:
				parp = parProperty(
							obj, par.name, ownerComp, parpGroup)

	parg = getattr(obj, parpGroup)					

	return parg

class ParpGroup(object):

	def __init__(self, obj, ownerComp, name,parNames=[]):

		self.obj = obj
		self.ownerComp = ownerComp
		self.name = name
		self.parNames = parNames
		self.execCallbacks = True
		self._execGetCallback = True
		self._execSetCallback = True
		self._execPostSetCallback = True
		self._execParCallback = True

	def appendParp(self, name, parp, fcallback=None):

		setattr(self, name, parp)

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

def getOwnerComp(obj, ownerComp):

	if not ownerComp:
		if hasattr(obj, 'ownerComp'):
			ownerComp = obj.ownerComp
		else:
			raise AttributeError (	
					'Extension does not have "ownerComp" ' +
					'attribute, specify extension ownerComp ' +
					'attribute via ownerComp argument')

	return ownerComp


