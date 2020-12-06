#include "Header.h"
array <string, 4> subnetMask, decimalMask;
int hostAmount{ 0 }, arrayMemb{ 3 }, strReplace{ 0 };
string str;
unsigned char len{ 8 };

bool arrayCheck(string binaryArray)                             // Checks if array member has 1's or 0's in it. 
{
    if (count(binaryArray.begin(), binaryArray.end(), '1') == 0)
        return false;
    else
        return true;
}

void subnetmaskCalc(int hostQuery)
{
    subnetMask.fill("11111111");                                // Filling the subnetMask with 1's as it is the "default" subnetmask address
    for (int maskZeroes{ 1 }; hostAmount < hostQuery; maskZeroes++)
    {
        hostAmount = (pow(2.0, maskZeroes) - 2);                // Using the formula 2^x-2 gives us the amount of hosts a subnetmask can sustain. Variable maskZeroes 
        str.append("0");                                        // is the x in this formula. str-variable is used to replace subnetMask-array member contents.
        strReplace += 1;
        if (str.length() > len)                                 // Clearing str to 0 because each member of the array is supposed to be 8-bit length. Another variable len
        {                                                       // is used because str.length() returns as bytes and byte > int -arithmetics is not possible in c++.
            str.clear();
            str.append("0");
        }
        if (strReplace == 9)                                    // strReplace is used in string.replace() to tell how many digits we wish to replace. It is cleared after 
            strReplace = 1;                                     // exceeding value "8" as explained previously.

        if (arrayCheck(subnetMask[arrayMemb]) == false)         // If the array member has no 1's in it, meaning they have all been replaced with 0's, this is used to swap
        {                                                       // to the next array member (which is presumed to have only 1's in it)
            arrayMemb -= 1;   
            subnetMask[arrayMemb].replace((8 - strReplace), strReplace, str);
        }
        else
        {                                                       // The default snippet to be executed. Replaces 1's in the array member.
            subnetMask[arrayMemb].replace((8 - strReplace), strReplace, str);
        }
        for (int i{ 0 }; i < 4; i++)
        {
            if (subnetMask[i].length() < len)
                subnetMask[i].append("0");
        }
    }
    for (int i{ 0 }; i < 4; i++) 
        decimalMask[i] = { binaryConverter(subnetMask[i], 4) };
    cout << "...and after conversion to decimal: " << "\n";
    for (int i = 0; i < 4; i++)
        cout << decimalMask[i] << ".";
    
}//cout << "HOSTAMOUNT : " << hostAmount << " "<<  "MASKZEROES : " << maskZeroes << " " << "STR CONTENTS : " << str <<"\n";