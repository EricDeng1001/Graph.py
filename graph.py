__Author__ = "Anitnus"

from collections import deque
from functools import reduce

class Graph:
  def __init__( this ):
    this.__nodes = {}
    this.__ableToDijkstra = True

  def clearVertexs( this ):
    this.__nodes = {}
    this.__ableToDijkstra = True

  def clearEdges( this ):
    i = 0
    keys = list( this.__nodes.keys() )
    length = len( keys )
    while i < length:
      this.__nodes[keys[i]] = {}
      i += 1

  def addVertex( this , vertexName ):
    if vertexName in this.__nodes:
      return None
    this.__nodes[vertexName] = {}

  def removeVertex( this , vertexName ):
    if vertexName not in this.__nodes:
      return None
    del this.__nodes[vertexName]

  def addArcFromTo( this , vertex1 , vertex2 , weight = 1 ):
    if not vertex1 in this.__nodes:
      return vertex1
    if not vertex2 in this.__nodes:
      return vertex2
    this.__nodes[vertex1][vertex2] = weight
    if weight < 0:
      this.__ableToDijkstra = False

  def removeArcFromTo( this , vertex1 , vertex2 ):
    if vertex1 not in this.__nodes or vertex2 not in this.__nodes:
      return None
    del this.__nodes[vertex1][vertex2]

  def associate( this , vertex1 , vertex2 , weight = 1 ):
    if vertex1 not in this.__nodes or vertex2 not in this.__nodes:
      return None
    this.__nodes[vertex1][vertex2] = weight
    this.__nodes[vertex2][vertex1] = weight
    #print( this.__nodes )
    if weight < 0:
      this.__ableToDijkstra = False

  def unAssociate( this , vertex1 , vertex2 ):
    if vertex1 not in this.__nodes or vertex2 not in this.__nodes:
      return None
    del this.__nodes[vertex1][vertex2]
    del this.__nodes[vertex2][vertex1]
    #print( this.__nodes )

  def getAllNodes( this ):
    return list( this.__nodes )

  def getNeighbors( this , vertex ):
    if vertex not in this.__nodes:
      return []
    return list( this.__nodes[vertex] )

  def getWeight( this , vertex1 , vertex2 ):
    return this.__nodes[vertex1][vertex2]

  def findAPath( this , vertex1 , vertex2 ):
    if vertex1 not in this.__nodes and vertex2 not in this.__nodes:
      return None
    parent = {
      vertex1: None
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
        if node is vertex2:
          while node:
            path.insert( 0 , node )
            node = parent[node]
          end = True
          return
        __findAPath( node )
        if end:
          return

    __findAPath( vertex1 )
    return path

  def shortestPath( this , vertex1 , vertex2 ):
    toVisit = deque()
    visited = [vertex1]
    parent = {
      vertex1: None
    }
    for name in this.getNeighbors( vertex1 ):
      toVisit.append( name )
      parent[name] = vertex1
    while toVisit:
      node = toVisit.popleft()
      visited.append( node )
      if node is vertex2:
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

  def __dijkstra( this , vertex1 , vertex2 ):
    def getLowestCost():
      r = inf
      res = ""
      for node in toVisit:
        if cost[node] < r:
          res = node
          r = cost[node]
      return res
    
    inf = float("inf")
    cost = {}
    parent = {
      vertex1: None
    }
    visited = []
    toVisit = [vertex1]
    for node in this.getAllNodes():
      cost[node] = inf
    cost[vertex1] = 0
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
    node = vertex2
    theCost = cost[node]
    path = []
    while node:
      path.insert( 0 , node )
      node = parent[node]
    return path , theCost

  def lowestCostPath( this , vertex1 , vertex2 ):
    if this.__ableToDijkstra:
      return this.__dijkstra( vertex1 , vertex2 )
    else:
      return None

if __name__ == "__main__":
  test = Graph()
  test.addVertex( "vertex1" )
  test.addVertex( "vertex2" )
  test.addVertex( "vertex3" )
  test.addVertex( "vertex4" )
  test.addVertex( "vertex5" )

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
