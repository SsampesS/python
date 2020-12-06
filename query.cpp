#include "Header.h"

bool isValid(string decOctet)
{
	for (int i = 0; i < decOctet.length(); i++)
		if (isdigit(decOctet[i]) == false)
			return false;

	return true;
}

int query(int i)
{
	string input{};
	int decOctet{};
	cin >> input;

	while (isValid(input) == false)
	{
		cout << "Invalid input.\n";
		cin.clear();										 // Clear error flags
		cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Clear out the input buffer
		cout << "Try again: ";
		cin >> input;
	}
	if (isValid(input) == true)
		decOctet=stoi(input);

	while (i == 0 && decOctet > 255)
	{
		cout << "The decimal must be between 0-255.\n";
		cout << "Try again: ";
		cin >> decOctet;
	}

	cout << "------------------\n";
	return decOctet;
}