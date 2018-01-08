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

// Days of the week classes are allowed to be given
{string} Days = ...;

// Each slot lasts 15 minutes with first starting at 8am; number of slots defines
// time span of each Day e.g.
//  12 slots: 12*15/60 = 3 [hr]
//  Classes can be given between 8 and 11 each day
range Slots = 0..3;

// Preferences of each teacher for every for every slot (1 is prefered, 0 is not)
int TeacherPreferences[Teachers][Days][Slots] = ...;


/*** Decision variables definition ***/
// Assign teachers to certain classes (1 if assigned, 0 otherwise)
dvar int+ TeacherAssignments[Teachers][Classes] in 0..1;

// Assign rooms to certain classes (1 if assigned, 0 otherwise)
dvar int+ RoomAssignments[Rooms][Classes] in 0..1;

// Assign class to certain time slot (1 if assigned, 0 otherwise)
dvar int+ ClassAssignments[Classes][Days][Slots] in 0..1;


maximize
// Take under consideration only those <t,c,d,s> tuples where teacher has expertise
// TeacherAssignments[t][c] :
//  0 if teacher t is not assigned to class c => do not take other params into account
//  1 if assigned:
//    ClassAssignments * TeacherPreferences :
//      0 if class has not been assigned to preffered slot
//      1 otherwise
sum(t in Teachers, c in Classes, d in Days, s in Slots : TeacherExpertise[t][c] == 1)
  (TeacherAssignments[t][c] * ClassAssignments[c][d][s] * TeacherPreferences[t][d][s]);

/*** Constraints ***/
subject to {
  // Teacher must be assigned to exactly 1 class
  // @TODO: replace with: cannot have several classes in the same time
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

  // Assign only as much time as it is required
  forall(c in Classes) {
    sum(d in Days, s in Slots) (ClassAssignments[c][d][s]) == c.duration;
  }

  // TODO: two classes cannot be placed in same room in the same time
  // Code below is not working
  //forall(r in Rooms, c in Classes) {
  //  sum(c2 in Classes, d in Days, s in Slots : c.name != c2.name) (abs(ClassAssignments[c][d][s] - ClassAssignments[c2][d][s])) == 0;
  //}
}


execute {
  writeln("Starting simulation...");

  writeln("TeacherAssignments[Teachers][Classes]=", TeacherAssignments);
  writeln("RoomAssignments[Rooms][Classes]=", RoomAssignments);
  writeln("ClassAssignments[Classes][Days][Slots]=", ClassAssignments);

  writeln("Yeeeeeey! Somehow it did not crash");
};
