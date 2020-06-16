#include "Header.h"

int Fibonacci(int n)
{
	int x{ 0 }, y{ 1 }, z{ };

	cout << "The fibonacci series: ";

	z = x + y;

	for (int b = 0; b < n; b++) 
	{
		switch (b)
		{
		case 0:
			cout << x;
			break;
		case 1:
			cout << y;
			break;
		}
		z = x + y;
		x = y;
		y = z;

		cout << z << " ";
	}

	return 0;
}
