IDC = op.Modules.op('IDC').module
IDF = op.Modules.op('IDF').module
Clip = IDC.Clip

class ClipExt(Clip):
	# This extension inherits from Clip.
	# Lock or change op type to textDAT to customize...

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		Clip.__init__(self, ownerComp)


		# append more callbacks to self.ParCallbacks
		customCallbacks = IDF.getParCallbacksLookup(self, parNames=[])
		self.ParCallbacks.update(customCallbacks)


