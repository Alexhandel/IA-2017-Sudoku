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

#Parametros do Genetico. Mudar aqui
initPop=100
NGEN=50
CXPB=0.8
MUTPB=0.01

#função auxiliar para conversão de string
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#função que acha a soma esperada em cada linha, coluna e bloco
def findExpectedSum(size):
	expSum = sum(range(1,size+1))
	return expSum


#função que retorna um vetor tabuleiro a partir da entrada em texto
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
#fim da função

#Função de fitness do genetico
def evaluate(Individual):
	#primeira parte da função: colocar os numeros no tabuleiro de acordo com a string do individuo
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
	#segunda parte da função: faz o calculo
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
	#avaliação final
	finalResult=float(rowConflicts+colConflicts+blockConflicts)+0.1
	return(finalResult),

#gerador de numero aleartorio
def genRandom():
	return numpy.random.random_integers(1, high=size)

in_file = open(nome_entrada, 'r+')    
print ("leu arquivo " + nome_entrada)
size=int(in_file.readline())		#le a primeira linha, contem o tamanho do tabuleiro
boardLine=in_file.readline()
thisboard = makeBoard(boardLine,size)
print("BOARD: \n",thisboard)
unique, counts = numpy.unique(thisboard, return_counts=True) #conta quantos espaços vazios existem
emptyCount = counts[0]
in_file.close()
expSum=findExpectedSum(size)
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

pop= toolbox.population(n=initPop)		#inicializa a população inicial
for ind in pop:		#loop que avalia o fitness da população inicial
	ind.fitness.values = evaluate(ind)

endPop, log = algorithms.eaSimple(pop,toolbox,CXPB,MUTPB,NGEN, stats=mstats,halloffame=HoF,verbose=True) #essa é a linha que de fato faz e roda o genetico
for ind in endPop:		#loop que avalia o fitness da população final
	ind.fitness.values = evaluate(ind)
print("BEST INDIV:",HoF,"FITNESS:",evaluate(HoF)) #printa o individuo com melhor fitness entre todas as gerações
print(len(endPop), initPop)



