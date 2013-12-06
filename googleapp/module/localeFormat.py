#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
:mod:`localeformat` -- Additional locale module
===============================================

:synopsis: provide an alternative method to datetime's strptime, 
              taking an additional two language parameter to convert to another language

Requirements::
    1.  Run the code in an 2.7 environment

"""
import re
import datetime

__version__ = 1.00
__author__ = "Group 21"
__all__ = ["localeformat"]

class LocaleFormat:
    """ Formatting methods for at date string """

    def __init__(self):
        """
        Holds the languges that is provided by the module. More can be added for multilanguage usage.
        """
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
        """Return a datetime object from a international date string

        Args:
            dateString (str) - a string describing a date. E.g. "20. Okt 2013, 18:43"
            format (str) - a string describing the format of the dateString. E.g. '%d. %b %Y, %H:%M'
            langForm (str) - the dateString langeuge in locale format. E.g. "da_DK"
            langto (str) - the lange to which the string should be parsed in locale format. E.g. "C"

        Returns:
            (datetime) A datetime object initialized with the time specified be the arguments
        """
        localFormattedDateString = self.localeFormat(dateString, format, langFrom, langTo)
        date = datetime.datetime.strptime(localFormattedDateString, format)
        return date

    def localeFormat(self,  dateString, format, langFrom, langTo):
        """Converts the international date string to a date string in any other language

        Args:
            dateString (string) - a string describing a date. E.g. "20. Okt 2013, 18:43"
            format (string) - a string describing the format of the dateString. E.g. '%d. %b %Y, %H:%M'
            langForm - the dateString langeuge in locale format. E.g. "da_DK"
            langto - the lange to which the string should be parsed in locale format. E.g. "C"

        Returns:
            (string) a date string translated to the specified language

        """
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
    import sys
    args = sys.argv
    lf = LocaleFormat()
    print lf.localeFormatV2("20. Okt 2013, 18:43", "%d. %b %Y, %H:%M", "da_DK", "C")
    print lf.strptime("20. Okt 2013, 18:43", "%d. %b %Y, %H:%M", "da_DK", "C")


