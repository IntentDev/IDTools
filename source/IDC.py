class ObjectData:
	'''
	Inherit ObjectData in an extension or class
	
	Use GetAttrs() to return a JSON or TD storage serializable dict of all 
	the attributes of the extension/class inheriting ObjectData. 
	All attributes are converted to dicts with '_attr_val', '_attr_type' 
	and '_attr_set' keys. Non-serializable attributes ie. instances
	of non-base types (float, int, str, list etc...), lists, dicts or 
	tuples of non-base types and any combination of the above are all 
	converted. For example:

		- float -> attrDict
		- custom object -> attrDict
		- list (of floats, ints, strings, custom objects etc..) -> list of attrDicts
		- dict (of floats, ints, strings, custom objects etc..) -> dict of attrDicts
		- list of lists or dicts -> list of lists or dicts of attrDicts -> attrDicts
			of all sub objects (infinitely deep)
		- attribute of custom objects that is also a custom object -> attrDict -> attrDict
			also infinitely deep (at least to memory constraints)
		- properties -> propery attrDict containing property data attrDict
		- td.op -> OP attrDict which contains a string of the op path
		- td.op.par -> Par attrDict which contains various par attributes in 
			which only owner.path and par.name are being used in SetAttrs()
		- all other td and tdu types are filterd and not added to attrsDict 
			at this time. (still need to fliter a few other td built in base 
			classes such as Project and UI Class)
			- For types such as tdu.Matrix or tdu.Vector use the .vals 
				member in a property to get and set the actual data.

	Use GetAttrs() to return a JSON or TD storage serializable dict then
	dump to JSON or store in an op. Then use SetAttrs(yourAttrsDataDict) to set all
	the attributes of either the same instance or another instance of the same
	class/extension. 
	
	With keeping in mind that properties are slightly different than attributes
	you can even create empty an instance of a nearly empty class and fill it
	with attributes that did not previously exist in that instance. 

	Should be able to work without inheritance but that has not been tested,
	for now it is meant to be used as an inherited base class.

	Use self.__FILTER_GET_ATTR__ = (tuple of names(str) of attributes) that you 
	do not want to be added to the attrsDict

	Use self.__FILTER_SET_ATTR__ = (tuple of names(str) of attributes) that you 
	do not want to be set in the object that could exist in the attrDict	
	'''
	def __init__(self):

		self.__FILTER_GET__ = (	'__FILTER_GET__', '__FILTER_SET__',
								'__FILTER_GET_ATTR__', '__FILTER_SET_ATTR__', 
								'ownerComp')

		self.__FILTER_SET__ = ()

		pass

	def GetAttrs(self, obj=None):
		
		if not obj:
			obj = self

		# get instance attributes
		attrDict = {}
		for attrName, attrVal in obj.__dict__.items():			
			type_ = type(attrVal)
			typeName = type_.__name__	
			attrSet = True

			createKey = (	attrName[:13] != '_ObjectData__' and	
							attrName[:2] != '__' and
							attrName != '__FILTER_GET__' and
							attrName not in self.__FILTER_GET__
						)	


			if hasattr(obj, '__FILTER_GET_ATTR__'):
				
				createKey = (createKey and
							attrName not in obj.__FILTER_GET_ATTR__)

			if attrVal.__class__.__module__ not in ('td', 'tdu'):
				if not self.isSerializable(attrVal):
					attrVal = self.makeSerializable(attrVal, returnDict=False)
				
			elif hasattr(attrVal, 'OPType'):
				attrVal = attrVal.path
				typeName = 'OP'
				#attrSet = attrName not in ('ownerComp')

			elif attrVal.__class__ == Par:
				attrVal = self.makePar(attrVal)

			else: createKey = False

			if createKey:		
				attrDict[attrName] = {'_attr_val': attrVal, 
									'_attr_type': typeName, 
									'_attr_set': attrSet}



		# get class attributes that are not callable
		if hasattr(obj.__class__, '__dict__'):
			for attrName in obj.__class__.__dict__.keys():
				if attrName[:2] != '__':

					# check for static or class method
					attrVal = getattr(obj.__class__, attrName)
					if not callable(attrVal):

						createKey = attrName[:2] != '__'

						if attrVal.__class__.__module__ not in ('td', 'tdu'):

							type_ = type(attrVal)
							typeName = type_.__name__
							attrSet = False
							

							if type_ != property:
								if not self.isSerializable(attrVal):
									attrVal = self.makeSerializable(attrVal, returnDict=False)
								else:
									attrVal = getattr(obj, attrName)

							else:
								# get property
								attrSet = attrVal.fset != None

								if not self.isSerializable(attrVal.__get__(obj)):
									attrVal = self.makeSerializable(getattr(obj, attrName), 
																	inputAttrSet=attrSet)
								else:
									attrVal = getattr(obj, attrName)

						elif hasattr(attrVal, 'OPType'):
							attrVal = attrVal.path
							typeName = 'OP'

						elif attrVal.__class__ == Par:
							attrVal = self.makePar(attrVal)

						else: createKey = False

						createKey = (	createKey and	
										attrName[:2] != '__' and
										attrName != '__FILTER_GET__' and
										attrName not in self.__FILTER_GET__
									)			

						if hasattr(obj, '__FILTER_GET_ATTR__'):		
							createKey = (createKey and
										attrName not in obj.__FILTER_GET_ATTR__)	

						if createKey:

							attrDict[attrName] = {'_attr_val': attrVal, 
											'_attr_type': typeName, 
											'_attr_set': attrSet}

		return attrDict

	def isSerializable(self, data):

		if data is None:
			return True

		elif isinstance(data, (bool, int, float, str, type(None))):
			return True

		elif isinstance(data, (tuple, list)):
			return all(self.isSerializable(x) for x in data)

		elif isinstance(data, dict):
			return all(isinstance(key, str) and self.isSerializable(val) 
											for key,val in data.items())

		return False

	def makeSerializable(self, inputVal, inputTypeName=None, 
							inputAttrSet=True, returnDict=True):

		if isinstance(inputVal, (list, tuple)):
			l = []
			for val in inputVal:
				type_ = type(val)
				typeName = type_.__name__
				
				if isinstance(val, (list, tuple)):
					val = self.makeSerialList(val)
				
				elif isinstance(val, dict):
					val = self.makeSerialDict(val)				
				
				else:
					val = self.GetAttrs(obj=val)
				
				v = {'_attr_val': val, 
					'_attr_type': typeName, 
					'_attr_set': True}

				l.append(v)

			if isinstance(inputVal, tuple):
				l = tuple(l)

			attrVal = l
			
		elif isinstance(inputVal, dict):
			d = {}
			for key, val in inputVal.items():
				type_ = type(val)
				typeName = type_.__name__

				if isinstance(val, (list, tuple)):
					val = self.makeSerialList(val)

				elif isinstance(val, dict):
					val = self.makeSerialDict(val)	

				else:
					val = self.GetAttrs(obj=val)
				
				v = {'_attr_val': val, 
					'_attr_type': typeName, 
					'_attr_set': True}

				d[key] = v

			attrVal = d

		else:
			attrVal = self.GetAttrs(obj=inputVal)
		
		if returnDict:
			if not inputTypeName:
				type_ = type(inputVal)
				typeName = type_.__name__

			else:
				typeName = inputTypeName

			attrVal = {'_attr_val': attrVal, 
						'_attr_type': typeName, 
						'_attr_set': inputAttrSet}
				
		return attrVal

	def makeSerialList(self, inputList):

		outputList = []
		for inputVal in inputList:
			outputVal = self.makeSerializable(inputVal)
			outputList.append(outputVal)
		
		if isinstance(inputList, tuple):
			outputList = tuple(outputList)
		
		return outputList

	def makeSerialDict(self, inputDict):

		outputDict = {}
		for inputKey, inputVal in inputDict.items():
			outputVal = self.makeSerializable(inputVal)
			outputDict[inputKey] = outputVal
		
		return outputDict

	def makePar(self, par):

		outputPar = {}
		outputPar['val'] = par.val
		outputPar['eval'] = par.eval()
		outputPar['expr'] = par.expr
		outputPar['mode'] = str(par.mode)
		outputPar['owner'] = par.owner.path
		outputPar['name'] = par.name

		return outputPar

	def SetAttrs(self, attrDict, setProperty=True, obj=None):

		if not obj:
			obj = self

		if hasattr(self, '__FILTER_SET_ATTR__'):
			
			self.__FILTER_SET__ += tuple(self.__FILTER_SET_ATTR__)
			

		for attrName, attrVal in attrDict.items():
			if self.isBasicTypes(attrVal):
				if attrVal['_attr_set'] and attrName not in self.__FILTER_SET__:
					
					if attrVal['_attr_type'] == 'tuple':
						attrVal['_attr_val'] = tuple(attrVal['_attr_val'])
					
					setattr(obj, attrName, attrVal['_attr_val'])

			else:
				attr = self.makeNotBasicType(attrVal)

				if (attr != '__noSet__' and 
					attrVal['_attr_set'] and 
					attrName not in self.__FILTER_SET__):

					setattr(obj, attrName, attr)
	
	def isBasicTypes(self, data):

		if isinstance(data, dict):	
			if data['_attr_type'] in ('bool', 'int', 'float', 'str', 'NoneType'):
				return True

			elif data['_attr_type'] in ('tuple', 'list'):
				return all(self.isBasicTypes(x) for x in data['_attr_val'])
			
			elif data['_attr_type'] == 'dict':
				return all(isinstance(key, str) and self.isBasicTypes(val) 
												for key,val in data['_attr_val'].items())

		elif isinstance(data, (float, int, list, tuple, dict, str, type(None))):
			return True

		return False

	def makeNotBasicType(self, attrVal):
	
		setProperty = True

		if attrVal['_attr_type'] in ('tuple', 'list'):	
			return self.makeList(attrVal)
		
		elif attrVal['_attr_type'] == 'dict':			
			return self.makeDict(attrVal)
		
		elif attrVal['_attr_type'] == 'property':
			if setProperty:				
				return self.makeProperty(attrVal)

			return '__noSet__'

		elif attrVal['_attr_type'] == 'OP':
			return op(attrVal['_attr_val'])

		elif attrVal['_attr_type'] == 'Par':
			OP = op(attrVal['_attr_val']['owner'])
			return getattr(OP.par, attrVal['_attr_val']['name'])

		else:
			# make returned attribute of type specified
			attr = type(attrVal['_attr_type'], (), {})()
			for key, val in attrVal['_attr_val'].items():

				if val['_attr_type'] in ('int', 'float', 'str', 'bool', 'NoneType'):
					# set attribute of returned attribute
					setattr(attr, key, val['_attr_val'])
				
				else:
					# set attribute of returned attribute
					setattr(attr, key, self.makeNotBasicType(val))
					
			return attr

	def makeList(self, inputList):

		outputList = []
		for inputVal in inputList['_attr_val']:
			if self.isAttrDict(inputVal):

				if self.isBasicTypes(inputVal):
					attr = inputVal['_attr_val']

				else:
					attr = self.makeNotBasicType(inputVal)

				outputList.append(attr)

			else:				
				print('not attrDict:', inputList)
			
		if inputList['_attr_type'] == 'tuple':
			outputList = tuple(outputList)

		return outputList

	def makeDict(self, inputDict):

		outputDict = {}
		for inputKey, inputVal in inputDict['_attr_val'].items():
			if self.isAttrDict(inputVal):
				if self.isBasicTypes(inputVal):
					attr = inputVal['_attr_val']

				else:
					attr = self.makeNotBasicType(inputVal)
			
				outputDict[inputKey] = attr			

		return outputDict

	def makeProperty(self, attrVal):

		if isinstance(attrVal['_attr_val'], (int, float, str, bool, type(None))):
			return attrVal['_attr_val']

		elif isinstance(attrVal['_attr_val'], dict):
			return self.makeNotBasicType(attrVal['_attr_val'])

		elif isinstance(attrVal['_attr_val'], (list, tuple)):
			return self.makeList(attrVal['_attr_val'])

		return  '__noSet__'

	def isAttrDict(self, item):

		if isinstance(item, dict):
			if item.get('_attr_val'):
				return True

		return False


		

