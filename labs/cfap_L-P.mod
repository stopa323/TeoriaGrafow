/** Data type definitions **/
tuple Link {
  string name;
  int src_node;
  int dest_node;
  int cost;
  int capacity;
}

tuple Demand {
  string name;
  int ammount;
}

tuple Path {
  string name;
}

/** Constants **/
{Link} Links = ...;

{Demand} Demands = ...;

{Path} Paths = ...;

int delta[Links][Demands][Paths] = ...;


/** Variables **/
// throughput fulfilling demand
dvar float+ x[Demands][Paths];

// throughput assigned to link
dvar float+ y[Links];


/** Objective function **/
minimize
  sum(l in Links) (l.cost*y[l]);


/** Constraints **/
subject to {
a1:
  // On each link we must assign enough throughput to accomodate all demands on
  // this link
  forall(l in Links) {
    sum (d in Demands, p in Paths)
      (delta[l][d][p] * x[d][p]) == y[l];
  }

a2:
  // Assigned throughput must not be greater than link capacity
  forall(l in Links) {
    y[l] <= l.capacity;
  }

a3:
  // For each demand its assigned throughput must meet the required ammount
  forall(d in Demands) {
    sum(p in Paths)
      (x[d][p]) == d.ammount;
  };
}

execute {
	for(var l in Links){
		writeln("Link ", l.name, " uses ", y[l], " with ", l.capacity, " available capacity.");
	}

  writeln(x);
  writeln(y);
};
