import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import re
from test import *
class MyHighlighter( QSyntaxHighlighter ):
    def __init__( self, parent ):
      QSyntaxHighlighter.__init__( self, parent )
      self.parent = parent
      self.highlightingRules = []

      keyword = QTextCharFormat()
      keyword.setForeground( Qt.darkBlue )
      keyword.setFontWeight( QFont.Bold )
      keywords = ['ARRAY', 'BEGIN', 'CASE','DO', 'TO','DOWNTO', 'ELSE', 'FOR', 'FUNCTION', 'END', 'PROGRAM',
                  'CONST', 'OF', 'OR', 'NOT', 'PROCEDURE', 'RECORD','REPEAT', 'IF', 'THEN', 'TYPE','UNTIL',
                  'VAR', 'WHILE', 'CHAR', 'REAL', 'INTEGER', 'BOOLEAN','READ','WRITE','array', 'begin',
                  'case','do', 'to','downto', 'else', 'for', 'function', 'end', 'program', 'const', 'of',
                  'or', 'not', 'procedure', 'record','repeat', 'if', 'then', 'type','until', 'var', 'while',
                  'char', 'real', 'integer', 'boolean','read','write','true','false','TRUE','FALSE']
      for word in keywords:
        pattern = QRegExp("\\b" + word + "\\b")
        rule = (pattern,keyword)
        self.highlightingRules.append( rule )

      keyword = QTextCharFormat()
      keyword.setForeground( Qt.red )
      keyword.setFontWeight( QFont.Bold )
      keywords = ["-",":=","=","\+","\*","\.\.",">","<",">=","<=","\(","\)","\[","\]",":",";"]
      for word in keywords:
        pattern = QRegExp( word )
        rule = (pattern,keyword)
        self.highlightingRules.append( rule )

    def highlightBlock( self, text ):
        for rule in self.highlightingRules:
            expression = QRegExp( rule[0] )
            index = expression.indexIn( text )
            while index >= 0:
                length = expression.matchedLength()
                substr = text[index:index+length]
                self.setFormat( index, length, rule[1] )
                index = text.find(substr,index + length)
        self.setCurrentBlockState( 0 )

