class Error():
	def __init__(self, name, help=""):
		self.name = name
		self.help = help

	def __call__(self, c, *com):
		print("[{0}]: {1}\n(line {2})".format(self.name, '\n'.join(com), c))
		print(self.help)
		exit(0)

class Warning(Error):
	def __call__(self, c, *com):
		print("[{0}]: {1}\n(line {2})".format(self.name, "\n".join(com), c))
		print(self.help)

dataSectionError  = Error("DataSectionError", "Invalid section")
syntaxError       = Error("SyntaxError")
fileNotFound      = Error("FileNotFound")
nameError     	  = Error("NameError")
headError		  = Error("HeadError", "No head in loaded file")
expressionError   = Error("ExpressionError")
expressionWarning = Warning("ExpressionWarning")
valueError 		  = Error("ValueError")  
dataSizeError     = Error("dataSizeError")