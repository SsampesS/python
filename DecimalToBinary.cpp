#include "Header.h"
array <string, 4> ipBinaryArray;
int hostQuery{};

int main()
{
    cout << "Provide the IP-address of your network.\n" << "Press ENTER after each address part instead of the typical 'dot'.\n";
    for (int i{ 0 }; i < 4; i++)

        ipBinaryArray[i] = { decimalConverter(query(0)) };          // Calls function binaryConverter with value recieved from query()

    cout << "How many hosts does your network support?\n";
    hostQuery = query(1);
    subnetmaskCalc(hostQuery);
    return 0;
}