#/usr/bin/python
import itertools

class Trie:
    def __init__(self, value='', weight=0, parent=None):
        self.parent = parent
        self.weight = weight
        self.value = value
        self.children = []
    
    def child_values(self):
        return [ child.value for child in self.children ]

    def search(self, string):
        return self.search_stack(list(string[::-1]))
            
    def search_stack(self, stack):
        if len(stack) == 0:
            return self
        else:
            char = stack.pop()
            if char in self.child_values():
                child = [ child for child in self.children if char == child.value ][0]
                return child.search_stack(stack)
            else:
                return None
            
    def insert(self, string):
        return self.insert_stack(list(string[::-1]))

    def insert_stack(self, stack):
        if len(stack) == 0:
            #I am the result
            self.weight += 1
        else:
            char = stack.pop()
            if char in self.child_values():
                #grab child
                child = [ child for child in self.children if char == child.value ][0]
                child.insert_stack(stack)
            else:
                #create new child
                child = Trie(value=char, parent=self)
                child.insert_stack(stack)
                self.children.append(child)
                
    def word_value(self):
        if self.parent is None:
            return ''
        return self.parent.word_value() + self.value

    def words(self):
        if self.weight > 0:
            print self.word_value()
            
        for child in self.children:
            child.words()

def matrix_contains(matrix, x, y):
    result = False
    if (len(matrix) > x >= 0) and (len(matrix[x]) > y >= 0):
        result = True
        
    return result

class Node:
    def __init__(self, value):
        self.value = value
        
def print_graph(graph):
    print len(graph.keys())
    for key in graph.keys():
        result = '' + key.value + ' '
        result_list = []
        for key2 in graph[key]:
            result_list.append(key2.value)
        print result + str(result_list)

def construct_graph(matrix):
    result = {}
    for cx, x in enumerate(matrix):
        for cy, y in enumerate(x):
            neighbors = []
            possible_neighbors = list(itertools.product([cx - 1, cx, cx + 1],[cy - 1, cy, cy + 1]))
            
            for pn in possible_neighbors:
                if pn != (cx,cy):
                    if matrix_contains(matrix,pn[0],pn[1]):
                        neighbors.append(matrix[pn[0]][pn[1]])
                    
            #if cx - 1 >= 0
            result[y] = neighbors
    return result

def recurse_through_nodes(graph, node, trie, string):
    result = trie.search(string)
    if result is not None:
        if result.weight > 0 and len(string) >= 3:
                print result.word_value()
        for node in graph[node]:
            recurse_through_nodes(graph,node,trie,string + node.value)
        
# find matches
def find_matches(graph,trie):
    for node in graph.keys():
        new_string = node.value
        recurse_through_nodes(graph, node, trie, new_string)

if __name__ == '__main__':
    string = 'racecar aebxiod poieunx dankeur opcoede recktno obscurt'
    matrix = []
    for line in string.split():
        matrix.append([Node(char) for char in list(line)])
    graph = construct_graph(matrix)
    trie = Trie()
    with open("words.txt","r") as lines:
        for count, line in enumerate(lines):
            trie.insert(line.strip())
    trie.insert('tux')
    trie.insert('racecar')
    #print_graph(graph)
    find_matches(graph,trie)
