#include <iostream>

extern "C" void greet() {
    std::cout << "Hello from C++ module!" << std::endl;
}
