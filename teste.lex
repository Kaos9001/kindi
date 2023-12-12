< bool > ::= ( < not_op >) ? (" True " | " False ")
< digit > ::= [0 -9]
<int > ::= ("+" | " -") ? < digit >+
< float > ::= ("+" | " -") ? ( < digit >+ "." < digit >* | < digit >* "." < digit >+)
< number > ::= < int > | < float >
< char > ::= [a - z ] | [A - Z ]