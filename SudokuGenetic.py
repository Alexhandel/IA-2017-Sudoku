import random
import numpy
import math


from deap import base
from deap import creator
from deap import tools
from deap import algorithms

numpy.random.seed()

#nome do arquivo contendo a entrada
nome_entrada="entrada.txt"
initPop=100
NGEN=50
CXPB=0.8
MUTPB=0.1


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


in_file = open(nome_entrada, 'r+')
print ("leu arquivo " + nome_entrada)
size=int(in_file.readline())
boardLine=in_file.readline()
print(size)
thisboard = makeBoard(boardLine,size)
print("BOARD: \n",thisboard)
unique, counts = numpy.unique(thisboard, return_counts=True)
emptyCount = counts[0]
in_file.close()
expSum=findExpectedSum(size)

def evaluate(Individual):
	#primeira parte da função: colocar os numeros no tabuleiro de acordo com a string do individuo
	#print("IND:  ",Individual[1])
	#print(thisboard)
	finalResult=0
	tempResult=0
	newBoard=thisboard.copy()
	#print(newBoard,"manga")
	genes=numpy.zeros((0,0))
	#temp=Individual.split(' ')
	#print(temp)
	for x in Individual:
		genes = numpy.append(genes,[x])
	#print(genes)
	indexesToSub = numpy.where(thisboard==-1)
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
	finalResult=float(rowResult+colResult+blockResult)+0.1
	#print("FINAL EVAL:",finalResult)
	return(finalResult),


def genRandom():
	return numpy.random.random_integers(1, high=size)


IND_SIZE=emptyCount

creator.create("FitnessMin", base.Fitness, weights=(-10.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()
toolbox.register("attr_float", genRandom)
toolbox.register("individual", tools.initRepeat, creator.Individual,toolbox.attr_float, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate",tools.mutUniformInt,low=1,up=size, indpb=MUTPB)
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("evaluate", evaluate)
mstats = tools.Statistics(lambda ind: ind.fitness.values)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
mstats.register("min", numpy.min)
mstats.register("max", numpy.max)
HoF= tools.HallOfFame(1)

pop= toolbox.population(n=initPop)
for ind in pop:
	ind.fitness.values = evaluate(ind)

endPop, log = algorithms.eaSimple(pop,toolbox,CXPB,MUTPB,NGEN, stats=mstats,halloffame=HoF,verbose=True)
for ind in endPop:
	ind.fitness.values = evaluate(ind)
	#print("FITNESS:", ind.fitness.values)
print("BEST INDIV:",HoF,"FITNESS:",evaluate(HoF))
print(len(endPop), initPop)



