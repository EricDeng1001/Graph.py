__Author__ = "Anitnus"

from collections import deque, Iterable
from functools import reduce

class Graph:
  def __init__( this ):
    this.__nodes = {}
    this.__negetiveEdge = 0

  def clearVertexs( this ):
    this.__nodes = {}
    this.__negetiveEdge = 0

  def clearEdges( this ):
    i = 0
    keys = list( this.__nodes.keys() )
    length = len( keys )
    while i < length:
      this.__nodes[keys[i]] = {}
      i += 1

  def addVertex( this , vertexName ):
    if type( vertexName ) is str:
      if vertexName in this.__nodes:
        return None
      this.__nodes[vertexName] = {}
    elif isinstance( vertexName , Iterable ):
      for name in vertexName:
        if type( name ) is str:
          this.__nodes[name] = {}

  def removeVertex( this , vertexName ):
    if type( vertexName ) is str:
      if vertexName not in this.__nodes:
        return None
      del this.__nodes[vertexName]
    elif isinstance( vertexName , Iterable ):
      for name in vertexName:
        if type( name ) is str:
          del this.__nodes[name]

  def addArcFromTo( this , source , destiny , weight = 1 ):
    if not source in this.__nodes:
      return source
    if not destiny in this.__nodes:
      return destiny
    this.__nodes[source][destiny] = weight
    if weight < 0:
      this.__negetiveEdge += 1

  def removeArcFromTo( this , source , destiny ):
    if source not in this.__nodes or destiny not in this.__nodes:
      return None
    if this.__nodes[source][destiny] < 0:
      this.__negetiveEdge -= 1
    del this.__nodes[source][destiny]

  def associate( this , source , destiny , weight = 1 ):
    if source not in this.__nodes or destiny not in this.__nodes:
      return None
    this.__nodes[source][destiny] = weight
    this.__nodes[destiny][source] = weight
    #print( this.__nodes )
    if weight < 0:
      this.__negetiveEdge += 2

  def unAssociate( this , source , destiny ):
    if source not in this.__nodes or destiny not in this.__nodes:
      return None
    if this.__nodes[source][destiny] < 0:
      this.__negetiveEdge -= 2
    del this.__nodes[source][destiny]
    del this.__nodes[destiny][source]
    #print( this.__nodes )

  def getAllNodes( this ):
    return list( this.__nodes )

  def getNeighbors( this , vertex ):
    if vertex not in this.__nodes:
      return []
    return list( this.__nodes[vertex] )

  def getWeight( this , source , destiny ):
    if source not in this.__nodes or destiny not in this.__nodes[source]:
      return float("inf")
    return this.__nodes[source][destiny]

  def findAPath( this , source , destiny ):
    if source not in this.__nodes and destiny not in this.__nodes:
      return None
    parent = {
      source: None
    }
    visited = []
    path = []
    end = False
    def __findAPath( vertex ):
      nonlocal end
      visited.append( vertex )
      for node in this.getNeighbors( vertex ):
        if node in visited:
          continue
        parent[node] = vertex
        if node is destiny:
          while node:
            path.insert( 0 , node )
            node = parent[node]
          end = True
          return
        __findAPath( node )
        if end:
          return

    __findAPath( source )
    return path

  def shortestPath( this , source , destiny ):
    toVisit = deque()
    visited = [source]
    parent = {
      source: None
    }
    for name in this.getNeighbors( source ):
      toVisit.append( name )
      parent[name] = source
    while toVisit:
      node = toVisit.popleft()
      visited.append( node )
      if node is destiny:
        path = []
        while node:
          path.insert( 0 , node )
          node = parent[node]
        return path
      for name in this.getNeighbors( node ):
        if name not in visited and name not in toVisit:
          toVisit.append( name )
          parent[name] = node
    return None

  def bfr( this , vertex , callback ):
    end = False
    def endRetrieve():
      end = True
    toVisit = deque()
    visited = [vertex]
    res = [callback({
      "name": vertex,
      "path": [],
      "end": endRetrieve
    })]
    parent = {
      vertex: None
    }
    for name in this.getNeighbors( vertex ):
      toVisit.append( name )
      parent[name] = vertex
    while toVisit:
      node = toVisit.popleft()
      if node in visited:
        continue
      tmp =  parent[node]
      path = []
      while tmp:
        path.insert( 0 , tmp )
        tmp = parent[tmp]
      res.append( callback({
        "name": node,
        "path": path,
        "end": endRetrieve
      }))
      if end:
        return res
      visited.append( node )
      for name in this.getNeighbors( node ):
        if name not in visited and name not in toVisit:
          toVisit.append( name )
          parent[name] = node
    return res

  def dfr( this , vertex , callback ):
    if vertex not in this.__nodes:
      return None
    end = False
    res = []
    parent = {
      vertex: None
    }
    visited = []
    def endRetrieve():
      nonlocal end
      end = True
    def __dfr( vertex ):
      visited.append( vertex )
      for node in this.getNeighbors( vertex ):
        if node in visited:
          continue
        parent[node] = vertex
        tmp =  parent[node]
        path = []
        while tmp:
          path.insert( 0 , tmp )
          tmp = parent[tmp]
        res.append(callback({
          "name": node,
          "path": path,
          "end": endRetrieve
        }))
        if end:
          return
        __dfr( node )
        if end:
          return
    __dfr( vertex )
    return res

  def __dijkstra( this , source , destiny ):
    inf = float("inf")
    if destiny not in this.__nodes or source not in this.__nodes:
      return None , inf
    def getLowestCost():
      r = inf
      res = ""
      for node in toVisit:
        if cost[node] < r:
          res = node
          r = cost[node]
      return res
    cost = {}
    parent = {}
    visited = []
    toVisit = [source]
    for node in this.getAllNodes():
      cost[node] = inf
      parent[node] = None
    cost[source] = 0
    while toVisit:
      nodeNow = getLowestCost()
      toVisit.remove( nodeNow )
      visited.append( nodeNow )
      for node in this.getNeighbors( nodeNow ):
        if node in visited:
          continue
        toVisit.append( node )
        newCost = cost[nodeNow] + this.getWeight( nodeNow , node )
        if  newCost < cost[node]:
          cost[node] = newCost
          parent[node] = nodeNow
    node = destiny
    path = []
    while node:
      path.insert( 0 , node )
      node = parent[node]
    return path , cost[destiny]

  def __BellmanFord( this , source , destiny ):
    inf = float("inf")
    if destiny not in this.__nodes or source not in this.__nodes:
      return None , inf
    parent = {}
    cost = {}
    for node in this.getAllNodes():
      cost[node] = inf
      parent[node] = None
    cost[source] = 0
    for i in range( len ( this.getAllNodes() ) - 1 ):
      for node in this.getAllNodes():
        for neighbor in this.getNeighbors( node ):
          newCost = cost[node] + this.getWeight( node , neighbor )
          if cost[neighbor] > newCost:
            cost[neighbor] = newCost
            parent[neighbor] = node
    for node in this.getAllNodes():
      for neighbor in this.getNeighbors( node ):
        newCost = cost[neighbor] + this.getWeight( neighbor , node )
        if cost[node] > newCost:
          raise Exception("A negetive cycle exists")
    path = []
    node = destiny
    while node:
      path.insert( 0 , node )
      node = parent[node]
    return path , cost[destiny]

  def lowestCostPath( this , source , destiny ):
    if not this.__negetiveEdge:
      path , cost = this.__dijkstra( source , destiny )
    else:
      path , cost = this.__BellmanFord( source , destiny )
    if cost == float("inf"):
      return None , float("inf")
    return path , cost

if __name__ == "__main__":
  test = Graph()
  test.addVertex([ "vertex1" , "vertex2" , "vertex3" , "vertex4" , "vertex5" ])

  """

        1 ------------ 2 ---------4
        |                     /                  /
        |                /                    /
        |             /                    /
        |         /                     /
        |    /                       /
        3-------------5

  """

  test.associate( "vertex1" , "vertex2" )
  test.associate( "vertex1" , "vertex3" )
  test.associate( "vertex2" , "vertex4" )
  test.associate( "vertex3" , "vertex5" )
  test.associate( "vertex3" , "vertex2" )
  test.associate( "vertex5" , "vertex4" )

  #test.bfr( "vertex1" , lambda arg: print( reduce( lambda p , n : p + "->" + n , arg["path"] , "o" ) , "->" , arg["name"] ) )
  #test.dfr( "vertex1" , lambda arg: print( reduce( lambda p , n : p + "->" + n , arg["path"] , "o" ) , "->" , arg["name"] ) )

  path = test.shortestPath( "vertex1" , "vertex5" )
  print( path )
  path = test.findAPath( "vertex1" , "vertex5" )
  print( path )
  path = test.shortestPath( "vertex2" , "vertex5" )
  print( path )
  test.associate( "vertex2" , "vertex5" )
  path = test.shortestPath( "vertex2" , "vertex5" )
  print( path )
  test.unAssociate( "vertex2" , "vertex5" )
  path = test.shortestPath( "vertex2" , "vertex5" )
  print( path )
  path , cost = test.lowestCostPath( "vertex1" , "vertex5" )
  print( path , cost )

  test.clearEdges()

  test.associate( "vertex1" , "vertex2" , 3 )
  test.associate( "vertex1" , "vertex3" , 4.02 )
  test.associate( "vertex2" , "vertex4" , 0.5 )
  test.associate( "vertex3" , "vertex5" , 16.33 )
  test.associate( "vertex3" , "vertex2" , 1.01 )
  test.associate( "vertex5" , "vertex4" , 9 )

  path = test.shortestPath( "vertex1" , "vertex5" )
  print( path )
  path , cost = test.lowestCostPath( "vertex1" , "vertex5" )
  print( path , cost )

  path , cost = test.lowestCostPath( "vertex5" , "vertex1" )
  print( path , cost )

  test.clearEdges()

  test.associate( "vertex1" , "vertex2" , 3 )
  test.associate( "vertex1" , "vertex3" , 4.02 )
  test.addArcFromTo( "vertex4" , "vertex2" , 0.5 )
  test.associate( "vertex3" , "vertex5" , 16.33 )
  test.associate( "vertex3" , "vertex2" , 1.01 )
  test.associate( "vertex5" , "vertex4" , 9 )

  path , cost = test.lowestCostPath( "vertex1" , "vertex5" )
  print( path , cost )

  path , cost = test.lowestCostPath( "vertex5" , "vertex1" )
  print( path , cost )

  test.clearEdges()

  test.addArcFromTo( "vertex1" , "vertex2" , -4 )
  test.addArcFromTo( "vertex1" , "vertex3" , 4.02 )
  test.addArcFromTo( "vertex4" , "vertex2" , 0.5 )
  test.associate( "vertex3" , "vertex5" , 16.33 )
  test.associate( "vertex3" , "vertex2" , 1.01 )
  test.associate( "vertex5" , "vertex4" , 9 )

  path , cost = test.lowestCostPath( "vertex1" , "vertex5" )
  print( path , cost )

  path , cost = test.lowestCostPath( "vertex5" , "vertex1" )
  print( path , cost )

  path , cost = test.lowestCostPath( "v2" , "x1" )
  print( path , cost )
