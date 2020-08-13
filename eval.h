#include <deque>
#include <stack>
#include <set>
#include <iostream>
#include <sstream>
#include <string.h>
#include <cmath>

long double compute(std::deque<std::string>&);
int prec(std::string);
struct result;
extern "C" {
    result parse(char*);
    bool unique(const char*, const char**, const int);
}
