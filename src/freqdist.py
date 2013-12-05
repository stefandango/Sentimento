import nltk

#	Call:
#		fd = FrequencyDistribution(contents, 4)   
#		print fd.distribution.items()[:20];
#

class FrequencyDistribution:

	def __init__(self, contents, threshold):
		self.threshold = threshold
		self.distribution = self.__ComputeFrequencyDistribution(contents)

	def Print(self):
		print self.distribution.items()[:20]

	def ChartString(self):
		output_str = str(self.distribution.items()[:20])
		output_str = output_str.replace("(", "[")
		output_str = output_str.replace(")", "]")
		output_str = output_str.replace("[[", "[['Word', 'Occurrences'], [")
		return output_str

	def __ComputeFrequencyDistribution(self, contents):
		#remove bad characters
		contents = self.__RemoveBadChars(contents)
		#tokenize
		tokenized_words = nltk.tokenize.word_tokenize(contents)
		#remove Stopwords
		removed_stopwords = self.__RemoveStopwords(tokenized_words)
		#remove words below some length-threshold
		thresholded = self.__RemoveThreshold(removed_stopwords, self.threshold)
		return nltk.FreqDist(thresholded)

	def __RemoveBadChars(self, text):
		badchars = open('badchars.data').read().splitlines()
		for badchar in badchars:
			text = text.replace(badchar, "")
		return text

	def __RemoveStopwords(self, wordlist):
		danishstopwords = open('danishstopwords.data').read().splitlines()
		return [ word for word in wordlist if word not in danishstopwords]

	def __RemoveThreshold(self, words, threshold):
		return [word for word in words if len(word) >= threshold]