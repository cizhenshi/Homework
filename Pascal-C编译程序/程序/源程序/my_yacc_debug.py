#-*- coding: UTF-8 -*-

from __future__ import print_function
import ply.yacc as yacc
from my_lex import *
from support_functions import *

isRecord = False
id_cnt = 0

def my_print(str):
    TextBrowser.append(str)
def p_program(p):
    '''program : program_head program_body '.' '''
    fp.close()
    my_print("completed")
    #action

def p_program_head(p):
    '''program_head : PROGRAM ID '(' identifier_list ')' ';' '''
    #action
    print("#include<stdio.h>" ,file=fp)
    global id_cnt
    id_cnt = 0

def p_program_body(p):
    '''program_body : const_declarations type_declarations var_declarations subprogram_declarations O compound_statement'''
    #action
    print(p[6].str + "}", file=fp)

def p_O(p):
    '''O : empty '''
    #action
    print("main()\n{", file=fp)

def p_identifier_list(p):
    '''identifier_list : identifier_list ',' ID
                       | ID '''
    #action
    item={}
    global isRecord
    global id_cnt
    p[0] = Attribute()
    if len(p) == 4:
        id_cnt += 1
        p[0].str = p[1].str + "," + p[3]
        item["name"] = p[3]
        item["type"] = ""
        item["F_type"] = False
        item["F_const"] = False
        item["declare_line"] = p.lineno(3)
        item["extend"] = []
        item["var"] = False
        isDefined = symboltable.find(p[3], mode=1)
        if not isRecord and not isDefined:
            symboltable.insert(item)
        elif isRecord and not isDefined:
            p[0].extend = []
            p[0].extend.append(item)
        else:
            my_print(str(p[3]) + " at line" + str(p.lineno(3)) + "has already been defined")
            p[0].type = "type_error"
    else:
        p[0].str = p[1]
        id_cnt += 1
        item["name"] = p[1]
        item["type"] = ""
        item["F_type"] = False
        item["F_const"] = False
        item["declare_line"] = p.lineno(1)
        item["extend"] = []
        item["var"] = False
        isDefined = symboltable.find(p[1], mode=1)
        if not isRecord and not isDefined:
            symboltable.insert(item)
        elif isRecord and not isDefined:
            p[0].extend = []
            p[0].extend.append(item)
        else:
            my_print(str(p[1]) + " at line" + str(p.lineno(1)) + "has already been defined")
            p[0].type = "type_error"

def p_const_declarations(p):
    '''const_declarations : CONST const_declaration ';'
                          | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        print(";", file=fp)
        if p[2].type == "type_error":
            p[0].type = "type_error"

# def p_P(p):
#     ''' P : empty '''
#     #action
#     print("const ",end = "",file=fp)

def p_const_declaration(p):
    '''const_declaration : const_declaration ';' Q ID '=' const_variable
                         | ID '=' const_variable'''
    #action
    p[0] = Attribute()
    item={}
    if len(p)==7:
        print("const", p[6].type, p[4], " = ", p[6].str, end="", file=fp)
        if p[6].type != "type_error" and p[1].type != "type_error":
            if not symboltable.find(p[4]):
                item["name"] = p[4]
                item["type"] = p[6].type
                item["F_type"] = False
                item["F_const"] = True
                item["declare_line"] = p.lineno(4)
                item["extend"] = p[6].value
                item["var"] = False
                symboltable.insert(item)
            else:
                print(p[4], " at line", p.lineno(4), "has already been defined")
                p[0].type = "type_error"
        else:
            p[0].type = "type_error"
    elif len(p) == 4:
        print("const", p[3].type, p[1], " = ", p[3].str, end="", file=fp)
        if p[3].type != "type_error":
            if not symboltable.find(p[1]):
                item["name"] = p[1]
                item["type"] = p[3].type
                item["F_type"] = False
                item["F_const"] = True
                item["declare_line"] = p.lineno(1)
                item["extend"] = p[3].value
                item["var"] = False
                symboltable.insert(item)
            else:
                my_print(str(p[1]) + " at line" + str(p.lineno(4)) +  "has already been defined")
                p[0].type = "type_error"
        else:
            p[0].type = "type_error"

def p_Q(p):
    ''' Q : empty '''
    #action
    print(";", file=fp)

##modified
def p_const_variable_1(p):
    '''const_variable : '+' ID '''
    #action
    p[0] = Attribute()
    index = symboltable.find_item(p[2])
    if not index:
        p[0].type = "type_error"
        my_print(str(p[2]) + " at line" +  str(p.lineno(2)) + "is not a const variable")
    elif symboltable.table[index]["F_const"] == False:
        my_print("Bad const variable declared at line" +  str(p.lineno(2)) +  str(p[2]) + "is not a const variable")
        p[0].type = "type_error"
    else:
        p[0].type = symboltable.table[index]["type"]
        p[0].str = "+" + p[2]
        p[0].value = symboltable.table[index]["extend"]
        p[0].lineno = p.lineno(2)

#modified
def p_const_variable_2(p):
    '''const_variable : '-' ID '''
    #action
    p[0] = Attribute()
    index = symboltable.find_item(p[2])
    if not index:
        p[0].type = "type_error"
        my_print(str(p[2]) +  " at line" +  str(p.lineno(2)) +  "is not a const variable")
    elif symboltable.table[index]["F_const"] == False:
        my_print("Bad const variable declared at line" +  str(p.lineno(2)) +  str(p[2]) + "is not a const variable")
        p[0].type = "type_error"
    else:
        p[0].type = symboltable.table[index]["type"]
        p[0].str = "-" + p[2]
        p[0].value = symboltable.table[index]["extend"]
        p[0].lineno = p.lineno(2)

def p_const_variable_3(p):
    '''const_variable : '+' NUM '''
    #action
    p[0] = Attribute()
    p[0].value = p[2]
    p[0].str = "+" + str(p[2])
    p[0].type = "int"
    p[0].lineno = p.lineno(2)

def p_const_variable_4(p):
    '''const_variable : '-' NUM '''
    #action
    p[0] = Attribute()
    p[0].value = -p[2]
    p[0].str = "-" + str(p[2])
    p[0].type = "int"
    p[0].lineno = p.lineno(2)

def p_const_variable_5(p):
    '''const_variable : NUM '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = str(p[1])
    p[0].type = "int"
    p[0].lineno = p.lineno(1)

def p_const_variable_6(p):
    '''const_variable : CHARACTER '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = "\"" + p[1] + "\""
    p[0].type = "char"
    p[0].lineno = p.lineno(1)

def p_const_variable_7(p):
    '''const_variable : '+' FLOAT '''
    #action
    p[0] = Attribute()
    p[0].value = p[2]
    p[0].str = "+" + str(p[2])
    p[0].type = "float"
    p[0].lineno = p.lineno(2)

def p_const_variable_8(p):
    '''const_variable : '-' FLOAT '''
    #action
    p[0] = Attribute()
    p[0].value = -p[2]
    p[0].str = "-" + str(p[2])
    p[0].type = "float"
    p[0].lineno = p.lineno(2)

def p_const_variable_9(p):
    '''const_variable : FLOAT '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = str(p[1])
    p[0].type = "float"
    p[0].lineno = p.lineno(1)

#modified
def p_const_variable_10(p):
    '''const_variable : ID '''
    #action
    p[0] = Attribute()
    index = symboltable.find_item(p[1])
    if index == None:
        my_print(str(p[1]) + " at line" + str(p.lineno(1)) + "is not a const variable")
        p[0].type = "type_error"
    else:
        if symboltable.table[index]["F_const"] == False:
            my_print(str(p[1]) + " at line" +  str(p.lineno(1)) +  "is not a const variable")
        else:
            p[0].type = symboltable.table[index]["type"]
            p[0].str = p[1]
            p[0].value = symboltable.table[index]["extend"]
    p[0].lineno = p.lineno(1)

def p_type_declarations(p):
    '''type_declarations : TYPE R type_declaration ';'
                         | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 5:
        if p[3].type == "type_error":
            p[0].type = "type_error"

def p_R(p):
    ''' R : empty '''
    #action
    #print("typedef ", end="", file=fp)

def p_type_declaration(p):
    '''type_declaration : type_declaration ';' S ID '=' type
                        | ID '=' type '''
    #action
    p[0] = Attribute()
    item = {}
    if len(p) == 7:
        if p[6].type[0:5] != "array":
            print("typedef", p[6].type,p[4] + ";", file=fp)
        else:
            print("typedef", p[6].type[5:], p[4], end="", file=fp)
            for i in range(1, len(p[6].extend)):
                print("[", p[6].extend[i][1], "]"+";", file=fp)
        if p[6].type != "type_error":
            if not symboltable.find(p[4]):
                item["name"] = p[4]
                item["type"] = p[6].type
                item["F_type"] = True
                item["F_const"] = False
                item["declare_line"] = p.lineno(3)
                item["extend"] = p[6].extend
                item["var"] = False
                symboltable.insert(item)
            else:
                my_print(str(p[4]) +  " at line" +  str(p.lineno(4)) +  "has been declared")
                p[0].type = "type_error"
        else:
            p[0].type = "type_error"
    elif len(p) == 4:
        if p[3].type[0:5] != "array":
            print("typedef", p[3].str," ", p[1]+";", file=fp)
        else:
            print("typedef", p[3].str[5:]," ", p[1], end="", file=fp)
            for i in range(1, len(p[3].extend)):
                print("[", p[3].extend[i][1], "]" + ";", file=fp)
        if p[3].type != "type_error":
            if not symboltable.find(p[1]):
                item["name"] = p[1]
                item["type"] = p[3].type
                item["F_type"] = True
                item["F_const"] = False
                item["declare_line"] = p.lineno(1)
                item["extend"] = p[3].extend
                item["var"] = False
                symboltable.insert(item)
            else:
                my_print(str(p[1]) + " at line" +  str(p.lineno(1)) + "has been declared")
                p[0].type = "type_error"
        else:
            p[0].type = "type_error"

def p_S(p):
    ''' S : empty '''
    #action
    #print(",", end="", file=fp)

def p_type1(p):
    '''type : standard_type
            | RECORD L record_body END
            | ARRAY '[' periods ']' OF type'''
    #action
    p[0] = Attribute()
    if len(p) == 2:
        p[0].type = p[1].type
        p[0].str = p[1].type

    elif len(p) == 5:
        p[0].str = "struct\n{\n" + p[3].str + "\n}"
        if p[3].type != "type_error":
            p[0].type = "record"
            p[0].extend = p[3].extend
            global isRecord
            isRecord = False
        else:
            p[0].type = "type_error"

    elif len(p) == 7:
        if p[3].type != "type_error" and p[6].type != "type_error":
            p[0].type = "array" + p[6].type
            p[0].str = p[6].str
            p[0].extend = [p[6].type] + p[3].extend
        else:
            p[0].type = "type_error"

#modified
def p_type2(p):
    '''type : ID '''
    #action
    p[0] = Attribute()
    index = symboltable.find_item(p[1])
    if not index:
        my_print(str(p[1]) + " at line" + str(p.lineno(1)) + " is not a type")
        p[0].type = "type_error"
    else:
        flag1 = symboltable.find(p[1])
        flag2 = symboltable.table[index]["F_type"]
        if flag1 and flag2:
            p[0].name = p[1]
            p[0].str = p[1]
            p[0].type = p[1]
            p[0].extend = ""
        else:
            p[0].type = "type_error"
            if not flag2:
                my_print("Bad type declaration at line" +  str(p.lineno(1)) +  str(p[1]) +  " is not a type")
            if not flag1:
                my_print(str(p[1]) +  " at line" +  str(p.lineno(1)) + "is not declared")

def p_L(p):
    ''' L : empty '''
    global isRecord
    p[0] = Attribute()
    p[0].extend = []
    isRecord = True
    # print(",", end="", file=fp)

def p_standard_type1(p):
    '''standard_type : INTEGER  '''
    p[0] = Attribute()
    p[0].str = "int"
    p[0].type = "int"
    #action

def p_standard_type2(p):
    '''standard_type : REAL '''
    #action
    p[0] = Attribute()
    p[0].str = "float"
    p[0].type = "float"


def p_standard_type3(p):
    '''standard_type : BOOLEAN '''
    #action
    p[0] = Attribute()
    p[0].str = "int"
    p[0].type = "boolean"

def p_standard_type4(p):
    '''standard_type : CHAR '''
    #action
    p[0] = Attribute()
    p[0].str = "char"
    p[0].type = "char"

def p_record_body1(p):
    '''record_body : var_declaration '''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str
    if p[1].type != "type_error":
        p[0].extend = p[1].extend
    else:
        p[0].type = "type_error"

def p_record_body2(p):
    '''record_body : empty '''
    #action
    p[0] = Attribute()
    p[0].str = ""
    p[0].extend = []

def p_periods(p):
    '''periods : periods ',' period
               | period '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        if p[1].type != "type_error" and p[3].type != "type_error":
            p[0].extend = p[1].extend + p[3].extend
        else:
            p[0].type = "type_error"
    else:
        if p[1].type != "type_error":
            p[0].extend = p[1].extend
        else:
            p[0].type = "type_error"

def p_period(p):
    '''period : const_variable TOTO const_variable'''
    #action
    p[0] = Attribute()
    if p[1].type == "int" and p[3].type == "int" and  p[1].value < p[3].value:
        p[0].extend = [((p[1].value, p[3].value - p[1].value + 1))]
    else:
        my_print("Bad array index declaration at line" + str( p.lineno(2)))
        p[0].type = "type_error"

#gaile
def p_var_declarations(p):
    '''var_declarations : VAR var_declaration
                        | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 3:
        print(p[2].str, file=fp)
        if p[2].type == "type_error":
            p[0].type = "type_error"

#gaile
def p_var_declaration(p):
    '''var_declaration : var_declaration identifier_list ':' type ';'
                       | identifier_list ':' type ';' '''
    #action
    p[0] = Attribute()
    global isRecord
    global id_cnt

    if len(p) == 6 and not isRecord:
        if p[4].type == "type_error" or p[1].type == "type_error":
            p[0].type = "type_error"
        elif p[4].type[0:5] == "array":
            #符号表操作
            idx = symboltable.Top - 1
            for i in range(0,id_cnt):
                symboltable.table[idx - i]["type"] = p[4].type
                symboltable.table[idx - i]["extend"] = p[4].extend
            #代码生成
            p[0].str = p[1].str + "\n" + p[4].extend[0] + " "
            temp = p[2].str.split(',', 1)
            for Str in temp:
                Temp = ""
                for i in range(1, len(p[4].extend)):
                    Temp = Temp + "[" + str(p[4].extend[i][1]) + "]"
                p[0].str = p[0].str + Str + Temp + ","
            p[0].str = p[0].str[:-1] + ";"
        else:
            #符号表操作
            idx = symboltable.Top - 1
            for i in range(0, id_cnt):
                symboltable.table[idx-i]["type"] = p[4].type
                symboltable.table[idx-i]["extend"] = p[4].extend
            p[0].str = p[1].str + "\n" + p[4].str + " " + p[2].str + ";"

    elif len(p) == 6 and isRecord:
        list = p[2].extend
        length = len(list)
        for i in range(length - id_cnt, length):
            list[i]["type"] = p[4].type
            list[i]["extend"] = p[4].extend
        p[0].extend = p[1].extend + list
        if p[4].type == "type_error" or p[1].type == "type_error":
            p[0].type = "type_error"
        elif(p[4].type[0:5] == "array"):
            p[0].str = p[1].str + "\n" + p[4].extend[0] + " "
            temp = p[2].str.split(',',1)
            for Str in temp:
                Temp = ""
                for i in range(1,len(p[4].extend)):
                    Temp = Temp + "[" + str(p[4].extend[i][1])+"]"
                p[0].str = p[0].str + Str + Temp + ","
            p[0].str = p[0].str[:-1] + ";"
        else:
            p[0].str = p[1].str + "\n" + p[4].str + " " + p[2].str + ";"

    elif len(p) == 5 and not isRecord:
        if p[3].type == "type_error" or p[1].type == "type_error":
            p[0].type = "type_error"
        elif(p[3].type[0:5] == "array"):
            #符号表操作
            idx = symboltable.Top - 1
            for i in range(0,id_cnt):
                symboltable.table[idx - i]["type"] = p[3].type
                symboltable.table[idx - i]["extend"] = p[3].extend
            p[0].str = p[3].extend[0] + " "
            temp = p[1].str.split(',',1)
            for Str in temp:
                Temp = ""
                for i in range(1,len(p[3].extend)):
                    Temp = Temp + "[" + str(p[3].extend[i][1]) + "]"
                p[0].str = p[0].str + Str + Temp + ","
            p[0].str = p[0].str[:-1] + ";"
        else:
            idx = symboltable.Top - 1
            for i in range(0, id_cnt):
                symboltable.table[idx - i]["type"] = p[3].type
                symboltable.table[idx - i]["extend"] = p[3].extend
            p[0].str = p[3].str + " " + p[1].str + ";"

    elif len(p) == 5 and isRecord:
        list = p[1].extend
        length = len(list)
        for i in range(length - id_cnt, length):
            list[i]["type"] = p[3].type
            list[i]["extend"] = p[3].extend
        p[0].extend = list
        if p[3].type == "type_error" or p[1].type == "type_error":
            p[0].type = "type_error"
        elif p[3].type[0:5] == "array":
            p[0].str = p[3].extend[0] + " "
            temp = p[1].str.split(',',1)
            for Str in temp:
                Temp = ""
                for i in range(1, len(p[3].extend)):
                    Temp = Temp + "[" + str(p[3].extend[i][1]) + "]"
                p[0].str = p[0].str + Str + Temp + ","
            p[0].str = p[0].str[:-1] + ";"
        else:
            p[0].str = p[3].str + " " + p[1].str + ";"
    id_cnt = 0

def p_subprogram_declarations(p):
    '''subprogram_declarations : subprogram_declarations subprogram_declaration ';'
                               | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 3:
        symboltable.locate()
        if p[1].type == "type_error" or p[2].type == "type_error":
            p[0].type = "type_error"

def p_subprogram_declaration(p):
    '''subprogram_declaration : subprogram_head subprogram_body'''
    #action
    p[0] = Attribute()
    if p[1].type == "type_error" or p[2].type == "type_error":
        p[0].type = "type_error"
    # print(symboltable.table)
    symboltable.relocate()
    # print(symboltable.table)

def p_subprogram_body(p):
    '''subprogram_body : T const_declarations type_declarations var_declarations compound_statement LC_U'''
    #action
    p[0] = Attribute()
    if p[-1].type != "void" :
         print("return", p[-1].name + ";",file=fp)
    print("}", file=fp)
    if p[2].type == "type_error" or p[3].type == "type_error" or p[4].type == "type_error" or p[5].type == "type_error":
        p[0].type = "type_error"


def p_T(p):
    ''' T : empty '''
    # action
    print("{", file=fp)
    #函数返回参数声明
    if(p[-1].type != 'void'):
        print(p[-1].type, p[-1].name + ";", file=fp)

def p_LC_U(p):
    ''' LC_U : empty '''
    # action
    print(p[-1].str, end="",file=fp)
    #函数返回参数声明

def p_subprogram_head1(p):
    '''subprogram_head : X FUNCTION ID formal_parameter ':' standard_type ';' '''
    #action
    p[0] = Attribute()
    hasDefined = symboltable.find(p[3], mode=1)
    if not hasDefined and p[4].type != "type_error":
        fun_name = p[3] + "_function"
        print(p[6].str, fun_name, p[4].str, file=fp)
        p[0].name = p[3]
        p[0].type = p[6].type
        item = symboltable.domain_stack[1]
        symboltable.table[item]["name"] = p[3]
        symboltable.table[item]["type"] = "function"
        symboltable.table[item]["F_type"] = False
        symboltable.table[item]["F_const"] = False
        symboltable.table[item]["declare_line"] = p.lineno(3)
        symboltable.table[item]["extend"] = [p[6].type] + p[4].parameter_list
        symboltable.table[item]["var_list"]=["false"] + p[4].var_list
    elif hasDefined:
        my_print(str(p[3]) +  " at line" +  str(p.lineno(3)) +  "has already been defined")
        p[0].type = "type_error"
    else:
        p[0].type = "type_error"
def p_X(p):
    '''X : empty'''
    item = {}
    item["name"] = ""
    item["type"] = "function"
    item["F_type"] = False
    item["F_const"] = False
    item["declare_line"] = 0
    item["var"] = False
    symboltable.locate()
    symboltable.insert(item)


def p_subprogram_head2(p):
    '''subprogram_head : X FUNCTION ID formal_parameter ':' array_type ';' '''
    #action
    p[0] = Attribute()
    hasDefined = symboltable.find(p[3], mode=1)
    if not hasDefined and p[4].type != "type_error" and p[6].type != "type_error":
        fun_name = p[3] + "_function"
        print(p[6].str[5:] + '*', fun_name, p[4].str, file=fp)
        p[0].name = p[3]
        p[0].type = p[6].str
        item = symboltable.domain_stack[1]
        symboltable.table[item]["name"] = p[3]
        symboltable.table[item]["type"] = "function"
        symboltable.table[item]["F_type"] = False
        symboltable.table[item]["F_const"] = False
        symboltable.table[item]["declare_line"] = p.lineno(3)
        symboltable.table[item]["extend"] = [p[6].parameter_list] + p[4].parameter_list
        symboltable.table[item]["var"] = False
        symboltable.locate()
        symboltable.insert(item)
    elif hasDefined:
        my_print(str(p[2]) +  " at line" +  str(p.lineno(2)) + "has already been defined")
        p[0].type = "type_error"
    else:
        p[0].type = "type_error"

def p_subprogram_head3(p):
    '''subprogram_head : X FUNCTION ID formal_parameter ':' ID ';' '''
    #action
    p[0] = Attribute()
    index = symboltable.find_item(p[6])
    if not index:
        my_print(str(p[6]) +  " at line" +  str(p.lineno(6)) +  " is not a type")
        p[0].type = "type_error"
    else:
        if symboltable.table[index]["F_type"] == False:
            my_print("Return type error at line" +  str(p.lineno(6)) +  str(p[6]) +  " is not a type")
            p[0].type = "type_error"
        else:
            hasDefined = symboltable.find(p[3], mode=1)
            if not hasDefined and p[4].type == "type_error" :
                fun_name = p[3] + "_function";
                print(p[6], fun_name, p[4].str, file=fp)
                p[0].name = p[3]
                p[0].type = p[6]
                item = symboltable.domain_stack[1]
                symboltable.table[item]["name"] = p[3]
                symboltable.table[item]["type"] = "function"
                symboltable.table[item]["F_type"] = False
                symboltable.table[item]["F_const"] = False
                symboltable.table[item]["declare_line"] = p.lineno(3)
                symboltable.table[item]["extend"] = [p[6]] + p[4].parameter_list
                symboltable.table[item]["var_list"] = ["false"] + p[4].var_list
            elif hasDefined:
                my_print(str(p[3]) +  " at line" +  str(p.lineno(3)) +  "has already been defined")
                p[0].type = "type_error"
            else:
                p[0].type = "type_error"

def p_subprogram_head4(p):
    '''subprogram_head : X  PROCEDURE ID formal_parameter ';' '''
    #action
    p[0] = Attribute()
    hasDefined = symboltable.find(p[3], mode=1)
    if not hasDefined and p[4].type != "type_error":
        fun_name = p[3] + "_function";
        print("void", fun_name, p[4].str, file=fp)
        p[0].name = p[3]
        p[0].type = "void"
        item = symboltable.domain_stack[1]
        symboltable.table[item]["name"] = p[3]
        symboltable.table[item]["type"] = "procedure"
        symboltable.table[item]["F_type"] = False
        symboltable.table[item]["F_const"] = False
        symboltable.table[item]["declare_line"] = p.lineno(3)
        symboltable.table[item]["extend"] = p[4].parameter_list
        symboltable.table[item]["var_list"] = p[4].var_list
    elif hasDefined:
        my_print(str(p[3]) + " at line" +  str(p.lineno(3)) + "has already been defined")
        p[0].type = "type_error"
    else:
        p[0].type = "type_error"

def p_formal_parameter(p):
    '''formal_parameter : '(' parameter_lists ')'
                        | empty'''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        p[0].str = "(" + p[2].str + ")"
        p[0].parameter_list = p[2].parameter_list
        p[0].var_list = p[2].var_list
        if p[2].type == "type_error":
            p[0].type = "type_error"
    else:
        p[0].str = "()"
        p[0].parameter_list = []


def p_parameter_lists(p):
    '''parameter_lists : parameter_lists ';' parameter_list
                       | parameter_list '''
    #action
    p[0] = Attribute()
    p[0].parameter_list = []
    if len(p) == 4:
        p[0].str = p[1].str + "," + p[3].str
        p[0].parameter_list = p[1].parameter_list + p[3].parameter_list
        p[0].var_list = p[1].var_list + p[3].var_list
        if p[1].type == "type_error" and p[3].type == "type_error":
            p[0].type = "type_error"
    else:
        p[0].str = p[1].str
        p[0].parameter_list = p[1].parameter_list[:]
        p[0].var_list = p[1].var_list[:]
        p[0].type = p[1].type

def p_parameter_list1(p):
    '''parameter_list : var_parameter '''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str
    p[0].parameter_list = p[1].parameter_list
    p[0].var_list = p[1].var_list[:]
    if p[1].type == "type_error":
        p[0].type = "type_error"

def p_parameter_list2(p):
    '''parameter_list : value_parameter '''
    #action
    p[0] = Attribute()
    temp = p[1].str.split(',')
    p[0].str = ""
    for Str in temp:
        if "array" in p[1].type:
            p[0].str += p[1].type[5:] + " " + Str + "[],"
        else:
            p[0].str += p[1].type + " " + Str + ","
    p[0].str = p[0].str[:-1]
    p[0].parameter_list = p[1].parameter_list[:]
    p[0].var_list = p[1].var_list[:]
    if p[1].type == "type_error":
        p[0].type = "type_error"

def p_(p):
    '''var_parameter : VAR value_parameter'''
    #action
    p[0] = Attribute()
    p[0].str = ''
    temp = p[2].str.split(',',1)
    for Str in temp:
        if "array" in p[2].type:
            p[0].str = p[0].str + p[2].type[5:] + " " + Str + "[],"
        else:
            p[0].str = p[0].str + p[2].type + "* " + Str + ","
            symboltable.get(Str)["var"] = True
    p[0].str = p[0].str[:-1]
    p[0].parameter_list = p[2].parameter_list[:]
    p[0].var_list = p[2].var_list[:]
    length = len(p[0].var_list)
    for i in range(0,length):
        p[0].var_list[i] = "true"
    if p[2].type == "type_error":
        p[0].type = "type_error"

def p_value_parameter1(p):
    '''value_parameter : identifier_list ':' standard_type'''
    #action
    p[0] = Attribute()
    global id_cnt
    if p[1].type != "type_error":
        p[0].str = p[1].str
        p[0].type = p[3].type
        idx = symboltable.Top
        for idx in range (idx - id_cnt, idx):
            symboltable.table[idx]["type"]  = p[3].type
        i = id_cnt
        p[0].parameter_list = []
        while i != 0:
        #此处应有类型检查
            p[0].parameter_list.append(p[3].type)
            p[0].var_list.append("false")
            i -= 1
        id_cnt = 0
    else:
        p[0].type = "type_error"

def p_value_parameter2(p):
    '''value_parameter : identifier_list ':' array_type'''
    #action
    p[0] = Attribute()
    if p[1].type != "type_error" and p[3].type != "type_error":
        p[0].str = p[1].str
        p[0].type = "array" + p[3].type
        global id_cnt
        i = id_cnt
        p[0].parameter_list = []
        while i != 0:
        #此处应有类型检查
            p[0].parameter_list.append(p[3].parameter_list)
            p[0].var_list.append(p[3].var_list)
            i -= 1
        for index in range (symboltable.Top-id_cnt, symboltable.Top):
            symboltable.table[index]["type"]  = p[0].type
            symboltable.table[index]["extend"] = []
            symboltable.table[index]["extend"].append(p[3].type)
            symboltable.table[index]["extend"].append(None)
        id_cnt = 0
    else:
        p[0].type = "type_error"

def p_value_parameter3(p):
    '''value_parameter : identifier_list ':' ID '''
    #action
    p[0] = Attribute()
    index = symboltable.find_item(p[3])
    global id_cnt
    if not index:
        my_print(str(p[3]) +  " at line" +  str(p.lineno(3)) +  " is not a type")
        p[0].type = "type_error"
        id_cnt = 0
    else:
        isType = symboltable.table[index]["F_type"]
        if isType and p[1].type != "type_error":
            p[0].str = p[1].str
            p[0].type = p[3]
            i = id_cnt
            p[0].parameter_list = []
            while i != 0:
            #此处应有类型检查
                p[0].parameter_list.append(p[3])
                p[0].var_list.append("false")
                i -= 1
            idx = symboltable.Top
            for i in range (idx-id_cnt,idx):
                symboltable.table[i]["type"]  = p[3]
            id_cnt = 0
        elif not isType:
            my_print(str(p[3]) +  " at line" +  str(p.lineno(3)) +  " is not a type")
            p[0].type = "type_error"
        else:
            p[0].type = "type_error"

def p_array_type(p):
    '''array_type : ARRAY OF standard_type'''
    #action
    p[0] = Attribute()
    p[0].str = "array" + p[3].str
    p[0].type = p[3].type
    p[0].parameter_list = "array" + p[3].type

def p_compund_statement(p):
    '''compound_statement : BEGIN statement_list END U'''
    #action
    p[0] = Attribute()
    if p[2].type == "type_error":
        p[0].type = "type_error"
    p[0].str = p[2].str;

def p_U(p):
    ''' U : empty  '''
    #action
    #print(p[-2].str, end="", file=fp)

def p_statement_list(p):
    '''statement_list : statement_list ';' statement
                      | statement '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        p[0].str = p[1].str + p[3].str
        if p[1].type == "type_error" or p[3].type == "type_error":
            p[0].type = "type_error"
    else:
        p[0].str = p[1].str
        if p[1].type == "type_error":
            p[0].type = "type_error"

def p_statement1(p):
    '''statement : variable ASSIGNOP expression'''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str + "=" + p[3].str + ";\n"

    if p[1].type != "function":
        if p[1].type != p[3].type:
            if p[1].type == "float" and p[3].type == "int":
                pass
            elif p[1].type != "type_error" and p[3].type != "type_error":
                my_print(p[1].name +  " at line" +  str(p[1].lineno) +  "type does not match")
            else:
                p[0].type = "type_error"
    else:
        list = symboltable.get(p[1].name)
        if not list:
            my_print(p[1].name +  " at line" +  str(p.lineno(2)) +  "does not have an item")
            p[0].type = "type_error"
        else:
            if list["extend"][0] != p[3].type:
                if p[3].type == "int" and list["extend"][0] == "float":
                    pass
                elif p[3].type != "type_error":
                    my_print(p[1].name +  " at line" +  str(p.lineno(2)) +  "type does not match")
                else:
                    p[0].type = "type_error"

def p_statement2(p):
    '''statement : call_procedure_statement'''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str
    p[0].type = p[1].type

def p_statement3(p):
    '''statement : compound_statement'''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str
    p[0].type = p[1].type

def p_statement4(p):
    '''statement : IF expression THEN statement else_part'''
    #action
    p[0] = Attribute()
    p[0].str = "if(" + p[2].str + ")\n{\n" + p[4].str + "}" + p[5].str
    if p[2].type != "boolean":
        my_print(p[2].str +  " at line " +  str(p[2].lineno) +  " is not a boolean variable")
        p[0].type = "type_error"
    elif p[4].type == "type_error" or p[5].type == "type_error":
        p[0].type = "type_error"

def p_statement5(p):
    '''statement : CASE expression OF case_body END'''
    #action
    p[0] = Attribute()
    p[0].str = "\nswitch(" + p[2].str + ")\n{\n" + p[4].str + "}\n"
    if p[2].type == "type_error" or p[4].type == "type_error":
        p[0].type = "type_error"
    else:
        p[0].type = p[4].type

def p_statement6(p):
    '''statement : WHILE expression DO statement'''
    #action
    p[0] = Attribute()
    p[0].str = "while(" + p[2].str + ")\n{\n" + p[4].str + '}\n'
    if p[2].type != "boolean":
        my_print(p[2].str +  " at line " +  str(p[2].lineno) +  " is not a boolean variable")
        p[0].type = "type_error"
    else:
        p[0].type = p[4].type

def p_statement7(p):
    '''statement : REPEAT statement_list UNTIL expression'''
    #action
    p[0] = Attribute()
    p[0].str = "do{\n" + p[2].str + "}\nwhile(" + "!(" + p[4].str + ")" + ")\n"
    if p[4].type != "boolean":
        my_print(p[4].str +  " at line " +  str(p[4].lineno) +  " is not a boolean type")
        p[0].type = "type_error"
    else:
        p[0].type = p[2].type

def p_statement8(p):
    '''statement : FOR ID ASSIGNOP expression updown expression DO statement'''
    #action
    p[0] = Attribute()
    if p[5].str == "to":
        p[0].str = "for(" + p[2] + "=" + p[4].str + ";" + p[2] + "<=" + p[6].str + ";" + p[2] + "++)\n{\n" + p[8].str + "}\n"
    elif p[5].str == "downto":
        p[0].str = "for(" + p[2] + "=" + p[4].str + ";" + p[2] + ">=" + p[6].str + ";" + p[2] + "--)\n{\n" + p[8].str + "}\n"

    if not symboltable.find(p[2]):
        my_print(str(p[2]) +  "is not declared at line " +  str(p.lineno(2)))
        p[0].type = "type_error"
    if symboltable.get_type(p[2]) != p[4].type and p[6].type != p[4].type:
        my_print("expressions'types conflict at line " +  str(p.lineno(1)))
        p[0].type = "type_error"
    else:
        p[0].type = p[8].type

def p_statement9(p):
    '''statement : empty'''
    #action
    p[0] = Attribute()
    p[0].str = ""

def p_variable(p):
    '''variable : ID id_varparts'''
    #action
    p[0] = Attribute()
    p[0].lineno = p.lineno(1)
    if not symboltable.find(p[1]):
        my_print(str(p[1]) +  " not defined at line " +  str(p.lineno(1)))
        p[0].type = "type_error"
    else:
        if symboltable.get(p[1])["var"]:
            p[0].str = "*" + p[1] + p[2].str
        else:
            p[0].str = p[1] + p[2].str
        p[0].type = p[2].type
        p[0].name = p[1]
        p[0].parameter_list = []
        p[0].parameter_list.append((p[0].str, p[0].type))
        p[0].var_list = []
        p[0].var_list.append("False")

def p_id_varparts(p):
    '''id_varparts : id_varparts id_varpart
                   | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 3:
        p[0].dimension = p[2].dimension
        idtype = symboltable.get_real_type(p[-1])
        if idtype == None:
            my_print(str(p[-1]) +  " at line " +  str(p[2].lineno) +  " does not have an additional part")
            p[0].type = "type_error"
        elif idtype[0:5] != "array" and idtype != "record":
            my_print(str(p[-1]) +  " at line " +  str(p[2].lineno) +  " does not have an additional part")
            p[0].type = "type_error"
        else:
            p[0].sublist = p[2].sublist[:]
            p[0].str = p[1].str + p[2].str
            if p[1].type == "type_error" or p[2].type == "type_error":
                p[0].type = "type_error"
            else:
                p[0].type = p[2].type
    else:
        p[0].str = ""
        if symboltable.find(p[-1]):
            list = symboltable.get(p[-1])
            if not list:
                p[0].type = "type_error"
            else:
                p[0].type = list["type"]
                p[0].sublist = symboltable.get_extend(p[-1])
                if p[0].sublist == None:
                    p[0].sublist = []
        else:
            p[0].type = "type_error"

def p_id_varpart(p):
    '''id_varpart : '[' expression_list ']'
                  | '.' ID '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        p[0].dimension = p[-1].dimension + 1
        STR = ""
        if(len(p[-1].sublist)!=0):
            STR = p[-1].sublist[1][0]
        p[0].str = "[" + p[2].str + "-(" + str(STR) + ")" + "]"

        if("array" in p[-1].type):
            if p[2].type != "int":
                my_print("array index type error at line " + str(p.lineno(1)))
                p[0].type = "type_error"
            if len(p[-1].sublist) - 1 > 1:
                p[0].sublist = p[-1].sublist[:]
                p[0].sublist.pop(1)
                p[0].type = p[-1].type
            elif len(p[-1].sublist) - 1 == 1:
                p[0].sublist = p[-1].sublist[:]
                p[0].sublist.pop(1)
                p[0].type = p[-1].type[5:]
        else:
            p[0].type = "type_error"
        p[0].lineno = p.lineno(1)


    else:
            if symboltable.get_real_type(p[-1].type) == "record":
                record_list = symboltable.get(p[-1].type)["extend"]
                sublist = find_type(record_list,p[2])
                if not sublist:
                    my_print("record part not defined at line " + str(p.lineno(2)))
                    p[0].type = "type_error"
                else:
                    p[0].type = sublist["type"]
                    p[0].sublist = sublist["extend"]
            p[0].str = "." + p[2]
            p[0].lineno = p.lineno(2)


def p_else_part(p):
    '''else_part : ELSE statement
                 | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 3:
        p[0].str = "else\n{" + p[2].str + "\n}"
        p[0].type = p[2].type
    else:
        p[0].str = ""

#add a ';'
def p_case_body(p):
    '''case_body : branch_list ';'
                 | empty '''
    #action
    p[0] = Attribute()
    if len(p) == 3:
        p[0].str = p[1].str
        p[0].type = p[1].type
    else:
        p[0].str = ""
        p[0].type = ""

def p_branch_list(p):
    '''branch_list : branch_list ';' LZ branch
                   | LX branch '''
    #action
    p[0] = Attribute()
    if len(p) == 5:
        p[0].str = p[1].str + p[4].str
        if p[1].type == "type_error" or p[4].type == "type_error":
            p[0].type = "type_error"
    else:
        p[0].str = p[2].str
        p[0].type = p[2].type

def p_LX(p):
    ''' LX : empty '''
    p[0] = Attribute()
    p[0].type = p[-2].type

def p_LZ(p):
    ''' LZ : empty '''
    p[0] = Attribute()
    p[0].type = p[-4].type

def p_branch(p):
    '''branch : const_list ':' statement'''
    #action
    p[0] = Attribute()
    p[0].str = "case " + p[1].str + ":\n" + p[3].str + "break;\n"
    # p[0].type = p[1].type
    if p[1].type != "type_error" and p[1].type == p[-1].type:
        p[0].type = p[3].type
    else:
        my_print("types conflict in casebody, at line " +  str(p[1].lineno))
        p[0].type = "type_error"

def p_const_list(p):
    '''const_list : const_list ',' const_variable
                  | const_variable '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        p[0].str = p[1].str + "," + p[3].str
        p[0].lineno = p.lineno(2)
        if p[1].type == "type_error":
            p[0].type = "type_error"
        elif p[1].type != p[3].type:
            my_print("types conflict at line " +  str(p[3].lineno))
            p[0].type = "type_error"
        else:
            p[0].type = p[1].type
    else:
        p[0].str = p[1].str
        p[0].type = p[1].type
        p[0].lineno = p[1].lineno

def p_updown1(p):
    '''updown : TO'''
    #action
    p[0] = Attribute()
    p[0].str = "to"
    p[0].lineno = p.lineno(1)

def p_updown2(p):
    '''updown : DOWNTO '''
    #action
    p[0] = Attribute()
    p[0].str = "downto"
    p[0].lineno = p.lineno(1)

def p_call_procedure_statement1(p):
    '''call_procedure_statement : ID'''
    #action
    p[0] = Attribute()
    p[0].str = p[1] + "_function();\n"
    if not symboltable.find(p[1]):
        my_print(str(p[1]) +  " at line " +  str(p.lineno(1)) +  "is not defined")
        p[0].type = "type_error"
    elif symboltable.get_type(p[1]) != "procedure":
        my_print(str(p[1]) +  " at line  " +  str(p.lineno(1)) +  " is not a procedure")
        p[0].type = "type_error"
    elif(symboltable.get(p[1])["extend"]!=None):
        my_print(str(p[1]) +  " at line  " +  str(p.lineno(1)) +  " should have arguement " +str(symboltable.get(p[1])["extend"]))
        p[0].type = "type_error"

def p_call_procedure_statement2(p):
    '''call_procedure_statement : ID '(' expression_list ')' '''
    #action
    p[0] = Attribute()
    if(symboltable.find(p[1])):
        #重组参数列表
        str1 = p[3].str
        item_list = str1.split(",")
        # if( symboltable.get(p[1])!=None):
        Now_type = symboltable.get(p[1])["type"]
        var_list = symboltable.get(p[1])["var_list"]
        if(Now_type == "procedure"):
            for i in range(0,len(item_list)):
                if(var_list[i] == "true"):
                    if "array" not in symboltable.get_type(item_list[i]):
                        item_list[i] = "&" + item_list[i]
                    else:
                        item_list[i] = item_list[i]
            p[3].str = ""
            for i in item_list:
                p[3].str += "," + i
            p[3].str = p[3].str[1:]
        elif(Now_type == "function"):
            for i in range(0,len(item_list)):
                if(var_list[i+1] == "true"):
                    if "array" not in symboltable.get_type(item_list[i]):
                        item_list[i] = "&" + item_list[i]
                    else:
                        item_list[i] = item_list[i]
            p[3].str = ""
            for i in range(0,len(item_list)):
                p[3].str += "," + item_list[i]
            p[3].str = p[3].str[1:]
        p[0].str = p[1] + "_function(" + p[3].str + ");\n"
    if not symboltable.find(p[1]):
        my_print("function " +  str(p[1]) +  " not defined at line " +  str(p.lineno(1)))
        p[0].type = "type_error"
    elif symboltable.get_type(p[1]) == "function":
        if p[3].type != "".join(symboltable.get(p[1])['extend'][1:]):
            my_print("The parameters do not match at line " + str(p.lineno(1)))
            p[0].type = "type_error"
    elif symboltable.get_type(p[1]) == "procedure":
        if p[3].type != "".join(symboltable.get(p[1])['extend']):
            my_print("The parameters do not match at line " + str(p.lineno(1)))
            p[0].type = "type_error"
    else:
        my_print(str(p[1]) +  " at line " +  str(p.lineno(1)) +  " is not a function or procedure")
        p[0].type = "type_error"

def p_call_procedure_statement3(p):
    '''call_procedure_statement : WRITE '(' expression_list ')' '''
    #action
    p[0] = Attribute()
    format_str = ""
    id_str = ""
    for i in range(0, len(p[3].parameter_list)):
        if p[3].parameter_list[i][1] == "int":
            format_str += "%d"
        elif p[3].parameter_list[i][1] == "boolean":
            format_str += "%d"
        elif p[3].parameter_list[i][1] == "char":
            format_str += "%c"
        else:
            format_str += "%f"
        id_str += "," + p[3].parameter_list[i][0]
    p[0].str = "printf(\"" + format_str+ "\"" + id_str + ");\n"

def p_call_procedure_statement4(p):
    '''call_procedure_statement : READ '(' variables ')' '''
    #action
    format_str = ""
    id_str = ""
    for i in range(0, len(p[3].parameter_list)):
        if p[3].parameter_list[i][1] == "int":
            format_str += "%d"
        elif p[3].parameter_list[i][1] == "boolean":
            format_str += "%d"
        elif p[3].parameter_list[i][1] == "char":
            format_str += "%c"
        else:
            format_str += "%f"
        id_str += ",&" + p[3].parameter_list[i][0]
    p[0] = Attribute()
    p[0].str = "scanf(\"" + format_str + "\"" + id_str + ");\n"
    if p[3].type == "type_error":
        p[0].type = "type_error"
        my_print("read parameters type error at line " +  str(p.lineno(1)))

def p_variables(p):
    '''variables : variables ',' variable 
                 | variable '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        p[1].parameter_list.append((p[3].str, p[3].type))
        p[0].parameter_list = p[1].parameter_list[:]
        if p[1].type == "type_error" or p[3].type == "type_error":
            p[0].type = "type_error"
    else:
        p[0].parameter_list = p[1].parameter_list[:]
        p[0].type = p[1].type

def p_expression_list(p):
    '''expression_list : expression_list ',' expression
                       | expression '''
    #action
    if len(p) == 4:
        p[0] = Attribute()
        p[0].str = p[1].str + ','+ p[3].str
        #如果作为数组下标检查常量
        p[0].type = str(p[1].type) + str(p[3].type)
        p[0].parameter_list = []
        p[0].var_list = p[1].var_list + p[3].var_list
        p[1].parameter_list.append((p[3].str, p[3].type))
        for i in  p[1].parameter_list:
            p[0].parameter_list.append(i)
        if p[0].type == "type_error" or p[3].type == "type_error":
            p[0].type = "type_error"
    else:
        p[0] = Attribute()
        p[0].str = p[1].str
        p[0].type = p[1].type
        p[0].parameter_list =[]
        p[0].parameter_list.append((p[1].str,p[1].type))

def p_expression1(p):
    '''expression : simple_expression RELOP simple_expression
                  | simple_expression '''
    #action
    if len(p) == 4:
        p[0] = Attribute()
        p[0].str = p[1].str + p[2] + p[3].str
        p[0].lineno = p.lineno(2)
        if p[1].type == "type_error" or p[3].type == "type_error":
            p[0].type = "type_error"
        elif p[1].type != p[3].type:
            my_print("types don't match at line " +  str(p.lineno(2)))
            p[0].type = "type_error"
        else:
            p[0].type = "boolean"
    else:
        p[0] = Attribute()
        p[0].str = p[1].str
        p[0].type = p[1].type
        p[0].lineno = p[1].lineno
        p[0].name = p[1].name

def p_expression2(p):
    '''expression : simple_expression '=' simple_expression'''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str + "=" + p[3].str
    p[0].lineno = p.lineno(2)
    if p[1].type == "type_error" or p[3].type == "type_error":
        p[0].type = "type_error"
    elif p[1].type != p[3].type:
        my_print("types don't match at line " +  str(p.lineno(2)))
        p[0].type = "type_error"
    else:
        p[0].type = "boolean"

def p_simple_expression1(p):
    '''simple_expression : term'''
    #actionb+
    p[0] = Attribute()
    p[0].str = p[1].str
    p[0].type = p[1].type
    p[0].lineno = p[1].lineno
    p[0].name = p[1].name

def p_simple_expression2(p):
    '''simple_expression : '+' term'''
    #action
    p[0] = Attribute()
    p[0].str = "+" + p[2].str
    if p[2].type == "float" or p[2].type == "int":
        p[0].type = p[2].type
    else:
        if p[2].type != "type_error":
            my_print("Opreator '+' can not deal with type " +  p[2].type +  " at line " + str(p.lineno(1)))
        p[0].type = "type_error"
    p[0].lineno = p.lineno(1)

def p_simple_expression3(p):
    '''simple_expression : '-' term '''
    #action
    p[0] = Attribute()
    p[0].str = "-" + p[2].str
    if p[2].type == "float" or p[2].type == "int":
        p[0].type = p[2].type
    else:
        if p[2].type != "type_error":
            my_print("Opreator '-' can not deal with type " +  p[2].type +  " at line " +  str(p.lineno(1)))
        p[0].type = "type_error"
    p[0].lineno = p.lineno(1)

def p_simple_expression4(p):
    '''simple_expression : simple_expression '+' term '''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str + "+" + p[3].str
    p[0].lineno = p.lineno(2)
    if p[1].type in ["int", "float"] and p[3].type in ["int", "float"]:
        if p[1].type == "int" and p[3].type == "int":
            p[0].type = "int"
        else:
            p[0].type = "float"
    else:
        my_print("Type " +  p[1].type +  " can not add with type " +  p[3].type +  " at line " +  str(p.lineno(2)))
        p[0].type = "type_error"

def p_simple_expression5(p):
    '''simple_expression : simple_expression '-' term '''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str + "-" + p[3].str
    p[0].lineno = p.lineno(2)
    if p[1].type in ["int", "float"] and p[3].type in ["int", "float"]:
        if p[1].type == "int" and p[3].type == "int":
            p[0].type = "int"
        else:
            p[0].type = "float"
    else:
        my_print("Type " +  p[1].type +  " can not sub with type " +  p[3].type +  " at line " + str(p.lineno(2)))
        p[0].type = "type_error"

def p_simple_expression6(p):
    '''simple_expression : simple_expression OR term '''
    #action
    p[0] = Attribute()
    if p[1].type == "boolean" and p[3].type == "boolean":
        p[0].str = p[1].str + "||" + p[3].str
    else:
        p[0].str = p[1].str + "|" + p[3].str
    p[0].lineno = p.lineno(2)
    if p[1].type == p[3].type:
        if p[1].type == "int":
            p[0].type = "int"
        elif p[1].type == "boolean":
            p[0].type = "boolean"
        else:
            if p[1].type != "type_error" and p[3].type != "type_error":
                my_print("Type error at line " +  str(p.lineno(2)) +  " , the operands must be integer or boolean")
            p[0].type = "type_error"
    else:
        if p[1].type != "type_error" and p[3].type != "type_error":
            my_print("Types conflict at line " +  str(p.lineno(2)) +  " , and the operands must be integer or boolean")
        p[0].type = "type_error"

def p_term(p):
    '''term : term MULOP factor
            | factor '''
    #action
    p[0] = Attribute()
    if len(p) == 4:
        p[0].lineno = p.lineno(2)
        if p[2] == 'mod':
            STR = '%'
            if p[1].type == p[3].type:
                if p[1].type == "int":
                    p[0].type = "int"
                else:
                    if p[1].type != "type_error" and p[3].type != "type_error":
                        my_print("Type error at line " +  str(p.lineno(2)) +  ", the operands must be integer or boolean")
                    p[0].type = "type_error"
            else:
                if p[1].type != "type_error" and p[3].type != "type_error":
                    my_print("Types conflict at line " +  str(p.lineno(2)) +  ", and the operands must be integer or boolean")
                p[0].type = "type_error"
        elif p[2] == 'div':
            STR = '/'
            if p[1].type == p[3].type:
                if p[1].type == "int":
                    p[0].type = "int"
                else:
                    if p[1].type != "type_error" and p[3].type != "type_error":
                        my_print("Type error at line " +  str(p.lineno(2)) +  ", the operands must be integer")
                    p[0].type = "type_error"
            else:
                if p[1].type != "type_error" and p[3].type != "type_error":
                    my_print("Types conflict at line " +  str(p.lineno(2)) +  ", and the operands must be integer")
                p[0].type = "type_error"
        elif p[2] == 'and':
            STR = '&'
            if p[1].type == p[3].type:
                if p[1].type == "int":
                    p[0].type = "int"
                elif p[1].type == "boolean":
                    STR = "&&"
                    p[0].type = "boolean"
                else:
                    if p[1].type != "type_error" and p[3].type != "type_error":
                        my_print("Type error at line " +  str(p.lineno(2)) +  ", the operands must be integer or boolean")
                    p[0].type = "type_error"
            else:
                if p[1].type != "type_error" and p[3].type != "type_error":
                    my_print("Types conflict at line " +  str(p.lineno(2)) +  ", and the operands must be integer or boolean")
                p[0].type = "type_error"
        else:
            STR = p[2]
            if p[1].type in ["int", "float"] and p[3].type in ["int", "float"]:
                p[0].type = "float"
            else:
                p[0].type = "type_error"
                if p[1].type != "type_error" and p[3].type != "type_error":
                    my_print("Type error at line " +  str(p.lineno(2)) + ", the operands must be integer or real")
        p[0].str = p[1].str + STR + p[3].str

    else:
        p[0].str = p[1].str
        p[0].type = p[1].type
        p[0].lineno = p[1].lineno
        p[0].name = p[1].name

def p_factor1(p):
    '''factor : unsign_const_variable '''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str
    p[0].type = p[1].type
    p[0].lineno = p[1].lineno

def p_factor2(p):
    '''factor : variable '''
    #action
    p[0] = Attribute()
    p[0].str = p[1].str
    p[0].type = p[1].type
    p[0].lineno = p[1].lineno
    p[0].name = p[1].name

def p_factor3(p):
    '''factor : ID '(' expression_list ')' '''
    #action
    p[0] = Attribute()

    p[0].lineno = p.lineno(1)
    p[0].name = p[1]
    #函数调用翻译
    str1 = p[3].str
    item_list = str1.split(",")
    var_list = symboltable.get(p[1])["var_list"]
    for i in range(0,len(item_list)):
        if(var_list[i+1] == "true"):
            if "array" not in symboltable.get_type(item_list[i]):
                item_list[i] = "&" + item_list[i]
            else:
                item_list[i] = item_list[i]
    p[3].str = ""
    for i in item_list:
        p[3].str += "," + i
    p[3].str = p[3].str[1:]
    p[0].str = p[1] + "_function(" + p[3].str + ")"
    #函数调用翻译结束
    if not symboltable.find(p[1]):
        my_print("function " +  str(p[1]) +  " not defined at line " + str(p.lineno(1)))
        p[0].type = "type_error"
    elif symboltable.get_type(p[1]) != "function":
        my_print(str(p[1]) +  " at line " +  str(p.lineno(1)) +  " is not a function")
        p[0].type = "type_error"
    elif p[3].type != "".join(symboltable.get(p[1])['extend'][1:]):
        my_print("function's parameters do not match at line " +  str(p.lineno(1)))
        p[0].type = "type_error"
    else:
        p[0].type = symboltable.get(p[1])["extend"][0]

def p_factor4(p):
    '''factor : '(' expression ')' '''
    #action
    p[0] = Attribute()
    p[0].str = "(" + p[2].str + ")"
    p[0].type = p[2].type
    p[0].lineno = p[2].lineno

def p_factor5(p):
    '''factor : NOT factor '''
    #action
    p[0] = Attribute()
    p[0].str = "~" + p[2].str
    p[0].type = p[2].type
    p[0].lineno = p.lineno(1)

def p_unsigned_const_variable1(p):
    '''unsign_const_variable : NUM '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = str(p[1])
    p[0].lineno = p.lineno(1)
    p[0].type = "int"

def p_unsigned_const_variable2(p):
    '''unsign_const_variable : CHARACTER '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = "\""+p[1]+"\""
    p[0].lineno = p.lineno(1)
    p[0].type = "char"

def p_unsigned_const_variable3(p):
    '''unsign_const_variable : FLOAT '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = str(p[1])
    p[0].lineno = p.lineno(1)
    p[0].type = "float"

def p_unsigned_const_variable_11(p):
    '''unsign_const_variable : TRUE '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = str(1)
    p[0].type = "boolean"
    p[0].lineno = p.lineno(1)

def p_unsigned_const_variable_12(p):
    '''unsign_const_variable : FALSE '''
    #action
    p[0] = Attribute()
    p[0].value = p[1]
    p[0].str = str(0)
    p[0].type = "boolean"
    p[0].lineno = p.lineno(1)

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("SyntaxError!", p)

def p_program_head_error0(p):
    '''program_head : PROGRAM ID  error ')' ';' '''
    #action
    my_print(p[3])
    if p[3].type == 'ID':
        my_print("Expected a '(' in line " +  str(p.lineno(3)))

def p_program_head_error1(p):
    '''program_head : PROGRAM ID '(' error ')' ';' '''
    # action
    my_print("Expected a 'ID' in line " +  str(p.lineno(4)))

def p_program_head_error2(p):
    '''program_head : PROGRAM ID '(' identifier_list error ';' '''
    # action
    my_print("Expected a ')' in line "+ str(p.lineno(5)))

def p_program_head_error3(p):
    '''program_head : PROGRAM ID '(' identifier_list ')' error  '''
    # action
    my_print("Expected a ';' before line " +  str(p.lineno(6)))

def p_identifier_list_error(p):
    '''identifier_list : error ',' ID'''
    #action
    my_print("Expected a 'ID' in line " +  str(p.lineno(1)))

def p_const_declaration_error0(p):
    '''const_declaration : error ';' Q ID '=' const_variable'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Const variable defined error in line ", str(p.lineno(1)))

def p_const_declaration_error1(p):
    '''const_declaration : error '=' const_variable'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'ID' before '=' in line " +  str(p.lineno(1)))

def p_const_declaration_error2(p):
    '''const_declaration : const_declaration ';' Q error '=' const_variable'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'ID' before '=' in line " +  str(p.lineno(4)))

def p_const_declaration_error3(p):
    '''const_declaration : const_declaration ';' Q ID '=' error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a variable assign to ID in line " +  str(p.lineno(6)))

def p_const_declaration_error4(p):
    '''const_declaration : ID '=' error'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a variable assign to ID in line " +  str(p.lineno(3)))

def p_const_declaration_error5(p):
    '''const_declaration : const_declaration error Q ID '=' const_variable'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " + str(p.lineno(1)))

def p_type_declaration_error0(p):
    '''type_declaration : error ';' S ID '=' type'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Type definition error in line " + str(p.lineno(1)))

def p_type_declaration_error1(p):
    '''type_declaration : error '=' type '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'ID' before '=' in line " +  str(p.lineno(1)))

def p_type_declaration_error2(p):
    '''type_declaration : type_declaration ';' S error '=' type'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'ID' before '=' in line " +  str(p.lineno(4)))

def p_type_declaration_error3(p):
    '''type_declaration : type_declaration ';' S ID '=' error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'type' assign to ID before '=' in line " +  str(p.lineno(6)))

def p_type_declaration_error4(p):
    '''type_declaration : ID '=' error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'type' assign to ID before '=' in line " +  str(p.lineno(3)))

def p_type_declaration_error5(p):
    '''type_declaration : type_declaration error S ID '=' type'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(2)))

def p_type_error0(p):
    '''type : ARRAY error OF type'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Array index definition error in line " +  str(p.lineno(2)))

def p_type_error1(p):
    '''type : ARRAY '[' periods ']' OF error'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Array type definition error in line " +  str(p.lineno(6)))

def p_periods_error(p):
    '''periods : error ',' period'''
    # action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Array index definition error in line " + str(p.lineno(1)))

def p_period_error(p):
    '''period : error TOTO const_variable'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Array index definition error in line " +  str(p.lineno(1)))

def p_var_declaration_error0(p):
    '''var_declaration : var_declaration error ':' type ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Variable definition error in line " +  str(p.lineno(1)))

def p_var_declaration_error1(p):
    '''var_declaration : var_declaration identifier_list ':' error ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a correct type behind ':' in line " +  str(p.lineno(4)))

def p_var_declaration_error2(p):
    '''var_declaration : error ':' type ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Variable definition error in line " +  str(p.lineno(1)))

def p_var_declaration_error3(p):
    '''var_declaration : identifier_list ':' error ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a correct type behind ':' in line " +  str(p.lineno(3)))

def p_var_declaration_error4(p):
    '''var_declaration : var_declaration identifier_list ':' type error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(5)))

def p_var_declaration_error5(p):
    '''var_declaration : identifier_list ':' type error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(4)))

def p_subprogram_head_error0(p):
    '''subprogram_head : X FUNCTION ID '(' error ':' standard_type ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Parameter list definition error in line " +  str(p.lineno(5)))

def p_subprogram_head_error1(p):
    '''subprogram_head : X FUNCTION ID '(' error ':' ID ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Parameter list definition error in line " +  str(p.lineno(5)))

def p_subprogram_head_error2(p):
    '''subprogram_head : X FUNCTION ID formal_parameter ':' error ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Function return type error in line " +  str(p.lineno(6)))

def p_subprogram_head_error3(p):
    '''subprogram_head : X FUNCTION ID formal_parameter ':' standard_type error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(7)))

def p_subprogram_head_error4(p):
    '''subprogram_head : X FUNCTION ID formal_parameter ':' ID error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(7)))

def p_subprogram_head_error5(p):
    '''subprogram_head : X PROCEDURE ID '(' error ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Parameter list definition error in line " +  str(p.lineno(4)))

def p_subprogram_head_error6(p):
    '''subprogram_head : X PROCEDURE ID formal_parameter error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(7)))

def p_parameter_lists_error0(p):
    '''parameter_lists : error ';' parameter_list '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Parameter list definition error in line " + str(p.lineno(1)))

def p_parameter_lists_error1(p):
    '''parameter_lists : parameter_lists error parameter_list '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " +  str(p.lineno(2)))

def p_parameter_lists_error2(p):
    '''parameter_lists : parameter_lists ';' error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Parameter list definition error in line " +  str(p.lineno(3)))

def p_statement_error0(p):
    '''statement : error ASSIGNOP expression'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a variable ID before ':=' in line " + str(p.lineno(1)))

def p_statement_error1(p):
    '''statement : IF expression error statement else_part'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'then' behind 'if' in line " +  str(p.lineno(3)))

def p_statement_error3(p):
    '''statement : CASE expression OF case_body error'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected an 'end' behind 'case' in line " +  str(p.lineno(5)))

def p_statement_error4(p):
    '''statement : WHILE expression error statement'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'do' behind 'while' in line " +  str(p.lineno(3)))

def p_statement_error5(p):
    '''statement : FOR error updown expression DO statement'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected an initial varible behind 'for' in line " +  str(p.lineno(2)))

def p_statement_error6(p):
    '''statement : FOR ID ASSIGNOP expression error expression DO statement'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'to' or 'down to' behind 'for' in line "+ str(p.lineno(5)))

def p_statement_error7(p):
    '''statement : FOR ID ASSIGNOP expression updown expression error statement'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'do' behind 'for' in line"+ str(p.lineno(7)))

def p_id_varpart_errpr(p):
    '''id_varpart : error ']' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a '[' or index error in line " +  str(p.lineno(1)))

def p_branch_error(p):
    '''branch : error ':' statement'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a const variable before ':' in line " +  str(p.lineno(1)))

def p_variables_error(p):
    '''variables : error ',' variable  '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Record or Array error in line " +  str(p.lineno(1)))

def p_expression_error0(p):
    '''expression : error RELOP simple_expression '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Incorrect object before relational operation in line " +  str(p.lineno(1)))

def p_expression_error2(p):
    '''expression : error '=' simple_expression '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Incorrect object before relational operation in line " + str(p.lineno(1)))

def p_simple_expression_error0(p):
    '''simple_expression : error '+' term '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Incorrect object before relational operation in line " +  str(p.lineno(1)))

def p_simple_expression_error1(p):
    '''simple_expression : error '-' term '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Incorrect object before relational operation in line " +  str(p.lineno(1)))

def p_simple_expression_error2(p):
    '''simple_expression : error OR term '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Incorrect object before relational operation in line " +  str(p.lineno(1)))

def p_term_error(p):
    '''term : error MULOP factor '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Incorrect object before relational operation in line " +  str(p.lineno(1)))

def p_factor_error(p):
    '''factor : error ')' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a '(' or a function in line " +  str(p.lineno(1)))
def p_compund_statement_error0(p):
    '''compound_statement : error END U'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'begin' before line " + str(p.lineno(1)))

def p_compund_statement_error1(p):
    '''compound_statement : BEGIN statement_list error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a 'end' to match the 'begin' in line " + str(p.lineno(1)))

def p_compund_statement_error2(p):
    '''compound_statement : BEGIN error END U '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    # my_print("Expected a 'end' to match the 'begin' in line " + str(p.lineno(2)))

def p_program_error(p):
    '''program : program_head program_body '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a '.' at the end of program")
    my_print("completed")

def p_statement_list_error(p):
    '''statement_list : statement_list error  ';' '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " + str(p.lineno(2)))

def p_const_declarations_error(p):
    '''const_declarations : CONST const_declaration error '''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " + str(p.lineno(3)))

def p_subprogram_declarations_error(p):
    '''subprogram_declarations : subprogram_declarations subprogram_declaration error'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' before line " + str(p.lineno(3)))

def p_program_body_error(p):
    '''program_body : const_declarations type_declarations var_declarations subprogram_declarations subprogram_declaration error'''
    #action
    my_print("Cannot find main function ")
def p_variable_error(p):
    '''variable : ID id_varparts error'''
    #action
    p[0] = Attribute()
    p[0].type = "type_error"
    my_print("Expected a ';' or operation near line " + str(p.lineno(3)))



symboltable = SymbolTable()
fp = None
TextBrowser =None

def my_yacc(input_data,textBrowser):
    symboltable.rollback()
    lexer = lex.lex()
    global TextBrowser,fp
    fp = open("output.c", "w")
    TextBrowser = textBrowser
    parser = yacc.yacc()
    # result = parser.parse(input_data.lower(), debug=True)
    result = parser.parse(input_data.lower())
