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
