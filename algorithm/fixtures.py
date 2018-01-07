import numpy as np
import structures


def load_classes():
    c1 = structures.Class(1, "Algebra", 2, 30)
    c2 = structures.Class(2, "Algebra2", 2, 30)
    c3 = structures.Class(3, "Telecomunication", 2, 60)
    c4 = structures.Class(4, "Swimming", 2, 60, False, False, True)
    return {c1.id: c1, c2.id: c2, c3.id: c3, c4.id: c4}


def load_rooms():
    r1 = structures.Room(1, "D5/120", 30)
    r2 = structures.Room(2, "D5/500", 60)
    r3 = structures.Room(3, "Swimming Pool", 60, False, False, True)
    return {r1.id: r1, r2.id: r2, r3.id: r3}


def load_teachers():
    t1 = structures.Teacher(1, "Hulio", np.array([1., 1., 0., 0., 0., 0.]), set([3]), 2, 3, 1)
    t2 = structures.Teacher(2, "Adamus", np.array([1., 0., -np.inf, 1., 1., 1.]), set([1, 2]), 2, 3, 1)
    t3 = structures.Teacher(3, "Adamus Jr", np.array([0., 1., 1., 1., 1., 0.]), set([1, 2]), 2, 3, 1)
    t4 = structures.Teacher(4, "WFista", np.array([1., 1., 1., 0., 1., 0.]), set([4]), 2, 3, 1)
    return {t1.id: t1, t2.id: t2, t3.id: t3, t4.id: t4}
