structure Tokens = Tokens

type pos = int
type svalue = Tokens.svaslue
type ('a,'b) token = ('a,'b) Tokens.token
type lexresult= (svalue,pos) token

val pos = ref 0
fun teste() = print "oi";
fun error (e,l : int,_) = TextIO.output (TextIO.stdOut, String.concat[
	"line ", (Int.toString l), ": ", e, "\n"
      ])
%%
%header (functor KindiLexFun(structure Tokens: Kindi_TOKENS));
char=[A-Za-z];
digit=[0-9];
op =[-+*/%><=^];
white_space = [\ \n\t];
%%
\n              => (pos := (!pos) + 1; lex());
{white_space}+  => (lex());
{digit}+        => (Tokens.NUM (valOf (Int.fromString yytext), !pos, !pos));

"int"   => (Tokens.TYPE(yytext,!pos,!pos));