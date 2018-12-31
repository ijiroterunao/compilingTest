# -*- coding: UTF-8 -*-
import os
import sys

program = "   Const x=81,y=7; Var a,b,c; begin a=2*x; b=a+x+y; c=a+3b end "
syntax = 2
p = 0
sum = 0
m = 0
ch = ''
token = ""
rwtab = ["begin", "if", "then", "else", "while", "do", "Const", "Var", "end"]
offset = 0


def isNumber(ch):
    return (ch <= '9' and ch >= '0')


def isAlpha(ch):
    return (ch >= 'a' and ch <= 'z' or ch >= 'A' and ch <= 'Z')


def Print(syntax):
    if syntax == 11:
        print(syntax, sum, sep=",")
    else:
        print(syntax, token, sep=",")


def printOffset():
    for i in range(offset):
        sys.stdout.write(' ')


'''
-1 error
0 #
1 "begin"
2 "if"
3 "then"
4 "else"
5 "while"
6 "do"
7 "Const"
8 "Var"
9 "end"
10 标识符
11 数字
12 +
13 -
14 *
15 /
16 =
17 ==
18 <=
19 <
20 >
21 >=
22 <>
23 ;
24 (
25 )
26 ,

'''


def lexer():
    global p, m, token, ch, syntax, sum, offset

    num = 0
    token = ''
    m = 0

    ch = program[p]
    p = p + 1

    while True:
        if (ch == ' ' or ch == '\n' or ch == '\t'):
            ch = program[p]
            p = p + 1
        else:
            break

    if isAlpha(ch):
        while True:
            token = token[:m] + ch  # token[m] = ch
            m = m + 1
            ch = program[p]
            p = p + 1
            if (isAlpha(ch) == False and isNumber(ch) == False):
                break

        p = p - 1
        syntax = 10
        for n in range(9):
            if token == rwtab[n]:
                syntax = n + 1
                break

        return

    elif isNumber(ch):
        sum = 0
        while True:
            if isNumber(ch) == False:
                break
            sum = sum * 10 + int(ch)
            ch = program[p]
            p = p + 1

        p = p - 1
        syntax = 11
        if isAlpha(ch):
            syntax = -1
        return

    else:
        token = ch  # token[0]=ch
        if ch == '<':
            ch = program[p]
            p = p + 1
            if ch == '>':
                syntax = 22
                token = token[:1] + ch  # token[1] = ch
            elif ch == '=':
                syntax = 18
                token = token[:1] + ch  # token[1] = ch
            else:
                syntax = 19
                p = p - 1
        elif ch == '>':
            ch = program[p]
            p = p + 1
            if ch == '=':
                syntax = 21
                token = token[:1] + ch  # token[1] = ch
            else:
                syntax = 20
                p = p - 1
        elif ch == '=':
            ch = program[p]
            p = p + 1
            if ch == '=':
                syntax = 17
                token = token[:1] + ch  # token[1] = ch
            else:
                syntax = 16
                p = p - 1
        elif ch == '+':
            syntax = 12
        elif ch == '-':
            syntax = 13
        elif ch == '*':
            syntax = 14
        elif ch == '/':
            syntax = 15
        elif ch == ';':
            syntax = 23
        elif ch == '(':
            syntax = 24
        elif ch == ')':
            syntax = 25
        elif ch == ',':
            syntax = 26
        elif ch == '#':
            syntax = 0
        else:
            syntax = -1

        return


def Const_Description():  # <常量说明>→Const <常量定义>{，<常量定义>}；
    global p, m, token, ch, syntax, sum, offset
    lexer()
    if (syntax == 7):  # 7 "Const"
        printOffset()
        print("<常量说明>", token)
        offset += 4
        lexer()
        while True:
            if Const_Define() == False:
                break
            lexer()
            if syntax == 23:  # 23 ;
                printOffset()
                print("分号", token)
                offset -= 4
                return True
            elif syntax == 26:  # 26 ,
                printOffset()
                print("逗号", token)
                lexer()
                continue
            print("常量说明错误")
    else:
        return False


def Const_Define():  # <常量定义>→<标识符>＝<无符号整数>
    global p, m, token, ch, syntax, sum, offset
    if syntax == 10:
        printOffset()
        print("<常量定义>")
        offset += 4
        printOffset()
        print(token)
        lexer()
        if syntax == 16:
            printOffset()
            print("等于", token)
            lexer()
            if (syntax == 11):
                printOffset()
                print("无符号整数", sum)
                offset -= 4
                return True
            return False
        return False
    return False


def Var_Description():  # <变量说明>→Var <标识符>{，<标识符>}；
    global p, m, token, ch, syntax, sum, offset
    lexer()
    if syntax == 8:  # "Var"
        printOffset()
        print("<变量说明>", token)
        offset += 4
        lexer()
        while True:
            if Var_Define() == False:
                break
            lexer()
            if syntax == 23:  # 23 ;
                printOffset()
                print("分号", token)
                offset -= 4
                return True
            elif syntax == 26:  # 26 ,
                printOffset()
                print("逗号", token)
                lexer()
                continue
            print("变量声明错误")


def Var_Define():  # <标识符>→<字母>{<字母>|<数字>}
    global syntax
    if syntax == 10:
        printOffset()
        print("<变量定义>", token)
        return True
    else:
        return False


def Stmt():  # <语句>→<赋值语句>|<条件语句>|<当循环语句>|<复合语句>|ε
    global syntax
    if syntax == 10:  # 标识符<赋值语句>
        Assignment_Stmt()
        return True

    elif syntax == 2:  # if<条件语句>
        Conditional_Stmts()
        return True

    elif syntax == 5:  # while<当循环语句>
        While_Stmt()
        return True

    elif syntax == 1:  # begin<复合语句>
        Compound_Stmts()
        return True

    else:
        return False


def Assignment_Stmt():  # <赋值语句>→<标识符>＝<表达式>;
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<赋值语句>")
    offset += 4
    printOffset()
    print("<标识符>", token)
    lexer()
    if (syntax == 16):  # 等于号
        printOffset()
        print("赋值语句的等于 =")
        offset += 4
        lexer()
        Expression()  # <表达式>
        offset -= 8
        return True
    else:
        print("缺少等号 =")


def Conditional_Stmts():#<条件语句>→if <条件> then <语句>| if <条件> then <语句> else<语句>
    global p, m, token, ch, syntax, sum, offset
    if syntax == 2 : #"if"
        printOffset()
        print("条件语句 if")
        lexer()
        Condition()
        if syntax ==3: #"then"
            printOffset()
            print("条件语句 then")
            lexer()
            Stmt()
            if syntax ==4 : #"else"
                lexer()
                Stmt()
            else:
                return True
        else:
            print("条件语句中缺少 then")
            return False
    else:
        return False


def While_Stmt(): #<当循环语句>→while <条件> do <语句>
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<当循环语句>",token)
    lexer()
    Condition()
    if syntax ==6: #"do"
        printOffset()
        print("while循环的do")
        lexer()
        Stmt()
        return True
    else:
        return False

def Compound_Stmts():#<复合语句>→begin <语句>{；<语句>} end
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<复合语句>",token)
    offset +=4
    lexer()
    while True:
        if Stmt()==False:
            break
        if syntax == 23:    #  分号;
            printOffset()
            print("复合语句中的分割符",token)
            lexer()
            if syntax ==9:  # 结束"end"
                break

    if syntax ==9:# 结束"end"
        offset -=4
        printOffset()
        print("<复合语句>",token)
        lexer()
        return True

    else:
        print("<复合语句>缺乏")
        return False

    # if syntax ==0:
    #     printOffset()
    #     print("<复合语句>",token)






def Expression():  # <表达式>→[＋|－]<项>{<加法运算符><项>}
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<表达式>")
    offset += 4
    Item()# <项>
    while True:
        if syntax == 12 or syntax == 13:  # 12,+ 13,-
            printOffset()
            print("<加法运算符>", token)
            lexer()
            Item()  # <项>
        else:
            break

    offset -= 4
    return True


def Item():  # <项>→<因子>{<乘法运算符><因子>}
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<项>")
    offset += 4
    while True:
        if Factor() == False:
            break
        if syntax == 14 or syntax == 15:  # "*" "/"
            printOffset()
            print("<乘法运算符>", token)
            lexer()
        else:
            offset -= 4
            return True

    offset -= 4
    return False


def Factor():  # <因子>→<标识符> | <无符号整数> | ‘(’<表达式>‘)’
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<因子>")
    offset += 4
    if syntax == 10:  # <标识符>
        printOffset()
        print("<标识符>", token)
        lexer()
        offset -= 4
        return True
    elif syntax == 11:  # <无符号整数>
        printOffset()
        print("<无符号整数> ", sum)
        lexer()
        offset -= 4
        return True
    elif syntax == 24:  # ‘(’<表达式>‘)’
        printOffset()
        print("<左括号>", token)
        lexer()
        Expression()
        if syntax == 25:  # ‘)’
            printOffset()
            print("<右括号> ", token)
            lexer()
            offset -= 4
            return True
        else:
            print("没有找到 <右括号>，error")
            offset -= 4
            return False

    else:
        print("没有找到 <因子>，error")
        offset -= 4
        return False
    # offset -=4
    # return False

def Condition(): #<条件>→<表达式><关系运算符><表达式>
    global p, m, token, ch, syntax, sum, offset
    printOffset()
    print("<条件>")
    Expression()
    if syntax==17 or syntax==18 or syntax==19 or syntax==20 or syntax==21 or syntax==22: #<关系运算符>
        printOffset()
        print("<关系运算符>",token)
        lexer()
    else:
        printOffset()
        print("关系运算符错误")
        return False
    Expression()


if __name__ == "__main__":
    program = open('examplse.txt').read()
    sys.stderr = open('err.log', 'w')
    sys.stdout = open('file_out.txt', 'w')
    print("源程序：")
    print(program)
    p = 0
    currentLine = 1
    print("开始语法分析：")
    offset += 4
    # <程序>→[<常量说明>][<变量说明>]<语句>
    Const_Description()
    Var_Description()
    while True:
        lexer()
        Stmt()
        if syntax == 0:
            print("#语法分析结束")
            break
