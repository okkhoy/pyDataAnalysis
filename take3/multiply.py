import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

L = 5
M = 5
N = 5

def mapper(record):
    # key: (i, k)
    # value: A[i,j]
    # for every k in 1..N, N is number of columns in B
    # A is L X M; B = M X N
    # correspondingly for B
    
    key = record[0]
    value = record[1:]
    
    if key == 'a':
        for k in range(N):
            mr.emit_intermediate((record[1], k), (key, record[2], record[3]))
    elif key == 'b':
        for i in range(L):
            mr.emit_intermediate((i, record[2]),(key, record[1], record[3])) 

def reducer(key, list_of_values):
    # key: (i, k)
    # value: sum(A[i,j] * B[j,k])

    (i,k) = key
    
    total = 0 
    tempA = {}
    tempB = {}
    for v in list_of_values:
        if v[0] == 'a':
            tempA[v[1]] = v[2]
        else:
            tempB[v[1]] = v[2]

    for j in range(M):
        if j in tempA and j in tempB:
            total += tempA[j] * tempB[j]
            
    mr.emit((i,k, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
  

"""
Assume you have two matrices A and B in a sparse matrix format, where each record is of the form i, j, value. Design a MapReduce algorithm to compute the matrix multiplication A x B

Map Input

The input to the map function will be a row of a matrix represented as a list. Each list will be of the form [matrix, i, j, value] where matrix is a string and i, j, and value are integers.

The first item, matrix, is a string that identifies which matrix the record originates from. This field has two possible values: "a" indicates that the record is from matrix A and "b" indicates that the record is from matrix B.

Reduce Output

The output from the reduce function will also be a row of the result matrix represented as a tuple. Each tuple will be of the form (i, j, value) where each element is an integer.

You can test your solution to this problem using matrix.json:

$ python multiply.py matrix.json
You can verify your solution by comparing your result with the file multiply.json.
"""
