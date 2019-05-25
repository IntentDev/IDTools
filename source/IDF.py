# need to add readOnly argument and have option of no setter

def createParProperty(inst, name, getCallback=None, 
						setCallback=None, postSetCallback=None):
	print('createParProperty:', name)

	if getCallback or setCallback or postSetCallback:		
		createParPropCallbacks(inst, name, getCallback,
									setCallback, postSetCallback)
									
	else:
		createParPropNoCallbacks(inst, name)


def createParPropNoCallbacks(inst, name):

	def getter(inst):
		return getattr(inst.ownerComp.par, name).eval()

	def setter(inst, value):
		setattr(inst.ownerComp.par, name, value)

	setattr(inst.__class__, name, property(getter, setter))

def createParPropCallbacks(inst, name, getCallback,
							setCallback, postSetCallback):

	def getter(inst):
		
		value = getattr(inst.ownerComp.par, name).eval()

		if getCallback:
			return getCallback(name, value)

		return value

	def setter(inst, value):
		
		if setCallback:
			value = setCallback(name, value)

		setattr(inst.ownerComp.par, name, value)

		if postSetCallback:
			postSetCallback(name, value)

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
		
	
