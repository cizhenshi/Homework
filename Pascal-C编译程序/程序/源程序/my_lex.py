import ply.lex as lex
#from my_yacc_debug import TextBrowser
import my_yacc_debug
tokens = ('NUM', 'ID', 'FLOAT', 'CHARACTER', 'RELOP', 'MULOP', 'ASSIGNOP', 'TOTO', 'ARRAY', 'BEGIN', 'CASE',
'DO', 'TO','DOWNTO', 'ELSE', 'FOR', 'FUNCTION', 'END', 'PROGRAM', 'CONST', 'OF', 'OR', 'NOT', 'PROCEDURE', 'RECORD',
'REPEAT', 'IF', 'THEN', 'TYPE', 'UNTIL', 'VAR', 'WHILE', 'CHAR', 'REAL', 'INTEGER', 'BOOLEAN','READ','WRITE','TRUE','FALSE')

# literals = [ '+','-', '(', ')', ',', ';', '=', '[', ']', ':', '.', ]

#keyword_list
Key_list=['ARRAY', 'BEGIN', 'CASE','DO', 'TO','DOWNTO', 'ELSE', 'FOR', 'FUNCTION', 'END', 'PROGRAM', 'CONST', 'OF', 'OR', 'NOT', 'PROCEDURE', 'RECORD',
'REPEAT', 'IF', 'THEN', 'TYPE', 'UNTIL', 'VAR', 'WHILE', 'CHAR', 'REAL', 'INTEGER', 'BOOLEAN','READ','WRITE','FALSE','TRUE']

#idetifier
def t_MULOP(t):
    r"\*|/| div | mod | and "
    ##t.lexpos=find_column(input_data,t)
    return t

def t_ID(t):
    r'[a-z][a-z0-9]*'
   # t.lexpos=find_column(input_data,t)
    if t.value.upper() in Key_list:
        t.type =Key_list[Key_list.index(t.value.upper())]
    return t

def t_FLOAT(t):
    r"\d+\.\d+e[+-]{0,1}\d+|\d+\.\d+"
    ##t.lexpos=find_column(input_data,t)
    t.value=float(t.value)
    return t

def t_NUM(t):
    r'\d+e[+-]{0,1}\d+|\d+'
    ##t.lexpos=find_column(input_data,t)
    t.value = int(t.value)
    return t

def t_CHARACTER(t):
    r'\'[\s\S]\''
    ##t.lexpos=find_column(input_data,t)
    t.value=t.value[1]
    return t

def t_RELOP(t):
    r"<>|<=|<|>=|>"
    ##t.lexpos=find_column(input_data,t)
    return t



def t_ASSIGNOP(t):
    r':='
    ##t.lexpos=find_column(input_data,t)
    return t

def t_TOTO(t):
    r"\.\."
    ##t.lexpos=find_column(input_data,t)
    return t

def t_newline(t):
    r'\n+'
    ##t.lexpos=find_column(input_data,t)
    t.lexer.lineno += len(t.value)

def t_annotation(t):
    r"{[\s\S]*}"
    pass

t_ignore=' |\t'

def t_error(t):
    ##t.lexpos=find_column(input_data,t)
    print("(",t.lineno,",",t.lexpos,")","Error:Illegal expression:",t.value[0])
    my_yacc_debug.TextBrowser.append("Error:Illegal expression: "+str(t.value[0])+" at line "+str(t.lineno))
    t.lexer.skip(1)

literals = [ '+','=','-',',',';','.',':','[',']','(',')' ]

# def find_column(input,token):
#     last_cr = input.rfind('\n',0,token.lexpos)
#     if last_cr < 0:
#         last_cr = -1
#     column = (token.lexpos - last_cr)
#     return column
# with open("test.txt") as f:
#         input_data = f.read()
# lexer=lex.lex()
