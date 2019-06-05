import pickle
Parps = op.IDM.op('ParProperties').module

class RemoteExt:

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.tcpip = ownerComp.op('tcpip')
		self.sync = ownerComp.op('sync')

		Parps.parProperties(self, parCallbacksDAT=self.ownerComp.op('ParCallbacks'))

		self.remoteFuncs = [self.setAttr, self.setPar, self.getAttr]
		self.connectionModes = ['client', 'server']

		self._callID = -1
		self._callList = []

	# Call to Call function, set attribute or set parameter on remote component
	##########################################
	def SetAttr(self, comp, attribute, value):
		self.sendData([0, comp.path, attribute, value])

	def SetPar(self, comp, attribute, value):
		self.sendData([1, comp.path, attribute, value])

	def GetAttr(self, comp, attribute, *args, **kwargs):
		self.sendData([2, comp.path, attribute, args, kwargs])

	# Send
	##########################################
	def sendData(self, data):

		if self.Remotecallsync:
			bytes_ = pickle.dumps(data.append(callID))
			self.sync.Remotecallid = self.callID

		else:
			bytes_ = pickle.dumps(datacallID)
	
		self.tcpip.sendBytes(bytes_)	

	# Receive
	##########################################
	def ReceiveBytes(self, bytes_):
		data = pickle.loads(bytes_)
		self.callFunc(self.remoteFuncs[data[0]], data[1:])
		#self.remoteFuncs[data[0]](data[1:])

	def callFunc(self, func, data):
		
		if self.Syncmode != 'PRO':
			func(data[:-1])

		else:
			data = data[:-1] 
			callID = data[-1]
			self.callList.append([callID, func, data])



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

	@property
	def callID(self):
		prevId = self._callID
		self._callID += 1
		return self._callID

	@property
	def callList(self):
		return self._callList
	
	@callList.setter
	def callList(self, value):
		self._callList = value

	@property
	def ConnectionMode(self):
		return self.tcpip.par.mode.eval()

	@ConnectionMode.setter
	def ConnectionMode(self, value):
		self.tcpip.par.mode = value	
