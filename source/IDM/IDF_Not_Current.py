# need to add readOnly argument and have option of no setter

def createParProperty(inst, name, getterCallback=None, 
						setterCallback=None, postSetterCallback=None):

	if getterCallback or setterCallback or postSetterCallback:		
		createParPropCallbacks(inst, name, getterCallback,
									setterCallback, postSetterCallback)
									
	else:
		createParPropNoCallbacks(inst, name)


def createParPropNoCallbacks(inst, name):

	def getter(inst):
		return getattr(inst.ownerComp.par, name).eval()

	def setter(inst, value):
		setattr(inst.ownerComp.par, name, value)

	setattr(inst.__class__, name, property(getter, setter))

def createParPropCallbacks(inst, name, getterCallback,
							setterCallback, postSetterCallback):

	def getter(inst):
		
		value = getattr(inst.ownerComp.par, name).eval()

		if getterCallback:
			return getterCallback(name, value)

		return value

	def setter(inst, value):
		
		if setterCallback:
			value = setterCallback(name, value)

		setattr(inst.ownerComp.par, name, value)

		if postSetterCallback:
			postSetterCallback(name, value)

	setattr(inst.__class__, name, property(getter, setter))

def createParProperties(inst, parNames=None, filterPars=[],
						customPars=True, builtinPars=False,
						printInfo=False):

	if printInfo:
		print('\nCreateParProperties in:', inst.ownerComp.path)

	if parNames:
		for name in parNames:
		
			if name not in filterPars:
				createParProperty(inst, name)

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
				createParProperty(inst, par.name)

				if printInfo:
					print('\t\tParProperty:\t', par.name)

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