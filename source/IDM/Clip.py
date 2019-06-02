import ObjectData as OD
ObjectData = OD.ObjectData

import ParProperties as Parps

class Clip(ObjectData):
	def __init__(self, ownerComp):
		ObjectData.__init__(self)
		self.ownerComp = ownerComp

		self.__FILTER_GET_ATTR__ = ['clipCallbacks']

		Parps.parProperties(self)

		# Parps.parProperty(	self, 'Play',
		# 					fSet=self.PlaySet,
		# 					fPostSet=self.PlayFunc,
		# 					fParCallback=self.PlayParCallback)

		Parps.parProperty(	self, 'Play',
							fPostSet=self.PlayFunc,
							fParCallback=self.PlayParCallback)
		
		# self.ParpGrp.toggleExecParCallback = False

		if self.Callbacksdat:
			self.clipCallbacks = self.Callbacksdat.module

	def StartParCallback(self, par):

		getattr(self.clipCallbacks, 'onStart')(self)


	def PlayParCallback(self, par, prev):

		# print('\nPlayParCallback:'.ljust(20), 'Play has been set to:', par)

		#self.PlayFunc(par)
		pass

	def PlaySet(self, value):

		print('\nPlaySet:'.ljust(20), 'Play is being set to:', value)
		#self.ParpGrp.execParCallback = False

		return value

	def PlayFunc(self, value):

		if type(value) == type(self.ownerComp.par.Play):
			print('\nPlayFunc has been called by fParCallback()')
		else:
			print('\nPlayFunc has been called by parp.__set__() via parp.fPostSet attribute')

		#run("args[0].ParpGrp.execParCallback = True", self.ownerComp,
		#	delayFrames=1)


