#Mr. Crawley Language Parser

from Actions import *

class TextParser(object):
    def parse(self, inputText):
        lineNumber = 0
        for line in inputText.split("\n"):
            self.parseLine(line, lineNumber)
            lineNumber += 1

    def parseLine(self, line, lineNumber):
        sectionNumber = 0
        for codeSection in line.lower().split(" get "):
            SectionParser().parse(codeSection, sectionNumber, lineNumber)
            sectionNumber += 1

class SectionParser(object):
    def parse(self, codeSection, sectionNumber, lineNumber):
        if sectionNumber = 0:
            ActionParser().parse(codeSection, lineNumber)
        elif sectionNumber = 1:
            GetParser().parse(codeSection, lineNumber)
        else
            raise CrawleyParserException("Invalid code section found")

class ActionParser(object):
    def __init__(self):
        self.actions = [First, Last, For]

    def parse(self, codeSection, lineNumber):
        ##TODO
        pass

    def parseAction(self, word, lineNumber):
        for action in self.actions:
            if word == action().__str__():
                self.addAction(action, lineNumber)
                return
        raise CrawleyActionNotFoundException("Action Not Found")

    def addAction(self, action, lineNumber):
        ##TODO
        pass

class GetParser(object):
    def parse(self, codeSection, lineNumber):
        ##TODO
        pass

class CrawleyParserException(Exception):
    def __init__(self, message):
        self.message = message
