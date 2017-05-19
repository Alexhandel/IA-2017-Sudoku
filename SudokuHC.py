#Algoritmo do Sudoku por Hill-Climbing
import numpy
import math

#nome do arquivo contendo a entrada
nome_entrada="entrada.txt"
initPop=100
maxIterations=35
numpy.random.seed()

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def findExpectedSum(size):
	expSum = sum(range(1,size+1))
	return expSum

def makeBoard(boardEntry,size):
	board = numpy.zeros((size,size))
	i=0
	j=0
	rows=boardEntry.split(";")
	for row in rows:
		row = row.rstrip()
		elementsInRow=row.split(",")
		for element in elementsInRow:
			element=element.rstrip()
			if RepresentsInt(element):
				board[i][j]=int(element)
			j=j+1
		j=0
		i=i+1
	return board

def generatePopulation(board,size,initPop,emptyCount):
	popList = []
	aux = []
	tempString=""
	for i in range(0,initPop):
		for j in range(0,emptyCount):
			tempString = tempString + str(numpy.random.random_integers(1, high=size)) + " "
		popList = popList + [tempString]

		tempString=""
	#print(popList)
	return popList

def evalFunction(Individual, thisboard, expSum):
	#primeira parte da função: colocar os numeros no tabuleiro de acordo com a string do individuo
	finalResult=0
	tempResult=0
	newBoard=thisboard.copy()
	#print(newBoard,"manga")
	genes=numpy.zeros((0,0))
	temp=Individual.split(' ')
	for x in temp:
		if RepresentsInt(x):
			genes = numpy.append(genes,[int(x)])
	#print(genes)
	indexesToSub = numpy.where(board==-1)
	#print(indexesToSub)
	for i in range(0,len(genes)):
		newBoard[indexesToSub[0][i]][indexesToSub[1][i]] = genes[i]
	#print (newBoard)
	#segunda parte da função: faz o calculo
	#calculo por linha
	rowResult=0
	for i in range(0,size):
		for j in range(0,size):
			tempResult=tempResult+newBoard[i][j]
		#	print ("tempResult is",tempResult, "after board", board[i][j])
		rowResult = rowResult+ abs((tempResult-expSum))
		#print("ROWS:",rowResult)
		tempResult=0
	#calculo por coluna
	colResult=0
	for j in range(0,size):
		for i in range(0,size):
			tempResult=tempResult+newBoard[i][j]
			#print ("tempResult is",tempResult, "after board", board[i][j])
		colResult = colResult+ abs((tempResult-expSum))
		#print("COLUMNS", colResult)
		tempResult=0
	#calculo por bloco
	blockSize=math.sqrt(size)
	blocks=numpy.zeros((0,0))
	blockResult=0
	hBlocks = numpy.hsplit(newBoard,blockSize)
	#print (hBlocks)
	for x in hBlocks:
		#print(x)
		temp=numpy.vsplit(x,blockSize)
		for f in temp:
			#print(f,"  BANANA")
			blocks = numpy.append(blocks,f)
	#print(blocks)
	for x in range(0,size):
		for y in range (0,size):
			tempResult=tempResult+blocks[y+(x*size)]
		blockResult = blockResult+ abs(tempResult-expSum)
		#print("BLOCKS:",blockResult)
		tempResult=0
	#avaliação final
	#print("ROW:",rowResult)
	#print("COLUMN:",colResult)
	#print("BLOCK:",blockResult)
	finalResult=rowResult+colResult+blockResult
	print("FINAL EVAL:",finalResult)
	return(finalResult)
	

def generateIntermediatePop(size, gameboard, expSum, population):
	maxResult = 0
	minResult = 100
	evalSum = 0
	evalMap = {}
	intPop = []
	ListOfCandidates = []
	for indiv in population:
		evalMap[indiv] = evalFunction(indiv, gameboard, expSum)
		if evalMap[indiv] > maxResult:
			maxResult=evalMap[indiv]
		if evalMap[indiv] < minResult:
			minResult=evalMap[indiv]
		evalSum= evalSum + evalMap[indiv]
	print (maxResult,minResult, evalSum)
	diff = maxResult - minResult
	piece = 100 / diff
	print("piece: ",piece)
	for i in range(0,len(population)):
		rando = numpy.random.random_integers(1, high=100)
		index = int((rando/piece)//1)
		if index == (diff): index=index-1
		print(rando,index)
		for indivi in evalMap:
			if evalMap[indivi]==index+minResult:
				ListOfCandidates=ListOfCandidates+[indivi]
		print(ListOfCandidates)
		individualToPass = ListOfCandidates[numpy.random.random_integers(0, high=(len(ListOfCandidates)-1))]
		print(individualToPass)
		ListOfCandidates=[]
	return 0

def doGenetic(mboard,size,emptyCount,expSum,initPop,maxIterations):
	initialPopulation = generatePopulation(mboard,size,initPop,emptyCount)
	intermediatePopulation = generateIntermediatePop(size,mboard,expSum,initialPopulation)		



in_file = open(nome_entrada, 'r+')
print ("leu arquivo " + nome_entrada)
size=int(in_file.readline())
boardLine=in_file.readline()
board = makeBoard(boardLine,size)
in_file.close()
#print(board)
unique, counts = numpy.unique(board, return_counts=True)
emptyCount = counts[0]
#print(emptyCount)
expSum=findExpectedSum(size)
doGenetic(board,size,emptyCount,expSum,initPop,maxIterations)