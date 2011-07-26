# building anagrammer.c

anag : words.o lexicon.o main.o 
	gcc -o anag words.o lexicon.o main.o 

tests : tests.o words.o lexicon.o
	gcc -o tests tests.o words.o lexicon.o

words.o : 
	gcc -c words.c
	
tests.o :
	gcc -c tests.c
	
lexicon.o :
	gcc -c lexicon.c

main.o :
	gcc -c main.c

clean :
	rm -f *.o
	rm -f *~