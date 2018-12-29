import os
import sys
program = "   Const x=81,y=7; Var a,b,c; begin a=2*x; b=a+x+y; c=a+3b end "
syn = 2
p = 0
sum = 0
m = 0
ch = ''
token = ""
rwtab = ["begin", "if", "then", "else", "while", "do", "Const", "Var", "end"]



def isNumber(ch):
    return (ch <= '9' and ch >= '0')


def isAlpha(ch):
    return (ch >= 'a' and ch <= 'z' or ch >= 'A' and ch <= 'Z')


def Print(syn):
    if syn == 11:
        print(syn, sum, sep=",")
    else:
        print(syn, token, sep=",")


def lexer():
    global p, m,token,ch,syn,sum,program

    num = 0
    token =''
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
            token=token[:m]+ch  #token[m] = ch
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
        token = ch  #token[0]=ch
        if ch =='<':
            ch=program[p]
            p=p+1
            if ch=='>':
                syn = 22
                token=token[:1]+ch  #token[1] = ch
            elif ch =='=':
                syn=18
                token=token[:1]+ch  #token[1] = ch
            else:
                syn=19
                p=p-1
        elif ch =='>':
            ch=program[p]
            p=p+1
            if ch =='=':
                syn=21
                token = token[:1] + ch  # token[1] = ch
            else:
                syn=20
                p=p-1
        elif ch =='=':
            ch=program[p]
            p=p+1
            if ch =='=':
                syn=17
                token = token[:1] + ch  # token[1] = ch
            else:
                syn=16
                p=p-1
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



if __name__ == "__main__":
    program = open('examplse2.txt').read()
    sys.stderr = open('err.log', 'w')
    sys.stdout = open('file_out.txt', 'w')
    print(program)
    p=0
    while True:
        lexer()

        if syn == -1:
            print("failed " + token)
            break
        elif syn == 0:
            print("success")
            break
        else:
            Print(syn)

