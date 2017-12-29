# Spark GraphFrames (GraphX)

## Housekeeping
### Official guide
https://graphframes.github.io/user-guide.html
### PySpark interactive shell
Note that you need the `--packages` option to access the `graphframes` package. 
```bash
pyspark --packages graphframes:graphframes:0.1.0-spark1.6
```

## Graph Operations
### Declare a `GraphFrame`
```python
# Import graphframes package
from graphframes import *

# Vertices
v = sqlContext.createDataFrame([ 
("a", "Alice", 34), 
("b", "Bob", 36), 
("c", "Charlie", 30), 
("d", "David", 29), 
("e", "Esther", 32), 
("f", "Fanny", 36) 
], ["id", "name", "age"]) 

# Edges
e = sqlContext.createDataFrame([ 
("a", "e", "friend"), 
("f", "b", "follow"), 
("c", "e", "friend"), 
("a", "b", "friend"), 
("b", "c", "follow"), 
("c", "b", "follow"), 
("f", "c", "follow"), 
("e", "f", "follow"), 
("e", "d", "friend"), 
("d", "a", "friend") 
], ["src", "dst", "relationship"]) 

# Graph
g = GraphFrame(v, e)
```

### Calculate stuff from a GraphFrame

#### Vertices and edges
```python
g.vertices.show()
g.edges.show()
```

#### Filter (like SQL's `where`)
```python
g.vertices.filter("age > 35")   # returns a DataFrame
```

#### Degrees
```python
g.inDegrees.show()

g.outDegrees.show()

g.degrees.show()
```

#### Pattern search
Motif means repeated pattern in a graph. 
GraphFrame uses a simple domain-specific language for [Motif finding](https://graphframes.github.io/user-guide.html#motif-finding) tasks.
- `(a)-[e]->(b)` refers to an edage `e` from `a` to `b`. 
- Vertices are denoted by parentheses: `(a)`
- Edges are denoted by square brackets: `[e]`
- Multiple conditions can be joint by semicolon: `(a)-[e]->(b); (b)-[e2]->(c)`
- Vertices and edges don't have to be named: `(a)-[]->(b)`, `(a)-[e]->()`
- An edge can be negated to indicate "no such edge": `(a)-[]->(b); !(b)-[]->(a)`
```python
motifs = g.find("(a)-[e]->(b); (b)-[e2]->(a)")    # g.find() returns a DataFrame
motifs.show()
```

#### BFS
Example: [user guide](https://graphframes.github.io/user-guide.html#breadth-first-search-bfs) | 
Syntax: [Python doc](https://graphframes.github.io/api/python/graphframes.html#graphframes.GraphFrame.bfs) |
Detail: [Scala doc](https://graphframes.github.io/api/scala/index.html#org.graphframes.lib.BFS)
```python
# Search from "Esther" for users of age < 32.
paths = g.bfs("name = 'Esther'", "age < 32")
paths.show()

# Specify edge filters or max path lengths.
g.bfs("name = 'Esther'", "age < 32",\
  edgeFilter="relationship != 'friend'", maxPathLength=3)
```


#### Connected components
Example: [user guide](https://graphframes.github.io/user-guide.html#connected-components) |
Syntax: [Python guide](https://graphframes.github.io/api/python/graphframes.html#graphframes.GraphFrame.connectedComponents)


#### PageRank
