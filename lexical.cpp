#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <string>
#include <map>
using namespace std;

int main(int argc, char const *argv[])
{
    ifstream file(argv[1]);
    vector<string> words;
    char separators[] = {'(',')',';',','};
    vector<string> operators = {"<=",">="};
    map<string, string> output;
    while (file)
    {
        string line;
        getline(file, line);
        string word;
        istringstream iss(line);
        while (getline(iss, word, ' '))
        {
            for (char sep : separators)
                {string seps(1,sep);if (word.find(seps) != string::npos) {output.insert(make_pair("separator",seps));}}
            for (string op : operators)
                {if (word.find(op) != string::npos) {output.insert(make_pair("operator",op));}}
        }
    }
    for (const auto& p : output) {
        cout << endl << p.first << "  " << p.second << endl;
    }
    file.close();
    return 0;
}

//char separators[] = {'(',')',';',','};
//for (char op : separators) {string ops(1,op);if (word.find(ops) != string::npos) {words.push_back(ops);}}