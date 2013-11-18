#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Module Sentiment Analysis
Words list credits: language assessment by Mechanical Turk 1.0
"""
import urllib2
import codecs

__version__ = 1.00
__author__ = "s092874"
__all__ = ["SentimentAnalysis"]

class SentimentAnalysis:
    """
    The SentimentAnalysis module determines a value from a 1 to 10 scale. The 
    number indicate whether a given text is positive, negative, or neutral. 10 
    beeing the upper positive limit. The module supplies one function, 
    moodscore(). For example:    
    
    >>> sa = SentimentAnalysis()
    >>> sa.moodscore(['love'])
    8.42
    
    >>> sa.moodscore(['xyz'])
    5.5
    
    >>> sa.moodscore(['love', 'hate', 'xyz'])
    5.38


    Alternatively use it with the command:
    
    python SentimentAnalysis.py love hate xyz

    """

    def __init__(self):
        self.moodscoreDict = self._moodscoreDict()

        # @TODO: move filename

    def _moodscoreDict(self):
        """
        Returns words and values
        """
        filename = "AFINN.da-19.txt"
        respond_lines = codecs.open(filename, "r", "utf-8").readlines()
        respond_lines_splitted = [line.split('\t') for line in respond_lines]
        #print respond_lines_splitted
        moodscore_dict = dict(map(lambda (line): (line[0], float(line[1])),
            respond_lines_splitted))
        #print moodscore_dict
        return moodscore_dict

    def moodscore(self, words):
        """
        Returns a single value
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