import pprint
class ObjectData:

	def __init__(self):
		pass
	
	def isSerializable(self, data):

		if data is None:
			return True
		elif isinstance(data, (bool, int, float)):
			return True
		elif isinstance(data, (tuple, list)):
			return all(self.isSerializable(x) for x in data)
		elif isinstance(data, dict):
			return all(isinstance(key, str) and self.isSerializable(val) for key,val in data.items())
		return False

	def makeSerialList(self, inputList):
		outputList = []
		for inputItem in inputList:
			t_ = type(inputItem)
			tName = t_.__name__
			inputItemVal = self.makeSerializable(inputItem)
			val = {'_attr_val': inputItemVal, '_attr_type': tName, '_attr_set': True}
			outputList.append(val)
		
		if isinstance(inputList, tuple):
			outputList = tuple(outputList)
		
		return outputList


	def makeSerializable(self, attrVal):

		if isinstance(attrVal, (list, tuple)):
			l = []
			for val in attrVal:
				type_ = type(val)
				typeName = type_.__name__
				
				if isinstance(val, (list, tuple)):
					newVal = []
					for item in val:
						t_ = type(item)
						tName = t_.__name__
						itemVal = self.makeSerializable(item)
						v = {'_attr_val': itemVal, '_attr_type': tName, '_attr_set': True}
						newVal.append(v)
					
					if isinstance(val, tuple):
						newVal = tuple(newVal)
					val = newVal
				
				elif isinstance(val, dict):
					newVal = {}

					for k, item in val.items():
						t_ = type(item)
						tName = t_.__name__
						itemVal = self.makeSerializable(item)
						v = {'_attr_val': itemVal, '_attr_type': tName, '_attr_set': True}
						newVal[k] = v
					
					val = newVal				
				
				else:
					val = self.GetAttrs(obj=val)
				
				v = {'_attr_val': val, '_attr_type': typeName, '_attr_set': True}
				l.append(v)

			if isinstance(attrVal, tuple):
				l = tuple(l)

			attrVal = l
			

		elif isinstance(attrVal, dict):
			d = {}
			for key, val in attrVal.items():

				type_ = type(val)
				typeName = type_.__name__

				if isinstance(val, (list, tuple)):
					newVal = []
					for item in val:
						t_ = type(item)
						tName = t_.__name__
						itemVal = self.makeSerializable(item)
						v = {'_attr_val': itemVal, '_attr_type': tName, '_attr_set': True}
						newVal.append(v)
					
					if isinstance(val, tuple):
						newVal = tuple(newVal)
					val = newVal

				elif isinstance(val, dict):
					newVal = {}

					for k, item in val.items():
						t_ = type(item)
						tName = t_.__name__
						itemVal = self.makeSerializable(item)
						v = {'_attr_val': itemVal, '_attr_type': tName, '_attr_set': True}
						newVal[k] = v
					
					val = newVal
				else:
					val = self.GetAttrs(obj=val)
				
				v = {'_attr_val': val, '_attr_type': typeName, '_attr_set': True}

				d[key] = v
			attrVal = d

		else:
			attrVal = self.GetAttrs(obj=attrVal)
			pass
		return attrVal

	def GetAttrs(self, obj=None):
		
		if not obj:
			obj = self

		baseTypes = (int, float, bool, list, tuple, dict, str)
	
		# get instance attributes
		attrs = {}
		if obj.__class__.__module__ not in ('td', 'tdu'):
			for attrName, attrVal in obj.__dict__.items():
				
				type_ = type(attrVal)
				typeName = type_.__name__	
				set_ = attrVal.__class__.__module__ not in ('td', 'tdu')
	
				if not self.isSerializable(attrVal):
					attrVal = self.makeSerializable(attrVal)
				
				attrs[attrName] = {'_attr_val': attrVal, '_attr_type': typeName, '_attr_set': set_}

			# get class attributes that are not callable
			if hasattr(obj.__class__, '__dict__'):

				for attrName in obj.__class__.__dict__.keys():
					if attrName[:2] != '__':		
						# check for static or class method
						value = getattr(obj.__class__, attrName)
						
						if not callable(value):			
							type_ = type(value)
							typeName = type_.__name__
							set_ = value.__class__.__module__ not in ('td', 'tdu')

							if type_ != property:
								if not self.isSerializable(value):
									value = self.makeSerializable(value)
								else:
									value = getattr(obj, attrName)
								#set_ = True

							else:
								set_ = value.fset != None

								
								if not self.isSerializable(value.__get__(obj)):

									t_ = type(getattr(obj, attrName))
									tName = t_.__name__

									val = self.makeSerializable(getattr(obj, attrName))
									value = {'_attr_val': val, '_attr_type': tName, '_attr_set': set_}

								else:

									value = getattr(obj, attrName)			
							
							attrs[attrName] = {'_attr_val': value, '_attr_type': typeName, '_attr_set': set_}


		return attrs



	def isAttrDict(self, item):
		if isinstance(item, dict):
			if item.get('_attr_val'):
				return True
		return False


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

	def isBasicTypes(self, data):

		if isinstance(data, dict):
			
			if data['_attr_type'] in ('bool', 'int', 'float', 'str', 'NoneType'):
				return True
			elif data['_attr_type'] in ('tuple', 'list'):
				return all(self.isBasicTypes(x) for x in data['_attr_val'])
			
			elif data['_attr_type'] == 'dict':
				return all(isinstance(key, str) and self.isBasicTypes(val) for key,val in data['_attr_val'].items())

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
		
	def SetAttrs(self, objData, setProperty=True, obj=None):

		if not obj:
			obj = self

		for attrName, attrVal in objData.items():

			if self.isBasicTypes(attrVal):

				if attrVal['_attr_set']:

					setattr(obj, attrName, attrVal['_attr_val'])
			else:
				#debug('SetAttrs Set:', attrName)

				attr = self.makeNotBasicType(attrVal)


				if attr != '__noSet__' and attrVal['_attr_set']:
					setattr(obj, attrName, attr)
