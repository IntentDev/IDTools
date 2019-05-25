def createParProperty(inst, name, getCallback=None, setCallback=None, postSetCallback=None):
	print('createParProperty:', name)

	if not getCallback or setCallback or postSetCallback:	
		createParPropNoCallbacks(inst, name)

	else:
		createParPropCallbacks(inst, name, getCallback,
									setCallback, postSetCallback)



def createParPropNoCallbacks(inst, name):
	print('createParPropNoCallbacks', name)
	def getter(inst):
		print('get property', name)
		return getattr(inst.ownerComp.par, name).eval()

	def setter(inst, value):
		print('set property', name)
		setattr(inst.ownerComp.par, name, value)

	setattr(inst.__class__, name, property(getter, setter))

def createParPropCallbacks(inst, name, getCallback,
							setCallback, postSetCallback):
	print('createParPropCallbacks', name)
	def getter(inst):
		print('get property', name)

		value = getattr(inst.ownerComp.par, name).eval()

		if getCallback:
			return getCallback(value)

		return value

	def setter(inst, value):
		print('set property', name)

		if setCallback:
			setCallback(value)

		setattr(inst.ownerComp.par, name, value)

		if postSetCallback:
			postSetCallback(value)

	setattr(inst.__class__, name, property(getter, setter))

def createParProperties(inst):

	for par in inst.ownerComp.customPars:

		createParProperty(inst, par.name)
		
	
