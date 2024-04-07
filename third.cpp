#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <regex>
using namespace std;

int main(int argc, char const *argv[])
{
    ifstream file(argv[1]);
    string bnd = std::string(R"(\b)");
    string wrd = std::string(R"(\w)");
    regex keyword(bnd + "(while)" + bnd);
    regex words("([A-Z]|[a-z])" + wrd + "+");
    smatch match;
    string token;
    string test = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec lacus eu dui scelerisque feugiat.";
    regex_search(test,match,words);
    cout << "String:range, size:" << match.size() << " matches\n";
    for (auto x : match) {
        cout << x << " , ";
    }
    file.close();
    return 0;
}