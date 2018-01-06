/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Asia
 * Creation Date: 1 sty 2018 at 20:22:23
 *********************************************/
/**
# Helpful links:
  https://www.ibm.com/support/knowledgecenter/SSSA5P_12.4.0/ilog.odms.ide.help/examples/html/opl/nurses/nurses.mod.html
  https://www.ibm.com/support/knowledgecenter/SSSA5P_12.4.0/ilog.odms.ide.help/examples/html/opl/nurses/nurses.dat.html
  http://sal.aalto.fi/publications/pdf-files/esan12_public.pdf
# TODOs:
  * Objective function:
    - add students preferences (optional)
  * Constraints:
    - class has to be assigned to continuous set of slots, situation when 30 min
      class is split into two slots e.g. 8:30-8:45, 10:00-10:15 is forbidden
    - only one class can be assigned to the room in a given time -  DONE
    - only one class can be assigned to the teacher in a given time - DONE
    - table, computer, swimming pool requirements - DONE
  * Constraints or obj function, not sure, but obj func most likely:
    - min/max break for the teacher (optional)
    - max class slots in row for the teacher (optional)
**/


/*** Data type definitions ***/
tuple teacher {
  key string name;              // name of the teacher
}

tuple class {
  key string name;              // name of the class
  int duration;                 // duration (time slots) of the class
  int req_seets;                // required seets for the class
  int req_table;                // table is required for that class
  int req_comp;                 // computers are required for that class
  int req_swim_pool;            // swimming pool is required for that class
}

tuple room {
  key string address;           // address of the room (e.g. "D5/125")
  int seets;                    // available seets in the room
  int has_table;                // room has table
  int has_comp;                 // room has computers
  int has_swim_pool;            // room has swimming pool
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


/*** Objective function ***/
maximize
// Take under consideration only those <t,c,d,s> tuples where teacher has expertise
// TeacherAssignments[t][c] :
//  0 if teacher t is not assigned to class c => do not take other params into account
//  1 if assigned:
//    ClassAssignments * TeacherPreferences :
//      0 if class has not been assigned to preffered slot
//      1 otherwise
sum(t in Teachers, c in Classes, d in Days, s in Slots : TeacherExpertise[t][c] == 1)
  ( TeacherAssignments[t][c] + ClassAssignments[c][d][s] + TeacherPreferences[t][d][s]);

/*** Constraints ***/
subject to {
  // Teacher cannot have several classes in the same time
  forall(t in Teachers, d in Days, s in Slots, c in Classes, c2 in Classes: c.name != c2.name) {
  a1:
    TeacherAssignments[t][c] + TeacherAssignments[t][c2] + ClassAssignments[c][d][s] + ClassAssignments[c2][d][s] <= 3;
  }

  // Teacher must not be assigned to class (s)he cannot give
  forall(t in Teachers, c in Classes : TeacherExpertise[t][c] == 0) {
  a2:
    TeacherAssignments[t][c] == 0;
  }

  // Each class must have teacher assigned
  forall(c in Classes) {
  a3:
    sum(t in Teachers) (TeacherAssignments[t][c]) >= 1;
  }

  // Each class must have exactly 1 room assigned
  forall(c in Classes) {
  a4:
    sum(r in Rooms) (RoomAssignments[r][c]) == 1;
  }

  // Each class must have exactly 1 teacher assigned
  forall(c in Classes) {
  a100:
    sum(t in Teachers) (TeacherAssignments[t][c]) == 1;
  }

  // Assigned room must have enough seets
  // @TODO(optional): prefer rooms with just enough seets
  forall(c in Classes, r in Rooms : c.req_seets > r.seets) {
  a5:
    RoomAssignments[r][c] == 0;
  }

  // Assign only as much time as it is required
  forall(c in Classes) {
  a6:
    sum(d in Days, s in Slots) (ClassAssignments[c][d][s]) == c.duration;
  }

  // Two classes cannot be placed in same room in the same time
  forall(r in Rooms, c in Classes, d in Days, s in Slots, c2 in Classes: c.name != c2.name ) {
  a7:
    ClassAssignments[c][d][s] + ClassAssignments[c2][d][s] + RoomAssignments[r][c] + RoomAssignments[r][c2] <= 3;
  }

  //table requirement
  forall(c in Classes, r in Rooms: c.req_table == 1 && r.has_table == 0) {
  a8:
    RoomAssignments[r][c] == 0;
  }

  //computer requirement
  forall(c in Classes, r in Rooms: c.req_comp == 1 && r.has_comp == 0) {
  a9:
    RoomAssignments[r][c] == 0;
  }

  //swimming pool requirement
  forall(c in Classes, r in Rooms: c.req_swim_pool == 1 && r.has_swim_pool == 0) {
  a10:
    RoomAssignments[r][c] == 0;
  }

}


execute {
  writeln("Starting simulation...");

  writeln("TeacherAssignments[Teachers][Classes]=", TeacherAssignments);
  writeln("RoomAssignments[Rooms][Classes]=", RoomAssignments);
  writeln("ClassAssignments[Classes][Days][Slots]=", ClassAssignments);

  writeln("Yeeeeeey! Somehow it did not crash");
};
