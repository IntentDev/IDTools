IDC = op.IDM.op('IDC').module
Clip = IDC.Clip

class ClipExt(Clip):
	# This extension inherits from Clip.
	# Lock or change op type to textDAT to customize...

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		Clip.__init__(self, ownerComp)



