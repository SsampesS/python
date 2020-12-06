#include "Header.h"
string decimalString;
int binaryAsDec{ 0 }, decCalc{};

string binaryConverter(string binaryString, int size)
{
	for (int i{ 7 }; i > -1; i--)
	{
		if (binaryString[i] == 48) 
			decCalc = (0 * pow(2.0, i));
		else 
			decCalc = (1 * pow(2.0, i));
		binaryAsDec = binaryAsDec + decCalc;
		//cout << "BINAARYASDEC: " << " " << binaryAsDec << "\n";
	}
	decimalString = to_string(binaryAsDec);
	binaryAsDec = 0;

	return decimalString;
}