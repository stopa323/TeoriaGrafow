/* Topology:
                 +-----+
       +-------> |Node2+-----------+
       |   10    +-----+     30    |
       |                           |
       |                           |
    +--+--+                     +--v--+
    |Node1|                     |Node4|
    +--+--+                     +--^--+
       |                           |
       |                           |
       |   20    +-----+     40    |
       +-------> |Node3+-----------+
                 +-----+
*/


tuple Edge {
  string name;
}

tuple Node {
  int id;
}

tuple Demand {
  float ammount;
}

{Edge} Edges = ...;
{Node} Nodes = ...;
{Demand} Demands = ...;

// Cost of single unit of throughput on link
int cost[Edges] = ...;

// id of source node for demand d
int source[Demands] = ...;

// id of destination node for demand d
int dest[Demands] = ...;

// a[e][v] = 1 if edge `e` starts in node `v`
int a[Edges][Nodes] = ...;

// b[e][v] = 1 if edge `e` ends in node `v`
int b[Edges][Nodes] = ...;


// Value of the flow realising demand `d` on edge `e`
dvar float+ x[Edges][Demands];

// Value of the throughput assigned to edge `e`
dvar float+ y[Edges];


minimize
  sum(e in Edges)
    (cost[e]*y[e]);


subject to {
  // if node is source node for demand `d`:
  // sum of all its outgoing flows minus sum of its ingoing flows must equal
  // total demand `d`
  forall(d in Demands, v in Nodes : v.id == source[d]) {
    (sum(e in Edges) (a[e][v]*x[e][d])) - (sum(e in Edges) (b[e][v]*x[e][d])) == d.ammount;
  };

  // if node is not source node nor dest node for demand `d`:
  // sum of all its outgoing flows minus sum of its ingoing flows must equal zero
  forall(d in Demands, v in Nodes : v.id != source[d] && v.id != dest[d]) {
    sum(e in Edges) (a[e][v]*x[e][d]) - sum(e in Edges) (b[e][v]*x[e][d]) == 0;
  };

  // if node is dest node for demand `d`:
  // sum of all its outgoing flows minus sum of its ingoing flows must equal
  // minus total demand `d`
  forall(d in Demands, v in Nodes : v.id == dest[d]) {
    sum(e in Edges) (a[e][v]*x[e][d]) - sum(e in Edges) (b[e][v]*x[e][d]) == -d.ammount;
  };

  // On each link e, sum of requested flows must be equal to assigned throughput
  forall(e in Edges) {
    sum(d in Demands) (x[e][d]) == y[e];
  };
};

execute {

  for(var e in Edges){
    writeln("Link ", e.name, " uses ", y[e], " throughput.");
  }

}
