#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
:mod:`FrequencyDistribution` -- Computes the word distribution of a string.
===========================================================================

:synopsis: Computes the word distribution of a given string, and only for word
			over a given treshold.

Requirements::
	1. 	You will need to install the ntlk library to run this code.
		http://www.nltk.org/download
    2.  Run the code in an 2.7 environment
"""

import nltk
import sys

__version__ = 1.00
__author__ = "Group 21"
__all__ = ["freqdist"]

class FrequencyDistribution:
	"""Computes the Frequency Distribution."""
	def __init__(self, contents, threshold):
		"""
		Kwargs:
			contents (str) - The string to compute the word distribution on.
			threshold (int) - The minimum number of characters in a word to be considered.
		"""
		self.threshold = threshold
		self.distribution = self.__ComputeFrequencyDistribution(contents)
	
	def __ComputeFrequencyDistribution(self, contents):
		"""
		Performs the actual frequency distribution.
		
		Args:
            contents (str) - a string with the contents used to compute the frequency distribution
		Returns:
			nltk.FreqDist (List) - A sorted list of tuples, indicating the frequency for each word.
		"""
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
		"""
		Removes bad characters from the contents.
		
		Args:
            text (str) - a string with the contents.
		Returns:
			text (str) - the input string, stripped for bad characters.
		"""
		badchars = open('badchars.data').read().splitlines()
		for badchar in badchars:
			text = text.replace(badchar, "")
		return text

	def __RemoveStopwords(self, wordlist):
		"""
		Removes danish stopwords contents.
		
		Args:
            text (str) - a string with the contents.
		Returns:
			(list) - A list of words from the input string, stripped for danish stopwords.
		"""
		danishstopwords = open('danishstopwords.data').read().splitlines()
		return [ word for word in wordlist if word not in danishstopwords]

	def __RemoveThreshold(self, words, threshold):
		"""
		Removes words from a list, that are shorter than the threshold.
		
		Args:
            words (list) - a string with the contents.
			threshold (int) - The minimum number of characters in a word to be considered.
		Returns:
			(list) - A list of words from the input string, stripped for danish stopwords.
		"""
		return [word for word in words if len(word) >= threshold]
	
	def Print(self, entries=20):
		"""
		Prints the contents of the word distribution.
		
		Args:
            entries (int) - The max number of entries to return, default is 20.
		"""
		print self.distribution.items()[:entries]

	def ChartString(self, entries=20):
	"""
		Creates a string to be used as input for a Google chart.
		
		returns 
		Args:
            entries (int) - The max number of entries to return, default is 20.
		
		Returns:
			output_str (str) - A string formatted to be used for a Google chart.
		"""
		output_str = str(self.distribution.items()[:entries])
		output_str = output_str.replace("(", "[")
		output_str = output_str.replace(")", "]")
		output_str = output_str.replace("[[", "[['Word', 'Occurrences'], [")
		return output_str
		
if __name__ == "__main__":
	import sys
	args = sys.argv
	contents = args[1]
	threshold = args[2]

	fd = FrequencyDistribution(contents, threshold)
	fd.Print()
	
	
