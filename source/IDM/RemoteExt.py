import pickle
IDF = op('IDF').module


class RemoteExt:

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.tcpip = ownerComp.op('tcpip')
		self.sync = ownerComp.op('sync')

		IDF.createParProperties(self, printInfo=True)

		self.remoteFuncs = [self.setAttr, self.setPar, self.getAttr]

	def SetMode(self, mode):

		# modes = 	'LOCAL', 'LOCAL_CONTROL_EXTERNAL', 
		# 			'CONTROL_EXTERNAL', 'EXTERNAL', 'BACKUP_UI'

		self.tcpip.par.active = not mode == 'LOCAL'

		if mode == 'LOCAL':
			self.ConnectionMode = 'server'
			self.sync.SyncOutActive(False)
			self.sync.SyncInActive(False)

		elif mode == 'LOCAL_CONTROL_EXTERNAL':
			self.ConnectionMode = 'server'
			self.sync.SyncOutActive(self.ownerComp.Ismaster)
			self.sync.SyncInActive(True)

		elif mode == 'CONTROL_EXTERNAL':
			self.ConnectionMode = 'server'	
			self.sync.SyncOutActive(self.ownerComp.Ismaster)
			self.sync.SyncInActive(False)

		elif mode == 'EXTERNAL':
			self.ConnectionMode = 'client'
			self.sync.SyncOutActive(self.ownerComp.Ismaster)
			self.sync.SyncInActive(True)

		elif mode == 'BACKUP_UI':
			self.ConnectionMode = 'client'
			self.sync.SyncOutActive(False)
			self.sync.SyncInActive(False)

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
			callID = absTime.frame
			bytes_ = pickle.dumps(data.append(callID))
			self.sync.Remotecallid = callID

		else:
			bytes_ = pickle.dumps(datacallID)
	
		self.tcpip.sendBytes(bytes_)	

	# Receive
	##########################################
	def ReceiveBytes(self, bytes_):
		data = pickle.loads(bytes_)
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


	@property
	def ConnectionMode(self):
		return self.tcpip.par.mode.eval()

	@ConnectionMode.setter
	def ConnectionMode(self, value):
		self.tcpip.par.mode = value	
