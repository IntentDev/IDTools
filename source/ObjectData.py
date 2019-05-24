import pprint
class ObjectData:

	def __init__(self):
		pass

	def GetAttrs(self, obj=None):
		
		if not obj:
			obj = self

		attrs = {}
		if obj.__class__.__module__ not in ('td', 'tdu'):

			# get instance attributes
			for attrName, attrVal in obj.__dict__.items():			
				type_ = type(attrVal)
				typeName = type_.__name__	
				attrSet = attrVal.__class__.__module__ not in ('td', 'tdu')
	
				if not self.isSerializable(attrVal):
					attrVal = self.makeSerializable(attrVal, returnDict=False)
				
				attrs[attrName] = {'_attr_val': attrVal, 
									'_attr_type': typeName, 
									'_attr_set': attrSet}

			# get class attributes that are not callable
			if hasattr(obj.__class__, '__dict__'):
				for attrName in obj.__class__.__dict__.keys():
					if attrName[:2] != '__':

						# check for static or class method
						attrVal = getattr(obj.__class__, attrName)
						if not callable(attrVal):			
							type_ = type(attrVal)
							typeName = type_.__name__
							attrSet = attrVal.__class__.__module__ not in ('td', 'tdu')

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
							
							attrs[attrName] = {'_attr_val': attrVal, 
												'_attr_type': typeName, 
												'_attr_set': attrSet}

		return attrs

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


	def SetAttrs(self, objData, setProperty=True, obj=None):

		if not obj:
			obj = self

		for attrName, attrVal in objData.items():
			if self.isBasicTypes(attrVal):
				if attrVal['_attr_set']:
					setattr(obj, attrName, attrVal['_attr_val'])

			else:
				attr = self.makeNotBasicType(attrVal)

				if attr != '__noSet__' and attrVal['_attr_set']:
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

		elif isinstance(data, (float, int, list, tuple, dict, type(None))):
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


		

