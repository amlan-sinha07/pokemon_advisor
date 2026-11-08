#include <iostream>
#include <string>
#include <cmath>
using namespace std;

float calculate_damage(int power,int atk,
                    int def_stat,float effectiveness, float stab){
    float float_power= static_cast<float>(power);

    float base=((2.0f*50 / 5 +2 )*power*atk/(float)def_stat)/50+2;
    cout<< "C++ Raw Base Damge: "<<base<<endl;
    float final_damage =base *stab *effectiveness;
    return static_cast<int>(std::round(final_damage));
}
int main(){
    int power, atk, def_stat;
    float effectiveness ,stab;

    cin>> power >> atk >> def_stat >> effectiveness >>stab;

    int damage = calculate_damage(power, atk, def_stat,effectiveness,stab);

    cout<< damage << endl;
    return 0;
}
/*
Module: damage_calc.cpp

Responsibilities:
- Computes damage values using standard formula calculations for the backend engine.
- Communicates with Python via standard input/output streams (`cin`/`cout`).

Dependencies:
- standard -> iostream, string, cmath

Known problems:
- Stdout pollution: Printing debug text ("C++ Raw Base Damge:") directly to `cout` corrupts the standard output stream, causing Python subprocess parsing (`int(result.stdout.strip())`) to crash with a `ValueError`.
- Unused variable: `float_power` is declared but never used in the damage formula.
- Return type mismatch: Function is declared as returning `float` while returning an `int` cast.

Testing:
- No automated tests currently documented.
*/