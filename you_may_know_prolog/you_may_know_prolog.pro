domains
    	name, city = symbol
    	age = integer
    	network = symbol*
	
predicates
	nondeterm person(name, age, city, network)
    	nondeterm friend(name, name)
    	nondeterm in_network(symbol, network)
    	nondeterm same_network(network, network)
    	nondeterm connected(name, name)
   	nondeterm relation(name, name)   
   	nondeterm you_may_know(name, name)
    	nondeterm suggestion(name)
    	nondeterm find_people()
    	
database
	suggestion_list(name)
	
clauses
    	person("Ali", 35, "Zonguldak", ["IEEE"]).
    	person("Veli", 26, "Ankara", ["Gazi", "Ankara"]).
    	person("Aylin", 24, "Zonguldak", ["IEEE", "Karaelmas"]).
    	person("Ayse", 22, "Mersin", ["Turkey"]).
           
    	friend("Ali", "Veli").
    	friend("Veli", "Ayse").
   
	in_network(X,[X|_]).
	in_network(X,[_|K]):-
		in_network(X,K).
	
	same_network([],_):- fail.
	same_network([H|T], Y):-
		same_network(T, Y);
		in_network(H, Y).
		
    	connected(Who, With) :- friend(Who, With); friend(With, Who).

    	relation(Who, With):-
       		connected(Who, Mutual)  , connected(Mutual, With);			% friend of friend
       		person(Who,WhoAge,_,_)  , person(With,WithAge,_,_), 
				WhoAge < WithAge+5 , WhoAge >  WithAge-5;		% +5, -5 age
        	person(Who,_,City,_)    , person(With,_,City,_);		  	% same city
		person(Who,_,_,A)	, person(With,_,_,B), same_network(A, B). 	% same network

    	you_may_know(Who, With) :-
       		relation(Who, With),   
       		With <> Who,
       		not(connected(Who, With)),
       		not(suggestion_list(With)).
	
    	suggestion(Who):-
       		you_may_know(Who, With),
       		assertz(suggestion_list(With)),
       		write(Who, " may be know ", With),nl,nl.
        	
    	find_people():-
    		write("Write a name to find people: "), readln(Who), nl,suggestion(Who), fail.  		

goal
	not(find_people).