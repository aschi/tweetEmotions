
class Logger:
	def __init__(self, filename):
		self.f = open(filename, 'w')

	def log(self, text):
		print text
		self.f.write(text +"\n")

	def finalize(self):
		self.f.close()

	def __del__(self):
		self.f.close()