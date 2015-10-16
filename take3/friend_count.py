import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: person id
    # value: count
    mr.emit_intermediate(record[0], 1)
    

def reducer(key, list_of_values):
    # key: person id
    # value: list of 1's (one for each friend)
    total = 0
    for v in list_of_values:
      total += v
    mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
  
  
"""
Consider a simple social network dataset consisting of a set of key-value pairs (person, friend) representing a friend relationship between two people. Describe a MapReduce algorithm to count the number of friends for each person.

Map Input

Each input record is a 2 element list [personA, personB] where personA is a string representing the name of a person and personB is a string representing the name of one of personA's friends. Note that it may or may not be the case that the personA is a friend of personB.

Reduce Output

The output should be a pair (person, friend_count) where person is a string and friend_count is an integer indicating the number of friends associated with person.

You can test your solution to this problem using friends.json:

$ python friend_count.py friends.json
You can verify your solution by comparing your result with the file friend_count.json.
"""
