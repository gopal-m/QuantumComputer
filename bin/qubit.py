
import numpy as np 
from math import sqrt
import random

#Class holds a quantum entangled state of 2^n where n=number qubits
class QuantumState: 

#Should be normalised by default
	
	def __init__(self,stateVector,normalise=False):
		self.stateVector = stateVector
		if(normalise):
			self.stateVector.normalise()

	def normalise(self):
		 self.stateVector = np.dot(self.stateVector,np.array(np.linalg.norm(self.stateVector)))
		 return self

	def measure(self):
		#take complex conjugate dot product for probability matrix
		
		probability = np.absolute(np.square(self.stateVector))
		print "state probabilities: "
		print probability
		#As probability matrix will sum to one, generate a random number between 0,1. Go through matrix
		#if sum at point is greater than random number stop as we have found the state. 
		position = random.random()
		print "random value: " +str(position)		
		it = np.nditer(probability,flags=['f_index'])
		total =0
		result = 0
		while not it.finished and total < position : 
			total+=it[0]
			result = it.index
			it.iternext()

		return result 

	@staticmethod
	def qubitToQuantumState(qubit):
		return quantumState(qubit.state)

#This is the qubit class
class Qubit:

	@property
	def currentState(self):return self.operations.state 
	
	
	def __init__(self,complex1=1/sqrt(2)+0j, complex2=1/sqrt(2)+0j,normalise=True):
		
		self.qubitState = QuantumState(np.array([complex1,complex2]))
		if(normalise):
			self.normalise()
		self.operations = StateOperations(self)
		


	def normalise(self):
		self.qubitState = self.qubitState.normalise()
		print self.qubitState.stateVector


	def entangle(self,qubit):
		print self.operations.ops
		self.operations.entangleQubit(qubit.operations)
		qubit.operations = self.operations
	def measure(self):
		self.currentState.measure()

	#required function to eventually calculate operations 
	#Should probably have an interface manage this for 
	#qubits and operators, however python doesn't require
	#interfaces necessarily 
	#this operation is just an outerproduct, and than reshape 
	# to 1D array, which is equivalent to tensor product
	def operate(self,quantumState):
		outer = np.outer(self.qubitState.stateVector,quantumState.stateVector)
		print QuantumState(np.reshape(outer,-1)).stateVector
		return QuantumState(np.reshape(outer,-1))


#Class to keep track of all applied operations, so that we can lazily evaluate state

class StateOperations:
	
	@property 
	def state(self): return self.generateState()
	
	def __init__(self,qubit):
		#list that holds all applied operations to date such as operators and entanglements
		self.ops = []
		self.qubits = 1
		self.operators = 0
		self.currState = QuantumState(np.array([1]))
		self.stateIsUpToDate = False
		self.ops.append(qubit)

	def entangleQubit(self,qubitOperations):
		#print qubitOperations.ops
		#print self.ops
		self.ops= self.ops + qubitOperations.ops
		self.qubits+=qubitOperations.qubits
		self.operators+=qubitOperations.operators
		self.stateIsUpToDate = False

	def applyOperator(self,operator):
		self.ops.append(operator)
		self.operators += 1
		self.stateIsUpToDate = False

	#This way work is culmative
	def generateState(self):
		print self.ops
		if (not self.stateIsUpToDate):
			self.currState = reduce(lambda to , apply : apply.operate(to),self.ops,self.currState)
		self.stateIsUpToDate = True		
		return self.currState



