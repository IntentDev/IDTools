# need to add readOnly argument and have option of no setter

def createParProperty(inst, name, getterCallback=None, 
						setterCallback=None, postSetterCallback=None):
	print('createParProperty:', name)

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

def createParProperties(inst, pars=None, filterPars=[],
						customPars=True, builtinPars=False):

	if pars:
		for name in parNames:
		
			if name not in filterPars:
				createParProperty(inst, name)

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

def getParCallbacksLookup(inst, parNames=[]):

	parCallbacks = {}

	for parName in parNames:
		callbackName = parName + '_parCallback'	

		if hasattr(inst, callbackName):
			parCallbacks[parName] = getattr(inst, callbackName)

	return parCallbacks


