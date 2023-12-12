< bool > ::= ( < not_op >) ? (" True " | " False ")
2
3 < digit > ::= [0 -9]
4
5 <int > ::= ("+" | " -") ? < digit >+
6
7 < float > ::= ("+" | " -") ? ( < digit >+ "." < digit >* | < digit >* "." < digit >+)
8
9 < number > ::= < int > | < float >
10
11 < char > ::= [a - z ] | [A - Z ]