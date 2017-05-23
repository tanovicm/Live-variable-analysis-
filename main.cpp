#include <stdio.h>
#include <cstdlib>
#include <string>
#include <algorithm>

int main (int argc, char **argv) {
	
	if (2 != argc) {
		printf("Usage: ./liveness_of_variables filename.cpp");
		exit(1);
	}
	
	std::string command = "g++ -S " + std::string(argv[1]);
	if(-1 == system(command.c_str())) {
		printf("Shell not found!");
		exit(1);
	}
	
	std::string fileName = argv[1]
	fileName = fileName.substring(0, fileName.size() - 3) + ".s";
	FILE *file = fopen(fileName,'r');
	
	if (file == NULL) {
		printf("Couldn't compile %s.\n", fileName);
		exit(1);
	}
	std::string line;
	while (std::getline(file, line)) {
		
		printf("%s\n",line);
	}
	return 0;
}