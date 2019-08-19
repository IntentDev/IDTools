import pickle
Parps = op.IDM.op('ParProperties').module

class RemoteExt:

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.tcpip = ownerComp.op('tcpip')
		self.sync = ownerComp.op('sync')

		Parps.parProperties(self, parCallbacksDAT=self.ownerComp.op('ParCallbacks'))
		self.remoteFuncs = [self.setAttr, self.setPar, self.getAttr, self.execFunc]
		self.connectionModes = ['client', 'server']

	# Call to Call function, set attribute or set parameter on remote component
	##########################################
	def SetAttr(self, comp, attribute, value):
		args = pickle.dumps([0, comp.path, attribute, value])
		self.tcpip.sendBytes(args)

	def SetPar(self, comp, attribute, value):
		args = pickle.dumps([1, comp.path, attribute, value])
		self.tcpip.sendBytes(args)

	def GetAttr(self, comp, attribute, *args, **kwargs):	
		data = pickle.dumps([2, comp.path, attribute, args, kwargs])
		self.tcpip.sendBytes(data)

	def ExecFunc(self, func, *args, **kwargs):	
		data = pickle.dumps([3, func, args, kwargs])
		self.tcpip.sendBytes(data)

	# Receive
	##########################################
	def ReceiveBytes(self, bytes):
		if not self.Isserver:
			data = pickle.loads(bytes)
			self.remoteFuncs[data[0]](data[1:])

	def setAttr(self, data):
		comp = op(data[0])
		attribute = data[1]
		value = data[2]
		setattr(comp, attribute, value)

	def setPar(self, data):
		comp = op(data[0])
		attribute = data[1]
		value = data[2]
		setattr(comp.par, attribute, value)

	def getAttr(self, data):
		comp = op(data[0])
		attribute = data[1]
		args = data[2]
		kwargs = data[3]
		getattr(comp, attribute)(*args, **kwargs)

	def execFunc(self, data):
		func = data[0]
		args = data[1]
		kwargs = data[2]
		print(func)
		exec(func)

	@property
	def ConnectionMode(self):
		return self.tcpip.par.mode.eval()

	@ConnectionMode.setter
	def ConnectionMode(self, value):
		self.tcpip.par.mode = value	
