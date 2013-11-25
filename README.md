## PyJsonKit Documents

-----

### how to use it.
	import JsonParser

#### 1、load json to python object
	parser = JsonParser.JsonParser()
	parser.load(json) # param is json. i.e. '{"name":"wufulin","age":24}'

#### 2、dump python object to json
	parser = JsonParser.JsonParser()
	parser.dump(pythonObject) # param is python object. i.e. [2, [2,(2,3)]]

#### 3、loadJson that load json text from file 
	parser = JsonParser.JsonParser()
	parser.loadJson(filePath) # param is file path that stores json text.

#### 4、 dumpJson that dump python object in file
	parser = JsonParser.JsonParser()
	parser.dumpJson(filePath, pythonObject) 
	# param 1 is file path that stores json text, param 2 is python object.

#### 5、loadDict 
	parser = JsonParser.JsonParser()
	parser.loadDict(dct) # param is json object.

#### 6、dumpDict
	parser = JsonParser.JsonParser()
	parser.dumpDict(python dict) # param is python dict type.