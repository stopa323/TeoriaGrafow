
/*** Data type definitions ***/
tuple teacher {
  key string name;
}

tuple class {
  key string name;
  int duration;
}

/*** Constants definitions ***/
{teacher} Teachers = ...;
{class} Classes = ...;

// For each teacher, define which classes (s)he is able to give (1 if able, 0 otherwise)
int TeacherExpertise[Teachers][Classes] = ...;

/*** Decision variables definition ***/
// Assign teachers to certain classes (1 if assigned, 0 otherwise)
dvar int+ TeacherAssignments[Teachers][Classes] in 0..1;

maximize
  sum(t in Teachers, c in Classes) (TeacherAssignments[t][c]);

subject to {
  // Teacher must be assigned to exactly 1 class
  forall(t in Teachers) {
    sum(c in Classes) (TeacherAssignments[t][c]) == 1;
  }

  // Teacher must not be assigned to class (s)he cannot give
  forall(t in Teachers, c in Classes : TeacherExpertise[t][c] == 0) {
    TeacherAssignments[t][c] == 0;
  }

  // Each class must have teacher assigned
  forall(c in Classes) {
    sum(t in Teachers) (TeacherAssignments[t][c]) >= 1;
  }
}

execute {
  writeln("Starting simulation...");

  writeln("Teachers=", Teachers);
  writeln("Courses=", Classes);
  writeln("TeacherExpertise=", TeacherAssignments);

  writeln("Yeeeeeey! Somehow it did not crash");
};
