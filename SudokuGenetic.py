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
CXPB=0.9
MUTPB=0.01

#funcao auxiliar para conversao de string
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#funcao que acha a soma esperada em cada linha, coluna e bloco
def findExpectedSum(size):
	expSum = sum(range(1,size+1))
	return expSum


#funcao que retorna um vetor tabuleiro a partir da entrada em texto
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
#fim da funcao

#Funcao de fitness do genetico
def evaluate(Individual):
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
	return(finalResult),

#gerador de numero aleartorio
def genRandom():
	return numpy.random.random_integers(1, high=size)


def selElitistAndTournament(individuals, k_elitist, k_tournament, tournsize):
	return tools.selBest(individuals, k_elitist) + tools.selTournament(individuals, k_tournament, tournsize=3)





in_file = open(nome_entrada, 'r+')    
print ("leu arquivo " + nome_entrada)
size=int(in_file.readline())		#le a primeira linha, contem o tamanho do tabuleiro
boardLine=in_file.readline()
thisboard = makeBoard(boardLine,size)
print("BOARD: \n",thisboard)
unique, counts = numpy.unique(thisboard, return_counts=True) #conta quantos espacos vazios existem
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
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("selectE", selElitistAndTournament, k_elitist=1, k_tournament=initPop-1, tournsize=3)
toolbox.register("evaluate", evaluate)
mstats = tools.Statistics(lambda ind: ind.fitness.values)
mstats.register("avg", numpy.mean)
mstats.register("std", numpy.std)
mstats.register("min", numpy.min)
mstats.register("max", numpy.max)
HoF= tools.HallOfFame(1)

pop= toolbox.population(n=initPop)		#inicializa a populacao inicial

print(len(pop))
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
	ind.fitness.values = fit
for g in range(NGEN):
		# Select the next generation individuals
		offspring = toolbox.selectE(pop)
		# Clone the selected individuals
		offspring = list(map(toolbox.clone, offspring))
		# Apply crossover and mutation on the offspring
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < CXPB:
				toolbox.mate(child1, child2)
				del child1.fitness.values
				del child2.fitness.values
		for mutant in offspring:
			if random.random() < MUTPB:
				toolbox.mutate(mutant)
				del mutant.fitness.values
		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit
		pop[:] = offspring
		fits = [ind.fitness.values[0] for ind in pop]
		length = len(pop)
		mean = sum(fits) / length
		sum2 = sum(x*x for x in fits)
		std = abs(sum2 / length - mean**2)**0.5
		genMin=min(fits)
		genMax=max(fits)
		print("GENERATION: ",g+1,"   MIN: ",genMin,"   MAX: ",genMax,"   MEAN: ",mean,"   STDEV: ",std)
		if genMin==0.1:
			print("EUREKA")
			print(tools.selBest(pop,1))


bestIndividual=tools.selBest(pop,1)
print("BEST: ",bestIndividual, "FITNESS: ", bestIndividual[0].fitness.values)
