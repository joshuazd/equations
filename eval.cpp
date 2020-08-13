#include "eval.h"

struct result {
    int ret;
    long double val;
    const char* msg;
};

int main(int argc, char** argv) {
    if(argc > 1) {
        /* parse(argv[1]); */
    } else {
        char str[] = "1+2";
        /* char s1[] = "2+1"; */
        std::string s1 = "2+1";
        const char* s[3] = {s1.c_str()};
        /* std::cout << unique(str, s, 1) << std::endl; */
        /* parse(str); */
    }

    return 0;
}

bool unique(const char* new_value, const char** old_values, const int old_length) {
    for(size_t i = 0; i < old_length; ++i) {
        const char* old = old_values[i];
        size_t len = strlen(old);
        std::multiset<char> old_set;
        for(size_t j = 0; j < len; ++j) {
            if(old[j] != ')' && old[j] != '(') {
                old_set.insert(old[j]);
            }
        }
        len = strlen(new_value);
        std::multiset<char> new_set;
        for(size_t j = 0; j < len; ++j) {
            if(new_value[j] != ')' && new_value[j] != '(') {
                new_set.insert(new_value[j]);
            }
        }

        if(new_set == old_set) {
            return false;
        }
    }
    return true;
}

result parse(char* input) {
    size_t length = strlen(input);
    std::stack<std::string> ops;
    std::deque<std::string> output;
    for(size_t i = 0; i < length; ++i) {
        char c = input[i];
        std::string s;
        s = c;
        if(c >= '0' && c <= '9') {
            output.push_back(s);
        } else if(s == "-" || s == "+" || s == "*" || s == "/" || s == "^" || s == "v" || s == "√") {
            while(ops.size() > 0
                    && (prec(ops.top()) >= prec(s))
                    && (ops.top() != "(")) {
                output.push_back(ops.top());
                ops.pop();
            }
            ops.push(s);

        } else if(s == "(") {
            ops.push(s);
        } else if(s == ")") {
            while(ops.top() != "(") {
                output.push_back(ops.top());
                ops.pop();
            }
            if(!ops.empty()) {
                ops.pop();
            }
        }
    }
    while(!ops.empty()) {
        output.push_back(ops.top());
        ops.pop();
    }
    try {
        result result;
        result.val = compute(output);
        result.ret = 0;
        result.msg = "";
        return result;
    } catch (const std::invalid_argument& e) {
        result result;
        result.val = 0;
        result.ret = 1;
        result.msg = e.what();
        return result;
    }
}

long double compute(std::deque<std::string>& output) {
    std::stack<std::string> stack;
    while(!output.empty()) {
        std::string token = output.front();
        long double tokenNum;
        if(std::stringstream(token) >> tokenNum) {
            std::cout << token << std::endl;
            stack.push(token);
        } else {
            long double rhs = std::stod(stack.top());
            stack.pop();
            long double lhs = std::stod(stack.top());
            stack.pop();
            std::cout << lhs << token << rhs << " = ";
            if(token == "+") {
                stack.push(std::to_string(lhs + rhs));
            } else if(token == "-") {
                stack.push(std::to_string(lhs - rhs));
            } else if(token == "*") {
                stack.push(std::to_string(lhs * rhs));
            } else if(token == "/") {
                stack.push(std::to_string(lhs / rhs));
            } else if(token == "^") {
                stack.push(std::to_string(pow(lhs, rhs)));
            } else if(token == "v" || token == "√") {
                if(lhs == 0) {
                    throw std::invalid_argument("zeroth root");
                }
                stack.push(std::to_string(pow(rhs, 1.0/lhs)));
                std::cout << std::to_string(pow(rhs, 1.0/lhs));
                std::cout << pow(rhs, 1.0/lhs);
            }
            std::cout << std::endl;
        }
        output.pop_front();
    }

    std::string value = stack.top();
    std::cout << value << std::endl;
    if(value == "inf") {
        throw std::invalid_argument("unable to compute result");
    } else {
        long double result;
        std::stringstream(value) >> result;
        return result;
    }
}

int prec(std::string op) {
    if(op == "-" || op == "+") {
        return 0;
    } else if(op == "*" || op == "/") {
        return 1;
    } else if(op == "^" || op == "v" || op == "√") {
        return 2;
    } else {
        return 99;
    }
}
