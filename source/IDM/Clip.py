import ObjectData as OD
ObjectData = OD.ObjectData

import ParProperties as Parps

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

	def PlayFunc(self, par, *args):
		
		append = ''

		if len(args) > 1:
			append = 'and called from parp.__set__()'
		else:
			append = 'and called from parexec_ParCallbacks'
		print(par.name + 'Func:'.ljust(12), '\tPlay has been set to:', par, append)

	def CueFunc(self, par, *args):
		
		append = ''

		if len(args) > 1:
			append = 'and called from parp.__set__()'
		else:
			append = 'and called from parexec_ParCallbacks'
		print(par.name + 'Func:'.ljust(12), '\tCue has been set to:', par, append)	

	def CuepulseFunc(self, par, *args):
		print(par.name + 'Func:\t'.ljust(9), par.isPulse)

	def PlayGet(self, value):

		print('PlayGet:'.ljust(12), 'Play is:', value)
		return value

	def PlaySet(self, value):

		print('PlaySet:'.ljust(12), 'Play is being set to:', value)
		return value

	def PlayPostSet(self, value):

		print('PlayPostSet:'.ljust(12), 'Play has been set to:', value)
		return value

