import numpy as np
import structures


# Scenario 2 => class 11 is removed from t5's expertise

# Scenario 3 => remove has_swim_pool flag from room 6 => alg error no solution


def load_classes():
    # Scenario 1
    c1 = structures.Class(1, "Class1", 3, 15)
    c2 = structures.Class(2, "Class2", 3, 15)
    c3 = structures.Class(3, "Class3", 3, 15)
    c4 = structures.Class(4, "Class4", 3, 15)
    c5 = structures.Class(5, "Class5", 6, 60)
    c6 = structures.Class(6, "Class6", 6, 60)
    c7 = structures.Class(7, "Class7", 6, 60)
    c8 = structures.Class(8, "Class8", 8, 100)
    c9 = structures.Class(9, "Class9", 6, 60)
    c10 = structures.Class(10, "Class10", 3, 15)
    c11 = structures.Class(11, "Class11", 12, 60, True, False, False)
    return {c1.id: c1,
            c2.id: c2,
            c3.id: c3,
            c4.id: c4,
            c5.id: c5,
            c6.id: c6,
            c7.id: c7,
            c8.id: c8,
            c9.id: c9,
            c10.id: c10,
            c11.id: c11}


def load_rooms():
    # Scenario 1
    r1 = structures.Room(1, "Room1", 15, False, True, False)
    r2 = structures.Room(2, "Room2", 15, False, True, True)
    r3 = structures.Room(3, "Room3", 15, False, True, True)
    r4 = structures.Room(4, "Room4", 60, False, False, True)
    r5 = structures.Room(5, "Room5", 100, False, False, True)
    r6 = structures.Room(6, "Room6", 60, True, False, False)
    return {r1.id: r1,
            r2.id: r2,
            r3.id: r3,
            r4.id: r4,
            r5.id: r5,
            r6.id: r6}


def load_teachers():
    # Scenario 1
    # t1 prefers early hours
    # t2 prefers late
    # t3 no pref
    # t4 middle of the dat
    # t5 needs 3-slots break after class
    #
    # t1 takes c1, c2 in early, c11 though he can is assigned to t5 to maximize objective
    # t2 takes only 5 in late
    # t3 has no pref thus takes 3 and 6 which could be also assigned to t2
    # t4 takes 8 9 10 cuz he's the only available
    # t5 takes 7 cuz he's only available + 11 for obj maximization
    t1 = structures.Teacher(
        1, "Teacher_1",
        np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                  1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]),
        set([1, 2, 11]), 1, 1, 1)
    t2 = structures.Teacher(
        2, "Teacher_2",
        np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
                  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]),
        set([3, 5, 6]), 1, 1, 1)
    t3 = structures.Teacher(
        3, "Teacher_3",
        np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
                  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]),
        set([3, 4, 6, 7]), 1, 1, 1)
    t4 = structures.Teacher(
        4, "Teacher_4",
        np.array([0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1.,
                  1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.]),
        set([8, 9, 10]), 1, 1, 1)
    t5 = structures.Teacher(
        5, "WFista",
        np.array([0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1.,
                  0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1.]),
        set([7, 11]), 1, 1, 3)
    return {t1.id: t1,
            t2.id: t2,
            t3.id: t3,
            t4.id: t4,
            t5.id: t5}
