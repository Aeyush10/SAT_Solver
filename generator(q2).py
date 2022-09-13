import numpy as np
from pysat.solvers import Solver
from pysat.card import *
import csv
import pandas as pd
import random
s = Solver(name='mc')

k = input("Enter k value: ")
k = int(k)

#Creating filled Sudoku Pair

#Sudoku 1: 
#Cell: Each number at most once
for i in range(0,k*k ):
	for j in range(0,k*k):
		s.add_atmost(lits =range(1 + j*k*k + i*k**4, k*k + 1 + j*k*k + i*k**4), k = 1)

#Row: Each number at most once
for i in range(0,k*k):
	for p in range(1,k*k + 1):
		s.add_atmost( np.arange(p +  i*k**4, p + k**4 + i*k**4, k*k, dtype = int).tolist(), k = 1)
			
#Col: Each number at most once
for j in range(0,k*k):
	for p in range(1,k*k + 1):
		s.add_atmost( np.arange(p + j*k*k, p + j*k*k + k**6, k**4, dtype = int).tolist(), k = 1)


#Box: Each number at least (and thus exactly) once
top_left = []
for i in np.arange(0,k*k,k,dtype = int).tolist():
	for j in np.arange(0,k*k,k,dtype = int).tolist():
		top_left.append(1 + j*k*k + i*k**4)
for t in top_left:
	for p in range(0, k*k):
		x = []
		for i in range(0,k):
			for j in range (0, k):
				x.append(t + p + j*k*k + i*k**4)
		s.add_clause(x)


#Sudoku 2: 
#Cell: Each number at most once
for i in range(0,k*k ):
	for j in range(0,k*k):
		s.add_atmost(lits =range(1 + j*k*k + i*k**4 + k**6, k*k + 1 + j*k*k + i*k**4+ k**6), k = 1)

#Row: Each number at most once
for i in range(0,k*k):
	for p in range(1,k*k + 1):
		s.add_atmost( np.arange(p +  i*k**4+ k**6, p + k**4 + i*k**4+ k**6, k*k, dtype = int).tolist(), k = 1)
			
#Col: Each number at most once
for j in range(0,k*k):
	for p in range(1,k*k + 1):
		s.add_atmost( np.arange(p + j*k*k+ k**6, p + j*k*k + k**6+ k**6, k**4, dtype = int).tolist(), k = 1)


#Box: Each number at least (and thus exactly) once
top_left = []
for i in np.arange(0,k*k,k,dtype = int).tolist():
	for j in np.arange(0,k*k,k,dtype = int).tolist():
		top_left.append(1 + j*k*k + i*k**4 + k**6)
for t in top_left:
	for p in range(0, k*k):
		x = []
		for i in range(0,k):
			for j in range (0, k):
				x.append(t + p + j*k*k + i*k**4)
		s.add_clause(x)

#Adding Sudoku Pair Condition
for i in range(1,k*k + 1):
	for j in range(1,k*k + 1):
		for p in range(1,k*k + 1):
			s.add_atmost(lits = [(p + (j - 1)*k*k + (i - 1)*k**4),(p + (j - 1)*k*k + (i - 1)*k**4 + k**6)], k = 1)

#Adding Randomisation 
s.solve([random.choice(range(1,k*k+1)) + random.choice(range(0,k*k))*k*k + random.choice(range(0,k*k))*k**4])

x = s.get_model()

#Removing the first model as a possible solution
for i in range(0,2*k**6):
	x[i] = -x[i]
s.add_clause(x)

#Converting model to 2D list
for i in range(0,2*k**6):
	x[i] = -x[i]

arr = []
for i in range(0,k*k):
	row = []
	for j in range(0,k*k):
		for p in range(0,k*k):
			if ( x[p + j*k*k + i*k**4] >0 ):
				row.append(p + 1)
	arr.append(row)

for i in range(0,k*k):
	row = []
	for j in range(0,k*k):
		for p in range(0,k*k):
			if ( x[p + j*k*k + i*k**4+ k**6] >0 ):
				row.append(p + 1)
	arr.append(row)	

#Converting model to input list
inp = []
for i in range(0,2*k*k): 
	for j in range(0,k*k):
			inp.append(arr[i][j] + j*k*k + i*k**4)


#Removing value at each index and checking for more solutions
inp_indices = [*range(0,2*k**4)]
while (len(inp_indices) > 0):

	a = random.choice(range(0,2*k*k))
	b = random.choice(range(0,k*k))
	if (arr[a][b] == 0):
		continue
	if (arr[a][b] + b*k*k + a*k**4 in inp):
		inp.remove(arr[a][b] + b*k*k + a*k**4)
	if (a*k*k + b in inp_indices):
		inp_indices.remove(a*k*k + b)
	temp = arr[a][b]
	arr[a][b] = 0

	if (s.solve(inp) == True): 
		#New Solution exists
		arr[a][b] = temp
		continue

#Display partially filled Sudoku Pair with unqiue solution
print("Sudoku 1: ")
for i in range(0,k*k):
	for j in range(0,k*k):
		if (arr[i][j] < 10):
			print('',arr[i][j],end = ' ')
		else:
			print(arr[i][j],end = ' ')
		if ((j+1)%k == 0):
			print("  ", end= '')
	print('')
	if ((i+1)%k == 0):
		print("")

print("\n\n\nSudoku 2: ")
for i in range(k*k,2*k*k):
	for j in range(0,k*k):
		if (arr[i][j] < 10):
			print('',arr[i][j],end = ' ')
		else:
			print(arr[i][j],end = ' ')
		if ((j+1)%k == 0):
			print("  ", end= '')
	print('')
	if ((i+1)%k == 0):
		print('')

#Send partially filled Sudoku Pair to .csv file 
df=pd.DataFrame(arr)
df.to_csv('output_q2.csv', index=False, header = False)