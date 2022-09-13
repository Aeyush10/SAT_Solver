import numpy as np
from pysat.solvers import Solver
from pysat.card import *
import csv
import pandas as pd
s = Solver(name='mc')

k = input("Enter k value: ")
k = int(k)

#Opening input file
with open('input_q1.csv', 'r') as f:
  file = csv.reader(f)
  my_list = list(file)
  for i in range(0,2*k*k):
      for j in range(0,k*k):
          my_list[i][j]=int(my_list[i][j])

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


#Assuming inputs
inp = []
#Sudoku 1 inputs:
for i in range(0,k*k): 
	for j in range(0,k*k):
		if (my_list[i][j] != 0):
			inp.append(my_list[i][j] + j*k*k + i*k**4)

#Sudoku 2 inputs:
for i in range(k*k,2*k*k):
	for j in range(0,k*k):
		if (my_list[i][j] != 0):
			inp.append(my_list[i][j] + j*k*k + (i - k*k)*k**4 + k**6)

s.solve(inp)
x = s.get_model()

#Converting model to 2D list
if (x is not None):
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

#Sending solution to .csv file
	df=pd.DataFrame(arr)
	df.to_csv('output_q1.csv', index=False)
else:
	print("None")