(* ============================================================================================== *) 
datatype lexresult	= SHELL of string * string * {line: word, column: word};
val error 			= fn x => TextIO.output(TextIO.stdOut,x ^ "\n")
val eof 			= fn () => SHELL("","eof",getNextTokenPos(""))
(* ============================================================================================== *)
(* ------------------------------------------------------------------ *)
(* assumes that ">" does not occur as part of a nonterminal symbol *)
fun generateSchemaTokenName( yytext ) =
    let
		fun split(x, []   ) =  raise General.Fail("an_error")
		  | split(x, y::ys) = if x=y then ys else split(x,ys);
													
		fun splitFirst(symbol,[])    = 	[] (* symbol was not in the input list *)
		  | splitFirst(symbol,x::xs) = 	if x = symbol 
						then (* found split point *)
							[]
						else (* keep looking      *)
							x::splitFirst(symbol,xs);
																		
        val s0   = explode(yytext);
        val s1   = split(#"<",s0);
        val s2   = splitFirst(#">",s1);  
    in
        implode(explode("!#schema_variable_") @ s2)        
    end;
	
(* ------------------------------------------------------------------ *)

(* ============================================================================================== *)
%%
%header (functor Target_LexFn(val getNextTokenPos : string -> {line: word, column: word}));

boolean      = "true" | "false";

posDigit     = [1-9];
digit        = [0-9];

integer      = 0 | {posDigit}{digit}*;



alpha        = [a-zA-Z];
id           = {alpha}+;

alphanumeric = [A-Za-z0-9_];
ws           = [\  \t \n];

schema_id    = "<" {alpha}{alphanumeric}* ">_" {alphanumeric}+;
comment      = "//" .* ;

%%
{ws}+        => ( getNextTokenPos(yytext); lex()  );
{comment}    => ( getNextTokenPos(yytext); lex()  );

"bool"                        => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"int"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"begin"                       => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"end"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"print"                       => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

"if"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"then"                        => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"else"                        => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"do"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"while"                       => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"for"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

"or"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"and"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"eq"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"ne"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"ge"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"le"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"gt"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"lt"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"not"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"neg"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"abs"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

"("                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
")"                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

"++"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"--"                          => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

"+"                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"-"                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"*"                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"^"                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"div"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
"mod"                         => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

"="                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );
";"                           => ( SHELL(yytext      , yytext,     getNextTokenPos(yytext))    );

{boolean}                     => ( SHELL("boolean"   , yytext,     getNextTokenPos(yytext))    );
{integer}                     => ( SHELL("integer"   , yytext,     getNextTokenPos(yytext))    );
{id}                          => ( SHELL("id"        , yytext,     getNextTokenPos(yytext))    );

{schema_id}                   => ( SHELL(generateSchemaTokenName(yytext), yytext, getNextTokenPos(yytext))    );
"[:]"                         => ( SHELL("" , yytext, getNextTokenPos(yytext))    );

 .                            => ( error("ignored an unprintable character: " ^ yytext); getNextTokenPos(yytext); lex()  );
