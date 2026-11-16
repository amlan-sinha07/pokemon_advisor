#include <iostream>
#include <cmath>

using namespace std;

int calculate_damage(
    int power,
    int atk,
    int def_stat,
    double effectiveness,
    double stab
) {
    double base=
    (((2.0 * 50 / 5 + 2 )*power*atk/ def_stat)/50)+2;
    double final_damage =base *stab *effectiveness;
    return static_cast<int>(std::round(final_damage));
}
int main(){
    int power, atk, def_stat;
    double effectiveness ,stab;

    if (!(std::cin>>power>>atk>>def_stat>>
    effectiveness>>stab)){
        std::cerr<<"Invalid input received.\n";
        return 1;
    }
    if (power<0 || atk<=0 || def_stat<=0 ||
        effectiveness<0 ||stab<=0){
            std::cerr<< "Invalid damage parameters\n";
            return 1;
        }

    int damage = calculate_damage(
        power,
        atk,
        def_stat,
        effectiveness,
        stab
    );

    std::cout<< damage << '\n';
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