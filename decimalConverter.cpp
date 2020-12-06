#include "Header.h"

string decimalConverter(int decOctet)
{
	string binaryOctet;
	int division{ decOctet }, octLen{ 8 };
	switch (decOctet)
	{
	case 0:
	{
		binaryOctet.append("00000000");
		return binaryOctet;
	}
	case 1:
	{
		binaryOctet.append("00000001");											// doing the conversion of "1" here because 
		return binaryOctet;														// it caused issues in the main conversion.
	}
	default:
	{
		while (division >= 1)
		{
			if (division != 1 && division == decOctet)
			{
				binaryOctet += to_string(division % 2);							// executing the first division
				division = decOctet / 2;										// binary added to binaryOctet
				binaryOctet += to_string(division % 2);
			}
			if (division == 1)
			{
				while (octLen != binaryOctet.length())							// adding the excempted zeroes to the binary. 
					binaryOctet.append("0");
				reverse(binaryOctet.begin(), binaryOctet.end());				// reversing the string to show the binary in a 'correct' way
				break;
			}
			else
				division = division / 2;										// executing subsequent divisions

			binaryOctet += to_string(division % 2);								// binary added to binaryOctet
		}
		return binaryOctet;
	}
	}
}