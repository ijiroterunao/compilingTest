# compilingTest
pl0的词法分析，语法分析，中间代码生成   

大三上编译原理实验，一开始我没打算写，因为我很菜，不知道怎么写，老师的要求也没搞懂。准备拿别人的代码去验收，第一天老师比较松，第二天突然变得严格起来。我们几个同学很纳闷，后来才知道，原来有人拿了别人的代码去找老师验收，明明没搞懂还软磨硬泡，折腾了老师40多分钟，老师很生气。叫我们剩下的人自己写，不要复制。没办法，只好看了别人的c代码写了个python版本的。   

examplse.txt和examplse2.txt是老师发的测试代码，要求能检错，其中examplse.txt用于词法分析和语法分析。examplse2.txt用于中间代码生成  

examplse.txt
“3中间代码生成1”是我看了别人验收的c语言代码写的，错的，他把*+-都当作一样的，没有优先级，老师第一天验收的时候没仔细看

“3中间代码生成2改改_ok” 才是勉强算对的
还有三个代码文件没什么用，自己写的时候的错误
```
Const x=8,y=7;
Var a,b,c;
begin
   a=b+x;
    
    if a>0
       then
       begin
         c=y -1;
         a=a+2;
       end
    else
       begin
         c=a+y;
       end
   
    while a>0
      do  a=a-1;
end
#
```

examplse2.txt

```
Const x=8,y=7;
Var a,b,c;
begin
   a=2*x;
   b=a+x+y;
   c=a+3*b;
end
#
```
