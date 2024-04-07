#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <string_view>
using namespace std;

string remove_stuff (string word, bool number) {
    if (number == true) {
        word.erase(remove_if(begin(word),end(word),[](char c) {
        return !isdigit(c) && c != '-' && c != '.';}),word.end());
        return word;
    } else {
        word.erase(remove_if(begin(word),end(word),[](char c) {
        return !isalpha(c);}),word.end());
        return word;
    }
}

int main(int argc, char const *argv[])
{
    ifstream file(argv[1]);
    char separators[] = {'(',')',';',',','{','}'};
    vector<string> operators = {"<=",">=", "!=", ">" , "<", "==", "+", "++", "-", "--", "*", "=", "/"};
    vector<string> keywords = {"while","endwhile","if"};

    while (file)
    {
        /* To-Do 
        -Remove comments
        -Add identifiers
        -Add other keywords
        */

        /* Separate line by line */
        string line;
        getline(file, line);
        string word;
        istringstream iss(line);

        while (getline(iss, word, ' ')) {
            //cout << endl << "   line: " << word << endl;
            bool has_number = false;
            bool has_alpha = false;
            bool has_na = false;

            /* Check for separators */
            for (char c : word) {
                if (isdigit(c)) {
                    has_number = true;
                } else if (isalpha(c)) {
                    has_alpha = true;
                } else {
                    has_na = true;
                }
            }

            if (has_na == true && has_alpha == false && has_number == false) {
                for (string op : operators){
                    if (word.find(op) != string::npos){
                        cout << endl << "operator   " << op << endl;
                    }
                }
                for (char sep : separators){
                    string seps(1,sep);
                    if (word.find(seps) != string::npos){
                        cout << endl << "separator   " << seps << endl;
                    }
                }
            }
            else if (has_number == true && has_na == false) {
                cout << endl << "real   " << word << endl;
            }

            else if (has_alpha == true && has_na == false) {
                bool is_keyword;
                for (string key : keywords)
                {
                    if (key.compare(word) == 0) {
                        cout << endl << "keyword:   " << key << endl;
                        is_keyword = true;
                    }
                }
                if (is_keyword == false) {
                    cout << endl << "identifier:   " << word << endl;
                }
            }

            else if (has_number == true && has_na == true) {
                bool after = false;
                string afters;
                for (char sep : separators) {
                    string seps(1,sep);
                    if(string_view(word).starts_with(seps)) {
                        cout << endl << "separator   " << sep << endl;
                    } else if (string_view(word).ends_with(seps)) {
                        after = true;
                        afters += sep;
                    }
                }
                cout << endl << "real   " << remove_stuff(word,true) << endl;
                if (after == true) {
                    cout << endl << "separator   " << afters << endl;
                }
            }

            else if (has_alpha == true && has_na == true) {
                bool after = false;
                string afters;
                for (char sep : separators) {
                    string seps(1,sep);
                    if(string_view(word).starts_with(seps)) {
                        cout << endl << "separator   " << sep << endl;
                    } else if (string_view(word).ends_with(seps)) {
                        after = true;
                        afters += sep;
                    }
                }
                cout << endl << "keyword   " << remove_stuff(word,false) << endl;
                if (after == true) {
                    cout << endl << "separator   " << afters << endl;
                }
            }
        }
    }
    file.close();
    return 0;
}