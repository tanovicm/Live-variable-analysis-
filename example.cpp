#include <stdio.h>
#include <stdlib.h>
       
int main() {
	volatile int a = 17;
	
	if (a > 5)
		a += 5;
	else 
		a -= 5;
		
	printf("%d\n",a);
	
	for (int i = 0; i < abs(a); i++) {
		printf("%d ", a+i);
	}
	
	a += 7;
	return 0;
}