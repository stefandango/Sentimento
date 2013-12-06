#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
:mod:`SentimentAnalysis` -- Sentiment Analysis Module 
===============================================

:synopsis: the module is used to determine how positive 
                or negative an attidude a given text have, the moodscore. 
                From a text a float is returned with the result.

Requirements::
    1.  You need to install the codecs module

Notes::
    Credit for the word list used goes to Finn Årup Nielsen
"""

import urllib2
import codecs

__version__ = 1.00
__author__ = "Gruppe 21"
__all__ = ["SentimentAnalysis"]

class SentimentAnalysis:
    """Calculating moodscore from wordlist"""

    def __init__(self):
        self.moodscoreDict = self._moodscoreDict()

        # @TODO: move filename

    def _moodscoreDict(self):
        """Initializes the dictionary used to look up the moodscore for a given word

        Args:
            None

        Returns:
            (dict) The dictionary hold keys and values, words and moodscore correspondly
        
        """
        filename = "AFINN.da-19.txt"
        respond_lines = codecs.open(filename, "r", "utf-8").readlines()
        respond_lines_splitted = [line.split('\t') for line in respond_lines]
        moodscore_dict = dict(map(lambda (line): (line[0], float(line[1])),
            respond_lines_splitted))
        return moodscore_dict

    def moodscore(self, words):
        """The method is used for calculating the moodscore. 
        Args:
            (list) a list of words

        Returns:
            (float) the moodscore calculated from all the words in the list given

        """
        numerator = 0
        denominator = 0
        for word in words:
            if(word in self.moodscoreDict):
                numerator += self.moodscoreDict[word]
                denominator += 1
        if denominator != 0:
            res = numerator / denominator
            return res
        return 5.5



if __name__ == "__main__":
    import sys
    sa = SentimentAnalysis()
    print sa.moodscore(sys.argv)