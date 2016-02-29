import inspect

def hasMethod(_object, _methodName):
	#   Returns True if _object has a method named _methodName
	for name, _ in inspect.getmembers(_object, inspect.ismethod):
		if name == _methodName:
			return True
	return False
