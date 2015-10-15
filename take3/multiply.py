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
    #print "MAP", record
    # key: (i, k)
    # value: A[i,j]
    # for every k in 1..N, N is number of columns in B
    # A is L X M; B = M X N
    # correspondingly for B
    
    key = record[0]
    value = record[1:]
    #print key, value
    
    if key == 'a':
        for k in range(N):
            mr.emit_intermediate((record[1], k), (key, record[2], record[3]))
    elif key == 'b':
        for i in range(L):
            mr.emit_intermediate((i, record[2]),(key, record[1], record[3])) 

def reducer(key, list_of_values):
    #print "REDUCE",
    # key: (i, k)
    # value: sum(A[i,j] * B[j,k])
    #print key, ":", list_of_values
    (i,k) = key
    
    total = 0 
    tempA = {}
    tempB = {}
    for v in list_of_values:
        if v[0] == 'a':
            #print "i,j:", i,  v[1], v[2]
            tempA[v[1]] = v[2]
        else:
            #print "j,k:", v[1], k, v[2]
            tempB[v[1]] = v[2]
    #tempA = sorted(tempA)
    #tempB = sorted(tempB)
    
    #print "\n", tempA
    #print "\n", tempB, "\n"
    for j in range(M):
        if j in tempA and j in tempB:
            total += tempA[j] * tempB[j]
            
    #for a in tempA:
    #    print "A[", i, ", ", a[0], "] = ", a[1]
    #for b in tempB:
    #    print "B[", b[0], ", ", k, "] = ", b[1]
    mr.emit((i,k, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
