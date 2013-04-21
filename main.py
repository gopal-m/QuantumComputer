import sys
import math
#add our bin folder to path
sys.path.insert(0, 'bin')
import qubit


a = qubit.Qubit()
b = qubit.Qubit(3.0/5,4.0/5)
c= 	qubit.Qubit(1/math.sqrt(2),1j/math.sqrt(2))
b.entangle(c)
c.entangle(a)
#no state is calculated until this is called
#due to laziness
state =  b.currentState
val = state.measure()
print "Measured state in integer form: " + str(val)
print "Measured state in basis form: " + bin(val)
