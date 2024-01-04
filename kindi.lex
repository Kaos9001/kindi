datatype lexresult= DIV | EOF | EOS | ID of string | LPAREN |
                     NUM of int | PLUS | PRINT | RPAREN | SUB | TIMES 

val linenum = ref 1
val error = fn x => output(std_out,x ^ "\n")
val eof = fn () => EOF
%%
%structure KindiLex

digit=[0-9];
int=(PLUS|SUB)? {digit}+;
floar=(PLUS|SUB)? ({digit}+ "." {digit}* | {digit}* "." {digit}+);
number=int|float;
char=[a-zA-Z];

ws = [\ \t];
%%
\n       => (inc linenum; lex());
{ws}+    => (lex());
"/"      => (DIV);
";"      => (EOS);
"("      => (LPAREN);
{digit}+ => (NUM (revfold (fn(a,r)=>ord(a)-ord("0")+10*r) (explode yytext) 0));
")"      => (RPAREN);
"+"      => (PLUS);
"-"      => (SUB);
"*"      => (TIMES);
.        => (error ("calc: ignoring bad character "^yytext); lex());