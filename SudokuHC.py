#Algoritmo do Sudoku por Hill-Climbing
import numpy
import math
from random import shuffle

#nome do arquivo contendo a entrada
nome_entrada="entrada.txt"
limit=350
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

def generateIndividual(board,size,emptyCount):
	individual = []
	temp=0
	numbers=range(1,size+1)
	for j in range(0,size):
		line=board[j,:]
		for x in line:
			if x!=-1: numbers.remove(x)
		shuffle(numbers)
		individual=individual + [numbers]
		numbers=range(1,size+1)
	return individual

def evalFunction(Individual, thisboard, expSum):
	#primeira parte da funcao: colocar os numeros no tabuleiro de acordo com a string do individuo
	finalResult=0
	tempResult=0
	tempArray=[]
	newBoard=thisboard.copy()
	genes=numpy.zeros((0,0))
	for x in Individual:
		genes = numpy.append(genes,[x])
	indexesToSub = numpy.where(thisboard==-1)
	for i in range(0,len(genes)):
		newBoard[indexesToSub[0][i]][indexesToSub[1][i]] = genes[i]
	#segunda parte da funcao: faz o calculo
	#calculo por linha
	rowConflicts=0
	for i in range(0,size):
		tempArray=[]
		for j in range(0,size):
			tempArray=numpy.append(tempArray,newBoard[i][j])
		uniques=len(numpy.unique(tempArray))
		rowConflicts = rowConflicts+ (size-uniques)
		tempResult=0
	#calculo por coluna
	colConflicts=0
	for j in range(0,size):
		tempArray=[]
		for i in range(0,size):
			tempArray=numpy.append(tempArray,newBoard[i][j])
		uniques=len(numpy.unique(tempArray))
		colConflicts = colConflicts+ (size-uniques)
		tempResult=0
	#calculo por bloco
	blockSize=math.sqrt(size)
	blocks=numpy.zeros((0,0))
	blockConflicts=0
	hBlocks = numpy.hsplit(newBoard,blockSize)
	for x in hBlocks:
		temp=numpy.vsplit(x,blockSize)
		for f in temp:
			uniques=len(numpy.unique(f))
			blockConflicts=blockConflicts+(size-uniques)
	#avaliacao final
	finalResult=float(rowConflicts+colConflicts+blockConflicts)+0.1
	return finalResult


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


def findSucessors(state,board):
	filledBoard=board.copy()
	temp=0
	sucessorList=[]
	for x in range(0,board.shape[0]):
		for i in range(0,len(state[x])):
			tempState=list(state)
			idx1=i
			for j in range(i+1,len(state[x])):
				line=list(state[x])
				idx2=j
				temp=line[idx1]
				line[idx1]=line[idx2]
				line[idx2]=temp
				tempState[x]=list(line)
				sucessorList.append(list(tempState))
	return sucessorList



def printBoard(indiv,board):
	newBoard=board.copy()
	genes=numpy.zeros((0,0))
	for x in indiv:
		genes = numpy.append(genes,[x])
	indexesToSub = numpy.where(board==-1)
	for i in range(0,len(genes)):
		newBoard[indexesToSub[0][i]][indexesToSub[1][i]] = genes[i]		
	print("===BOARD===")
	print(newBoard)
	print("EVAL:"), 
	print(evalFunction(Individual=indiv,thisboard=board,expSum=expSum))

def HillClimb(mboard,size,emptyCount,expSum):
	lastEvals=[0 for i in range(limit-1)]
	lastEvals.append(1)
	count=0
	initialState = generateIndividual(board=mboard.copy(),size=size,emptyCount=emptyCount)
	printBoard(indiv=initialState,board=mboard)
	while lastEvals.count(lastEvals[0]) != len(lastEvals):
		print(count),
		sucessorList=findSucessors(state=initialState,board=mboard.copy())
		evalMin=float("inf")
		for e in sucessorList:
			evaluation=evalFunction(Individual=e,thisboard=mboard.copy(),expSum=expSum)
			if evaluation<evalMin:
				evalMin=evaluation
				bestSucessor=list(e)
		lastEvals[count]=evalMin
		count+=1
		if count==limit: count=0
		initialState=list(bestSucessor)
	printBoard(indiv=list(bestSucessor),board=mboard.copy())



in_file = open(nome_entrada, 'r+')
print ("leu arquivo " + nome_entrada)
size=int(in_file.readline())
boardLine=in_file.readline()
board = makeBoard(boardLine,size)
in_file.close()
print(board)
unique, counts = numpy.unique(board, return_counts=True)
emptyCount = counts[0]
print(emptyCount)
expSum=findExpectedSum(size)
HillClimb(board,size,emptyCount,expSum)