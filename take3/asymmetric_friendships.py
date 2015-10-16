import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

seen = []

def mapper(record):
    # key: person a
    # value: person b
    mr.emit_intermediate(0, record)
    
def reducer(key, list_of_values):
    # key: person a
    # value: list of all friends of persone a
    #print list_of_values
    
    friendships = []
    for v in list_of_values:
        if [v[1], v[0]] in list_of_values:
            continue
        else:
            friendships.append([v[0],v[1]])
            friendships.append([v[1],v[0]])
    
    for f in friendships:
        mr.emit((f[0],f[1]))   
    

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
  

"""
The relationship "friend" is often symmetric, meaning that if I am your friend, you are my friend. Implement a MapReduce algorithm to check whether this property holds. Generate a list of all non-symmetric friend relationships.

Map Input

Each input record is a 2 element list [personA, personB] where personA is a string representing the name of a person and personB is a string representing the name of one of personA's friends. Note that it may or may not be the case that the personA is a friend of personB.

Reduce Output

The output should be all pairs (friend, person) such that (person, friend) appears in the dataset but (friend, person) does not.

You can test your solution to this problem using friends.json:

$ python asymmetric_friendships.py friends.json
You can verify your solution by comparing your result with the file asymmetric_friendships.json.
"""
