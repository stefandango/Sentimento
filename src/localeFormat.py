#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
"""
import re
import datetime

__version__ = 1.00
__author__ = ""
__all__ = ["localeFormat"]

class LocaleFormat:
    """
    Documentaion

    """

    def __init__(self):
        self.locale = {
                        "C":
                            {
                                "long": ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"],
                                "short": ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
                            },
                        "da_DK": 
                            {
                                "long": ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"],
                                "short": ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
                            }

                    }

    def strptime(self, dateString, format, langFrom, langTo):
        localFormattedDateString = self.localeFormatV2(dateString, format, langFrom, langTo)
        date = datetime.datetime.strptime(localFormattedDateString, format)
        return date

    def localeFormatV2(self,  dateString, format, langFrom, langTo):
        dateStringLower = dateString.lower()
        dateStringList = re.split('; |, |\*|\n|\ |\.|\:', dateStringLower)
        formatStringList = re.split('; |, |\*|\n|\ |\.|\:', format)
        
        for identifier in formatStringList:
            if identifier == "%B":
                index = formatStringList.index("%B")
                localeWord = dateStringList[index]
                wordIndex = self.locale[langFrom]["long"].index(localeWord)
                newWord = self.locale[langTo]["long"][wordIndex]
                formattedDateString = dateStringLower.replace(localeWord, newWord)
                return formattedDateString

            elif identifier == "%b":
                index = formatStringList.index("%b")
                localeWord = dateStringList[index]
                wordIndex = self.locale[langFrom]["short"].index(localeWord)
                newWord = self.locale[langTo]["short"][wordIndex]
                formattedDateString = dateStringLower.replace(localeWord, newWord)
                return formattedDateString

""" Test med denne dobbeltloop
    def localeFormatV1(self, dateString, langFrom, langTo):
        dateStringLower = dateString.lower()
        dateStringList = re.split('; |, |\*|\n|\ |\.|\:', dateStringLower)

        for word in dateStringList:
            for month in self.locale[langFrom]["long"]:
                if word == month:
                    index = self.locale[langFrom]["long"].index(word)
                    newWord = self.locale[langTo]["long"][index]
                    formattedDateString = dateStringLower.replace(word, newWord)
                    return formattedDateString
            for month in self.locale[langFrom]["short"]:
                if word == month:
                    index = self.locale[langFrom]["short"].index(word)
                    newWord = self.locale[langTo]["short"][index]
                    formattedDateString = dateStringLower.replace(word, newWord)
                    return formattedDateString
"""


if __name__ == "__main__":
    # args: e.g. "da_DK" "C" "20. Oktober 2013, 18:43"
    # arg ekstra: "%d. %B %Y, %H:%M"
    import sys
    args = sys.argv
    lf = LocaleFormat()
    #print "V1"
    #print lf.localeFormatV1("20. Okt 2013, 18:43", "da_DK", "C")
    print "before: " + "20. Okt 2013, 18:43"
    print "after: " + lf.localeFormatV2("20. Okt 2013, 18:43", "%d. %b %Y, %H:%M", "da_DK", "C")
    print "As an obj: "
    print lf.strptime("20. Okt 2013, 18:43", "%d. %b %Y, %H:%M", "da_DK", "C")


