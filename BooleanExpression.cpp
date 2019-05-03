#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <math.h> 

using namespace std;

//Stampa a video del'help menu
void Help_print(){
	cout << endl << "############## HELP ##############" <<endl
	<< "Operatore AND : &&" << endl
	<< "Operatore OR: ||" << endl
	<< "Operatore NOT: !" << endl
	<< "Operatore Implicazione: =>" << endl
	<< "Operatore doppia Implicazione: <=>" << endl
	<< "Inserisci l'espressione:"<<endl
	<< "- come parametro (tra virgolette);"<<endl
	<< "- avviando il programma."<<endl
	<< "##################################"<<endl
	<<endl;
}
//Funzione per interrompere il programma con un messaggio a video
void trowError(string s){
	cout << endl << "ERRORE INDIVIDUATO!";
	cout << endl << s<<endl<<endl;
	system("pause");
	exit(0);
}
//Funzione che restituisce true se trova la stringa in un vector di stinghe
bool findInVector(vector<string> v,string s){
	for(int i=0;i<v.size();i++){
		if (v[i] == s){
			return true;
		}
	}
	return false;
}
//Restituisce la posizione di una stringa in un vettore di stringhe
int findPosInVector(vector<string> v,string s){
	for(int i=0;i<v.size();i++){
		if (v[i] == s){
			return i;
		}
	}
	return -1;
}
//Restituisce vero se è una lettera o un numero
bool isANumberOrLetter(char c){
	int asciiCode = int(c);
	return (bool)((asciiCode >= 65 && asciiCode<=90) || (asciiCode>= 97 && asciiCode<= 122) || (asciiCode >=48 && asciiCode <= 57));
}
//Funzione che crea il vettore dei simboli data un'espressione
vector<string> findSym(string expression){
	bool lastisletter = false;
	string sym="";
	vector<string> v;
	for(int i =0;i< expression.length();i++){
		if(isANumberOrLetter(expression[i])){
			if (lastisletter){
				sym += expression[i];
			}else{
				lastisletter = true;
				sym += expression[i];
			}
		}else{
			lastisletter = false;
			if (sym != ""){
				if(!findInVector(v,sym)){
					v.push_back(sym);
				}
				sym = "";
			}
		}
	}
	if (sym != ""){
		if(!findInVector(v,sym)){
			v.push_back(sym);
		}
		sym = "";
	}
	return v;
}
//Comando che da la combinazione secondo un id
void combinationGive(int IdCombination,int Numbers,bool* values){
	int BitTester = pow(2,Numbers-1);
	for(int i = 0;i<Numbers;i++){
		values[i] = (IdCombination & BitTester) != 0;
		BitTester /= 2;
	}
}
//Comando che restituisce il comando dell'and
bool Logic_AND(bool a, bool b){
	if (a && b){
		return true;
	}else{
		return false;
	}
}
//Comando che restituisce il risultato dell'or
bool Logic_OR(bool a, bool b){
	if(a){
		return true;
	}
	if(b){
		return true;
	}
	return false;
}
//Comando che restituisce il risultato dell'implica
bool Logic_IMP(bool a, bool b){
	if (a == true && b == false){
		return false;
	}else{
		return true;
	}
}
//Comando che restituisce il risultato della doppia implicazione
bool Logic_DIMP(bool a, bool b){
	return a == b;
}
//Comando che restituisce il risultato del not (da char)
void charMap_NOT(char &c){
	switch(c){
		case 't':
			c='f';
			break;
		case 'f':
			c='t';
			break;
		default:
			trowError("NOT _ Null Value");
		break;
	}
}
//Trasforma la mappa del valore char in bool
bool charMaptoBool(char &c){
	switch(c){
		case 't':
			c='n';
			return true;
			break;
		case 'f':
			c='n';
			return false;
			break;
		default:
			trowError("Null Value");
		break;
	}
}
//Trasforma il valore bool nella mappa del valore char
char BooltoCharMap(bool b){
	if(b){
		return 't';
	}else{
		return 'f';
	}
}
//Comando che permette di cambiare la fase dell'algoritmo
void goNextFase(char &mode,char &val1,char &val2,char &oper,bool &NOT){
	if (mode == '2'){
		if(NOT){
			charMap_NOT(val2);
			NOT = false;
		}
		mode = 'o';
		switch(oper){
			case '&':
				val1 = BooltoCharMap(Logic_AND(charMaptoBool(val1),charMaptoBool(val2)));
			break;
			case '|':
				val1 = BooltoCharMap(Logic_OR(charMaptoBool(val1),charMaptoBool(val2)));
			break;
			case '<':
				val1 = BooltoCharMap(Logic_DIMP(charMaptoBool(val1),charMaptoBool(val2)));
			break;
			case '=':
				val1 = BooltoCharMap(Logic_IMP(charMaptoBool(val1),charMaptoBool(val2)));
			break;
			default:
				trowError("Errore con l'operatore (Errore interno)");
			break;
		}
		val2 = 'n';
		oper = 'n';
	}else if(mode == '1'){
		if(NOT){
			charMap_NOT(val1);
			NOT = false;
		}
		mode = 'o';
	}else if(mode == 'o'){
		mode = '2';
	}
}
//Funzione che calcola il valore dell'espressione secondo una tabella dei simboli con valori assegnati
bool CalculateExpression(vector<string> signTable,bool* signValues,string ex){
	char here;
	char val1= 'n' ,val2 = 'n'; // n = null, t = vero, f = falso
	char mode = '1'; // 1 = val1,o = operator, 2 = val2
	int priority = 0; // vero se si sta catturando una parentesi 
	string pr_tmp = "",sym_tmp = "";
	bool tmp_value = false, lastIsLetter = false, NotReq = false;
	char oper = 'n';//n = null,& = and; | = or; < = doppio impl; "=" = impl
	ex +="@";
	//Ciclo per esaminare la stringa espressione logica
	for(int pos = 0;pos < ex.length();pos++){
		here = ex[pos];
		//Gestisci le parentesi
		if (priority>0){
			switch(here){
				case '(':
					priority++;
					break;
				case ')':
					priority--;
					break;
			}
			//Se la parentesi e stata trovata calcola il valore (Ricursione)
			if (priority == 0){
				tmp_value=CalculateExpression(signTable,signValues,pr_tmp);
				switch(mode){
					case '1':
						val1 = BooltoCharMap(tmp_value);
						break;
					
					case 'o':
						trowError("2 valori insieme senza un operatore...");
						break;
					
					case '2':
						val2 = BooltoCharMap(tmp_value);
						break;
					
				}
				pr_tmp="";
				goNextFase(mode,val1,val2,oper,NotReq);
			}else{
				pr_tmp+=here;
			}
			//Applica il not sul valore successivo
		}else if(here == '!'){
			if(mode == 'o'){
				trowError("Impossibile negare un operatore...");
			}else{
				NotReq = true;
			}
		}else{
			//Identificazione del simbolo e assegnazione del valore secondo la tabella valori
			if (mode == '1' || mode == '2'){
				//gestione del valore in base al char trovato
				if(isANumberOrLetter(here)){
					if(lastIsLetter){
						sym_tmp+=here;
					}else{
						lastIsLetter = true;
						sym_tmp = "";
						sym_tmp += here;
					}
				}else if(here == '('){
					priority++;
				}else if ((here == '&'|| here == '|' || here == '=' || here == '<') && !lastIsLetter){
					trowError("Operatori posizionati non correttamente!");
				}else if(here != ' '){
					lastIsLetter = false;
					tmp_value = signValues[findPosInVector(signTable,sym_tmp)];
					if (mode == '1'){
						val1 = BooltoCharMap(tmp_value);
					}else{
						val2 = BooltoCharMap(tmp_value);
					}
					goNextFase(mode,val1,val2,oper,NotReq);
					pos--;
				}
				//ricerca del operatore
			}else if (mode == 'o'){
				if(isANumberOrLetter(here) || here == '(' || here == ')'){
					trowError("Operatore non trovato!");
				}else{
					//filtro degli operatori
					if(here == '&'){
						pos++;
						try{
							tmp_value = (ex[pos] == '&');
						}catch(exception e){
							cout <<"EXCEPT";
							tmp_value = false;
						}
						if(tmp_value){
							oper = '&';
							goNextFase(mode,val1,val2,oper,NotReq);
						}else{
							trowError("Simbolo valido non trovato (Individuato solo un \"&\")");
						}
					}else if(here == '|'){
						pos++;
						try{
							tmp_value = (ex[pos] == '|');
						}catch(exception e){
							tmp_value = false;
						}
						if(tmp_value){
							oper = '|';
							goNextFase(mode,val1,val2,oper,NotReq);
						}else{
							trowError("Simbolo valido non trovato (Individuato solo un \"|\")");
						}
					}else if(here == '<'){
						pos++;
						try{
							tmp_value = (ex[pos] == '=');
							pos++;
							tmp_value = (ex[pos] == '>' && tmp_value);
						}catch(exception e){
							tmp_value = false;
						}
						if(tmp_value){
							oper = '<';
							goNextFase(mode,val1,val2,oper,NotReq);
						}else{
							trowError("Simbolo valido non trovato (Individuato solo un \"<\")");
						}

					}else if(here == '='){
						pos++;
						try{
							tmp_value = (ex[pos] == '>');
						}catch(exception e){
							tmp_value = false;
						}
						if(tmp_value){
							oper = '=';
							goNextFase(mode,val1,val2,oper,NotReq);
						}else{
							trowError("Simbolo valido non trovato (Individuato solo un \"=\")");
						}
					}
				}
			}else{
				trowError("Mode non valida (Errore interno del codice)");
			}
		}	

	}
	//Output e filtro di falsi risultati
	if (priority != 0){
		trowError("Parentesi scorrettamente posizionate");
	}else if(mode == '2'){
		trowError("Simbolo successivo non trovato!");
	}else if (val2 == 'n' && val1 != 'n'){
		return charMaptoBool(val1);
	}else{
		trowError("Errore non identificato...!");
	}
}

int main(int argn, char ** argv){

	string expression = "";
	//Acquisizione in input o da parametro o da console
	if (argn>1){
		string tmp;
		for(int i=1;i<argn;i++){
			tmp= argv[i];
			if(tmp == "-h" || tmp == "--help"){
				Help_print();
				return 0;
			}
			expression += tmp;
			expression += " ";
		}
	}else{
		cout << "Inserire Espressione logica:";
		getline(cin,expression);
	}
	//Ricerca dei simboli nell'espressione
	vector<string> sym = findSym(expression);
	sort(sym.begin(),sym.end());

	int nSym = sym.size();
	int nComb = pow(2,nSym);
	if (nSym == 0){
		trowError("Nessun simbolo trovato");
	}

	bool res;
	bool values[nSym];
	cout << endl 
		 << "---------------------------------------"<<endl
		 << "---        Tabella di verit         ---"<<endl
		 << "---------------------------------------"<<endl<<endl
		 << "Espressione: " << expression << endl << endl;
		 //Creazione delle statisciche e soluzione di queste con stampa a video
	for(int i=0;i<nComb;i++){
		combinationGive(i,nSym,values);
		res = CalculateExpression(sym,values,expression);
		for (int i=0;i<nSym;i++){
			cout << "*" << sym[i] << ":  " << values[i] << " |   ";
		}
		cout << " ## Risultato: "<<res<<endl;
	}
	system("pause");
}
