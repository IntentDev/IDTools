ObjectData = op.IDM.op('ObjectData').module.ObjectData
Parps = op.IDM.op('ParProperties').module

class Clip(ObjectData):
	def __init__(self, ownerComp):
		ObjectData.__init__(self)
		self.ownerComp = ownerComp

		self.__FILTER_GET_ATTR__ = ['clipCallbacks']

		Parps.parProperties(self)

		self.ParpGrp.Play.fParCallback = self.PlayFunc
		self.ParpGrp.Cue.fParCallback = self.CueFunc
		self.ParpGrp.Cuepulse.fParCallback = self.CuepulseFunc

		if self.Callbacksdat:
			self.clipCallbacks = self.Callbacksdat.module

	def StartParCallback(self, par):

		getattr(self.clipCallbacks, 'onStart')(self)

	def PlayFunc(self, par, caller, prev):
		print(	par.name + 'Func:'.ljust(12), 
				'\t{} has been set to:'.format(par.name), 
				par, 'and called from', caller)

	def CueFunc(self, *args):
		par = args[0]
		caller = args[1]
		print(	par.name + 'Func:'.ljust(12), 
				'\t{} has been set to:'.format(par.name), 
				par, 'and called from', caller)
	

	def CuepulseFunc(self, par, caller):
		print(	par.name + 'Func:'.ljust(8), 
				'\t{} has been set to:'.format(par.name), 
				par, 'and called from', caller)

	def PlayGet(self, value):

		print('PlayGet:'.ljust(12), 'Play is:', value)
		return value

	def PlaySet(self, value):

		print('PlaySet:'.ljust(12), 'Play is being set to:', value)
		return value

	def PlayPostSet(self, value):

		print('PlayPostSet:'.ljust(12), 'Play has been set to:', value)
		return value

