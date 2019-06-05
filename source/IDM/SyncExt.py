import ParProperties as Parps

class SyncExt:

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.syncOut = ownerComp.op('syncout')
		self.syncIn = ownerComp.op('syncin')
		self.switchSync = ownerComp.op('switchSync')
		self.syncSources = ownerComp.op('syncSources')

		Parps.parProperties(self, parCallbacksDAT=self.ownerComp.op('ParCallbacks'))

	def Mode(self, mode):

		if mode == 'LOCAL':
			self.SyncOutActive(False)
			self.SyncInActive(False)

		elif mode == 'REMOTE':			
			self.SyncOutActive(False)
			self.SyncInActive(False)

		elif mode == 'PRO':		
			self.SyncOutActive(True)
			self.SyncInActive(True)


	def SyncOutActive(self, state):

		self.syncOut.par.active = state
		self.syncOut.bypass = not state

	def SyncInActive(self, state):

		self.syncIn.par.active = state
		self.syncIn.bypass = not state
		self.switchSync.par.index = int(state)
