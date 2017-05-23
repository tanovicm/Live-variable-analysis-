import sys
import re
import subprocess

def parsInstruction(line):
	'''
		Parsing name and parameters of instruction.
		
		@params line
		Instruction to parse.
		@returns
		Tuple: name of instruction, list of parameters
	'''
	
	parts = filter(None, re.split("[, \t]+",line))
	
	return (parts[0], parts[1:])

def loadInstructions(fileName):
	'''
		Loads instructions from file.
		Instructions are in following format:
		name param_in/out, ...
		
		@param fileName
		Instruction file.
		@returns 
		Dictionary with instructions as keys and list of parameters in/out as 
		values.
	'''
	return dict(parsInstruction(line.rstrip('\n')) for line in open(fileName))

def inoutOfInstruction(line):
	'''
		Determines in and out parameters of given instruction.
		@params line
		Instruction.
		@returns 
		Tuple: list of in parameters and list of out parameters.
	'''
	instruction, parameters = parsInstruction(line)
	inn = []
	out = []
	
	instructions = loadInstructions("instructions.txt")
	
	if instruction in instructions:
		for type, param in zip(instructions[instruction], parameters):
			if param[0] is not '%' or ':' in param:
				continue
			if 'in' in type:
				inn += [param]
			if 'out' in type:
				out += [param]
				
	return (inn, out)

def compileCppToAssembly(fileName):
	'''
		Compiles .cpp files to .s file and returns list of lines from .s file.
		
		@params fileName 
		.cpp file to compile
	
		@return
		List of lines in compiled .s file
	'''
	subprocess.call(["g++", "-S", fileName])
	
	return [line.rstrip('\n') for line in open(fileName[:-4] + ".s")]

def compileCToAssembly(fileName):
	'''
		Compiles .cpp files to .s file and returns list of lines from .s file
		
		@params fileName 
		.c file to compile
	
		@return
		List of lines in compiled .s file
	'''
	subprocess.call(["gcc", "-S", fileName])
	
	return [line.rstrip('\n') for line in open(fileName[:-2] + ".s")]

def compileToAssembly(fileName):
	'''
		Calls the appropriate function to compile fileName file based on extension.
		
		@params fileName 
		File to compile.
		
		@return
		List of lines in .s file.
	'''

	extension = fileName.split(".")[-1]
	
	compileExtensionToAssembly = {
	    "c"   : compileCToAssembly,
	    "cpp" : compileCppToAssembly
    }
	
	return compileExtensionToAssembly[extension](fileName)

def createBasicBlocks(lines):
	'''
		Creates basic block from list of lines from .s file.
		
		@params lines
		List of line from .s file.
		@return 
		List of basic blocks for .s file.
	'''
	basicBlocks = []
	basicBlock = []
	
	ctrFlowCmds = ["jmp", "ret", "je", "jle", "jge","jl", "jg", "jne"]
	
	for line in lines:
		if ":" in line and line[0] is '.':
			if len(basicBlock) > 0:
				basicBlocks += [basicBlock];
				
			basicBlock = []
		
		basicBlock += [line];
		
		if any(cmd in line for cmd in ctrFlowCmds):
			if len(basicBlock) > 0:
				basicBlocks += [basicBlock];
				
			basicBlock = []
			
	if len(basicBlock) > 0:
		basicBlocks += [basicBlock];
		
	return basicBlocks

def createInOutForBasicBlock(basicBlock):
	'''
		Creates in and out parametar list for every instruction in the basic block.
		
		@param basicBlock
		Basic block.
		@returns 
		List of tuples containing in and out parameters for each instruction.
		
	'''
	inOutBasicBlock = []
	
	for line in basicBlock:
		inn, out = inoutOfInstruction(line)
		if len(inn) or len(out):
			inOutBasicBlock += [(inn, out)];
			
	return inOutBasicBlock

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print "Usage: ./liveness_of_variables filename.cpp"
		exit(1)
	
	basicBlocks = createBasicBlocks(compileToAssembly(sys.argv[1]))
		
	# Print of basic blocks
	# in znaci da citas iz te promenjive a out da pises u nju
	for block in basicBlocks:
		inOutBlock = createInOutForBasicBlock(block)
		if len(inOutBlock) == 0:
			continue
		
		print "; BAZICNI BLOK"
		for inn, out in inOutBlock:
			print ' in: %-10s out: %-10s' % (', '.join(inn), ', '.join(out))
		print "; KRAJ BAZICNI BLOK\n"
		
	