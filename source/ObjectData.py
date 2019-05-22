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

	def makeSerializable(self, attrVal):

		if isinstance(attrVal, (list, tuple)):
			l = []
			for val in attrVal:
				type_ = type(val)
				typeName = type_.__name__
				
				if isinstance(val, (list, tuple)):
					newVal = []
					for item in val:
						type_ = type(item)
						typeName = type_.__name__
						itemVal = self.makeSerializable(item)
						v = {'value': itemVal, 'type': typeName, 'set': True}
						newVal.append(v)
					
					if isinstance(val, tuple):
						newVal = tuple(newVal)
					val = newVal
				
				elif isinstance(val, dict):
					newVal = {}

					for k, item in val.items():
						type_ = type(item)
						typeName = type_.__name__
						itemVal = self.makeSerializable(item)
						v = {'value': itemVal, 'type': typeName, 'set': True}
						newVal[k] = v
					
					val = newVal				
				
				else:
					val = self.GetAttrs(obj=val)
				
				v = {'value': val, 'type': typeName, 'set': True}
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
						type_ = type(item)
						typeName = type_.__name__
						itemVal = self.makeSerializable(item)
						v = {'value': itemVal, 'type': typeName, 'set': True}
						newVal.append(v)
					
					if isinstance(val, tuple):
						newVal = tuple(newVal)
					val = newVal

				elif isinstance(val, dict):
					newVal = {}

					for k, item in val.items():
						type_ = type(item)
						typeName = type_.__name__
						itemVal = self.makeSerializable(item)
						v = {'value': itemVal, 'type': typeName, 'set': True}
						newVal[k] = v
					
					val = newVal
				else:
					val = self.GetAttrs(obj=val)
				
				v = {'value': val, 'type': typeName, 'set': True}

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

		for attrName, attrVal in obj.__dict__.items():
			
			type_ = type(attrVal)
			typeName = type_.__name__	

			if not self.isSerializable(attrVal):
				attrVal = self.makeSerializable(attrVal)

			attrs[attrName] = {'value': attrVal, 'type': typeName, 'set': True}

		# get class attributes that are not callable
		for attrName in obj.__class__.__dict__.keys():
			if attrName[:2] != '__':		
				# check for static or class method
				value = getattr(obj.__class__, attrName)
				
				if not callable(value):			
					type_ = type(value)
					typeName = type_.__name__

					if type_ != property:
						if not self.isSerializable(value):
							value = self.makeSerializable(value)
						else:
							value = getattr(obj, attrName)
						attrSet = True

					else:
						attrSet = value.fset != None

						
						if not self.isSerializable(value.__get__(obj)):

							t_ = type(getattr(obj, attrName))
							tName = t_.__name__

							val = self.makeSerializable(getattr(obj, attrName))
							value = {'value': val, 'type': tName, 'set': attrSet}

						else:

							value = getattr(obj, attrName)			
					
					attrs[attrName] = {'value': value, 'type': typeName, 'set': attrSet}
	
		return attrs

	def makeList(self, attrVal):

		l = []

		for listVal in attrVal['value']:

			if isinstance(listVal, dict):

				if listVal.get('value'):
					
					attr = type(listVal['type'], (), {})()
					for key, val in listVal['value'].items():

						if val['type'] in ('int', 'float', 'str', 'bool', 'NoneType'):
							setattr(attr, key, val['value'])
						else:
							setattr(attr, key, self.makeNotBasicType(val))

					l.append(attr)

				else:

					l.append(self.makeDict(listVal))
			
			elif isinstance(listVal, (list, tuple)):

				l.append(self.makeList(listVal))




		return l

	def makeDict(self, attrVal):

		d = {}
		if attrVal.get('value'):
			for dictKey, dictVal in attrVal['value'].items():

				if isinstance(dictVal, dict):

					if dictVal.get('value'):

						attr = type(dictVal['type'], (), {})()
						for key, val in dictVal['value'].items():

							if val['type'] in ('int', 'float', 'str', 'bool', 'NoneType'):
								setattr(attr, key, val['value'])
							else:
								setattr(attr, key, self.makeNotBasicType(val))

						d[dictKey] = attr

					else:

						d[dictKey] = self.makeDict(dictVal)
				
				elif isinstance(dictVal, (list, tuple)):

					d[dictKey] = self.makeList(dictVal)
		else:
			d = attrVal

		return d

	def makeProperty(self, attrVal):

		if isinstance(attrVal['value'], (int, float, str, bool, type(None))):
			return attrVal['value']

		elif isinstance(attrVal['value'], dict):

			return self.makeNotBasicType(attrVal['value'])

		elif isinstance(attrVal['value'], (list, tuple)):

			return self.makeList(attrVal['value'])


		return  '__noSet__'

	def isBasicTypes(self, data):

		if isinstance(data, dict):
			if data['type'] in ('bool', 'int', 'float', 'str', 'NoneType'):
				return True
			elif data['type'] in ('tuple', 'list'):
				return all(self.isBasicTypes(x) for x in data['value'])
			
			elif data['type'] == 'dict':
				return all(isinstance(key, str) and self.isBasicTypes(val) for key,val in data['value'].items())

		elif isinstance(data, (float, int, list, tuple, dict, type(None))):
			return True

		return False

	def makeNotBasicType(self, attrVal):
		
		setProperty = True

		if attrVal['type'] in ('tuple', 'list'):
			
			l = self.makeList(attrVal)

			if attrVal['type'] == 'tuple':
				l = tuple(l)			
			
			return l
		
		elif attrVal['type'] == 'dict':
			
			return self.makeDict(attrVal)
		
		elif attrVal['type'] == 'property':

			if attrVal['set'] and setProperty:
				
				return self.makeProperty(attrVal)

			return '__noSet__'

		else:

			attr = type(attrVal['type'], (), {})()
			for key, val in attrVal['value'].items():

				if val['type'] in ('int', 'float', 'str', 'bool', 'NoneType'):
					setattr(attr, key, val['value'])
				else:
					setattr(attr, key, self.makeNotBasicType(val))

			return attr
		
	def SetAttrs(self, objData, setProperty=True, obj=None):

		if not obj:
			obj = self

		for attrName, attrVal in objData.items():

			if self.isBasicTypes(attrVal):

				if attrVal['set']:

					setattr(obj, attrName, attrVal['value'])
			else:
				debug('SetAttrs Set:', attrName)

				attr = self.makeNotBasicType(attrVal)

				if attr != '__noSet__':
					setattr(obj, attrName, attr)
