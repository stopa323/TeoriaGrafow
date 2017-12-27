/*** Data type definitions ***/
tuple teacher {
  key string name;                  // name of the teacher
}

tuple class {
  key string name;                  // name of the class
  int duration;                     // duration (time slots) of the class
  int req_seets;                    // required seets for the class
}

tuple room {
  key string address;               // address of the room (e.g. "D5/125")
  int seets;                        // available seets in the room
}


/*** Constants definitions ***/
{teacher} Teachers = ...;
{class} Classes = ...;
{room} Rooms = ...;

// For each teacher, define which classes (s)he is able to give (1 if able, 0 otherwise)
int TeacherExpertise[Teachers][Classes] = ...;


/*** Decision variables definition ***/
// Assign teachers to certain classes (1 if assigned, 0 otherwise)
dvar int+ TeacherAssignments[Teachers][Classes] in 0..1;

// Assign rooms to certain classes (1 if assigned, 0 otherwise)
dvar int+ RoomAssignments[Rooms][Classes] in 0..1;


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

  // Each class must have exactly 1 room assigned
  forall(c in Classes) {
    sum(r in Rooms) (RoomAssignments[r][c]) == 1;
  }

  // Assigned room must have enough seets
  // @TODO(optional): prefer rooms with just enough seets
  forall(c in Classes, r in Rooms : c.req_seets > r.seets) {
    RoomAssignments[r][c] == 0;
  }
}


execute {
  writeln("Starting simulation...");

  writeln("TeacherExpertise=", TeacherAssignments);
  writeln("RoomAssignments=", RoomAssignments);

  writeln("Yeeeeeey! Somehow it did not crash");
};
