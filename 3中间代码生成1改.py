import os
import sys

# 一堆全局变量
program = "   Const x=81,y=7; Var a,b,c; begin a=2*x; b=a+x+y; c=a+3b end "
syn = 2
p = 0
sum = 0
m = 0
ch = ''
token = ""
rwtab = ["begin", "if", "then", "else", "while", "do", "Const", "Var", "end"]
offset = 0
middle = []
for i in range(20):
    middle.append("")

LL = 0
nT = 0


def sult():
    global p, m, token, ch, syn, sum, offset, LL, nT, middle
    middle[LL] = middle[LL] + "t" + str(nT)
    LL += 1  # 相当于换行，写下一条语句
    middle[LL] = middle[LL] + "t" + str(nT) + " = "
    nT += 1


def isNumber(ch):
    return (ch <= '9' and ch >= '0')


def isAlpha(ch):
    return (ch >= 'a' and ch <= 'z' or ch >= 'A' and ch <= 'Z')

'''
def Print(syn):
    if syn == 11:
        print(syn, sum, sep=",")
    else:
        print(syn, token, sep=",")
'''

def printOffset():
    global p, m, token, ch, syn, sum, offset, LL, nT, middle
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
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle

    # num = 0
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
        syn = 10
        for n in range(9):
            if token == rwtab[n]:
                syn = n + 1
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
        syn = 11
        if isAlpha(ch):
            syn = -1
        return

    else:
        token = ch  # token[0]=ch
        if ch == '<':
            ch = program[p]
            p = p + 1
            if ch == '>':
                syn = 22
                token = token[:1] + ch  # token[1] = ch
            elif ch == '=':
                syn = 18
                token = token[:1] + ch  # token[1] = ch
            else:
                syn = 19
                p = p - 1
        elif ch == '>':
            ch = program[p]
            p = p + 1
            if ch == '=':
                syn = 21
                token = token[:1] + ch  # token[1] = ch
            else:
                syn = 20
                p = p - 1
        elif ch == '=':
            ch = program[p]
            p = p + 1
            if ch == '=':
                syn = 17
                token = token[:1] + ch  # token[1] = ch
            else:
                syn = 16
                p = p - 1
        elif ch == '+':
            syn = 12
        elif ch == '-':
            syn = 13
        elif ch == '*':
            syn = 14
        elif ch == '/':
            syn = 15
        elif ch == ';':
            syn = 23
        elif ch == '(':
            syn = 24
        elif ch == ')':
            syn = 25
        elif ch == ',':
            syn = 26
        elif ch == '#':
            syn = 0
        else:
            syn = -1

        return


def Const_Description():  # <常量说明>→Const <常量定义>{，<常量定义>}；
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    lexer()
    if (syn == 7):  # 7 "Const"
        printOffset()
        print("<常量说明>", token)
        offset += 4
        lexer()
        while True:
            if Const_Define() == False:
                break
            lexer()
            if syn == 23:  # 23 ;
                LL += 1
                printOffset()
                print("分号", token)
                offset -= 4
                return True
            elif syn == 26:  # 26 ,
                printOffset()
                print("逗号", token)
                lexer()
                continue
            print("常量说明错误")
    else:
        return False


def Const_Define():  # <常量定义>→<标识符>＝<无符号整数>
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    if syn == 10:
        middle[LL] = middle[LL] + token
        printOffset()
        print("<常量定义>")
        offset += 4
        printOffset()
        print(token)
        lexer()
        if syn == 16:
            middle[LL] = middle[LL] + " = "
            printOffset()
            print("等于", token)
            lexer()
            if (syn == 11):
                printOffset()
                print("无符号整数", sum)
                middle[LL] = middle[LL] + str(sum)
                offset -= 4
                LL += 1
                return True
            return False
        return False
    return False


def Var_Description():  # <变量说明>→Var <标识符>{，<标识符>}；
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    lexer()
    if syn == 8:  # "Var"
        printOffset()
        print("<变量说明>", token)
        offset += 4
        lexer()
        while True:
            if Var_Define() == False:
                break
            lexer()
            if syn == 23:  # 23 ;
                LL += 1
                printOffset()
                print("分号", token)
                offset -= 4
                return True
            elif syn == 26:  # 26 ,
                printOffset()
                print("逗号", token)
                lexer()
                continue
            print("变量声明错误")


def Var_Define():  # <标识符>→<字母>{<字母>|<数字>}
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    if syn == 10:
        middle[LL] = middle[LL] + token
        LL += 1
        printOffset()
        print("<变量定义>", token)
        return True
    else:
        return False


def Stmt():  # <语句>→<赋值语句>|<条件语句>|<当循环语句>|<复合语句>|ε
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    if syn == 10:  # 标识符<赋值语句>
        Assignment_Stmt()
        return True

    elif syn == 2:  # if<条件语句>
        Conditional_Stmts()
        return True

    elif syn == 5:  # while<当循环语句>
        While_Stmt()
        return True

    elif syn == 1:  # begin<复合语句>
        Compound_Stmts()
        return True

    else:
        return False


def Assignment_Stmt():  # <赋值语句>→<标识符>＝<表达式>;
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    middle[LL] = middle[LL] + token
    printOffset()
    print("<赋值语句>")
    offset += 4
    printOffset()
    print("<标识符>", token)
    lexer()
    if (syn == 16):  # 等于号
        printOffset()
        print("赋值语句的等于 =")
        offset += 4
        middle[LL] = middle[LL] + " = "
        lexer()
        sult()
        Expression()  # <表达式>
        LL += 1
        offset -= 8
        return True
    else:
        print("缺少等号 =")


def Conditional_Stmts():  # <条件语句>→if <条件> then <语句>| if <条件> then <语句> else<语句>
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    if syn == 2:  # "if"
        printOffset()
        print("条件语句 if")
        lexer()
        Condition()
        if syn == 3:  # "then"
            printOffset()
            print("条件语句 then")
            lexer()
            Stmt()
            if syn == 4:  # "else"
                lexer()
                Stmt()
            else:
                return True
        else:
            print("条件语句中缺少 then")
            return False
    else:
        return False


def While_Stmt():  # <当循环语句>→while <条件> do <语句>
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    printOffset()
    print("<当循环语句>", token)
    lexer()
    Condition()
    if syn == 6:  # "do"
        printOffset()
        print("while循环的do")
        lexer()
        Stmt()
        return True
    else:
        return False


def Compound_Stmts():  # <复合语句>→begin <语句>{；<语句>} end
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    printOffset()
    print("<复合语句>", token)
    offset += 4
    lexer()
    while True:
        if Stmt() == False:
            break
        if syn == 23:  # 分号;
            LL += 1
            printOffset()
            print("复合语句中的分割符", token)
            lexer()
            if syn == 9:  # 结束"end"
                break

    if syn == 9:  # 结束"end"
        offset -= 4
        printOffset()
        print("<复合语句>", token)
        lexer()
        return True

    else:
        print("<复合语句>缺乏")
        return False

    # if syn ==0:
    #     printOffset()
    #     print("<复合语句>",token)


def Expression():  # <表达式>→[＋|－]<项>{<加法运算符><项>}
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    printOffset()
    print("<表达式>")
    offset += 4
    Item()  # <项>
    while True:
        if syn == 12 or syn == 13:  # 12,+ 13,-
            printOffset()
            print("<加法运算符>", token)
            middle[LL] = middle[LL] + " " + token + " "
            sult()
            lexer()
            Item()  # <项>
        else:
            break

    offset -= 4
    return True


def Item():  # <项>→<因子>{<乘法运算符><因子>}
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    printOffset()
    print("<项>")
    offset += 4
    while True:
        if Factor() == False:
            break
        if syn == 14 or syn == 15:  # "*" "/"
            printOffset()
            print("<乘法运算符>", token)
            middle[LL] = middle[LL] + " * "
            #sult()
            lexer()
        else:
            offset -= 4
            return True

    offset -= 4
    return False


def Factor():  # <因子>→<标识符> | <无符号整数> | ‘(’<表达式>‘)’
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    printOffset()
    print("<因子>")
    offset += 4
    if syn == 10:  # <标识符>
        middle[LL] = middle[LL] + token
        printOffset()
        print("<标识符>", token)
        lexer()
        offset -= 4
        return True
    elif syn == 11:  # <无符号整数>
        printOffset()
        print("<无符号整数> ", sum)
        middle[LL] = middle[LL] + str(sum)
        lexer()
        offset -= 4
        return True
    elif syn == 24:  # ‘(’<表达式>‘)’
        printOffset()
        print("<左括号>", token)
        lexer()
        Expression()
        if syn == 25:  # ‘)’
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


def Condition():  # <条件>→<表达式><关系运算符><表达式>
    global program, p, m, token, ch, syn, sum, offset, LL, nT, middle
    printOffset()
    print("<条件>")
    Expression()
    if syn == 17 or syn == 18 or syn == 19 or syn == 20 or syn == 21 or syn == 22:  # <关系运算符>
        printOffset()
        print("<关系运算符>", token)
        lexer()
    else:
        printOffset()
        print("关系运算符错误")
        return False
    Expression()


if __name__ == "__main__":
    program = open('examplse2.txt').read()
    sys.stderr = open('err.log', 'w')
    sysoutsave = sys.stdout
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
        if syn == 0:
            print("退出 #")
            break

    sys.stdout = sysoutsave

    print("middle========================")
    for m in middle:
       print(m)
    print("middle========================")
    print("middle2========================")
    middle2=[]

    for m in middle2:
        print(m)
    print("middle2========================")
    # print("T1========================")
    # T1 = []
    # for j in middle:
    #     if j.__len__() > 1:
    #         T1.append(j)
    #
    # for m in T1:
    #     print(m)
    # print("T1========================")
    # # print(T1[4][0])
    #
    # T2 = []
    # i = 0
    # while i < len(T1):
    #     T3 = []
    #     if (T1[i][0] != 't'):
    #         T2.append(T1[i])
    #     else:
    #         T3.append(T2[-1])
    #         T2.pop(-1)
    #         j = i
    #         while True:
    #             if j >= len(T1):
    #                 break
    #             if T1[j][0] == 't':
    #                 T3.append(T1[j])
    #             else:
    #                 break
    #             j += 1
    #
    #         while len(T3):
    #             T2.append(T3[-1])
    #             T3.pop(-1)
    #
    #         i = j - 1
    #     i += 1
    # print("中间代码结果========================")
    # for m in T2:
    #     print(m)
    # print("中间代码结果========================")