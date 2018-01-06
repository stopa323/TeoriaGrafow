import numpy as np


TEACHERS = ['Hulio', 'Adamus', 'Adamus Jr']

CLASSES = ['Algebra', 'Algebra2', 'Telekomunikacja']

ROOMS = ['D5/120', 'D5/500']

DAYS = 1

SLOTS = 4

with open('results.dat') as f:
    results = f.read().replace('\n', '')

    i = results.find('[[')
    i2 = results.find(']]', i)

    teacher_assignments = results[i+1:i2+1]

    i = results.find('[[', i2)
    i2 = results.find(']]', i)

    room_assignments = results[i+1:i2+1]

    i = results.find('[[[', i2)
    i2 = results.find(']]]', i)

    class_assignments = results[i+1:i2+2]

    # Convert teacher assignments to convinient format
    i2 = 0
    ta = list()
    while True:
        i = teacher_assignments.find('[', i2)
        i2 = teacher_assignments.find(']', i)

        if i < 0 or i2 < 0:
            break

        tmp = teacher_assignments[i+1:i2].split()
        tmp = list(map(int, tmp))
        ta.append(tmp)

    # Convert room assignments to convinient format
    i2 = 0
    ra = list()
    while True:
        i = room_assignments.find('[', i2)
        i2 = room_assignments.find(']', i)

        if i < 0 or i2 < 0:
            break

        tmp = room_assignments[i+1:i2].split()
        tmp = list(map(int, tmp))
        ra.append(tmp)

    # Convert class assignments to convinient format
    i2 = 0
    ca = list()
    while True:
        i = class_assignments.find('[[', i2)
        i2 = class_assignments.find(']]', i)

        if i < 0 or i2 < 0:
            break

        tmp = class_assignments[i+1:i2+1]

        days = list()
        j2 = 0
        while True:
            j = tmp.find('[', j2)
            j2 = tmp.find(']', j)

            if j < 0 or j2 < 0:
                break

            tmp2 = tmp[j+1:j2].split()
            tmp2 = list(map(int, tmp2))
            days.append(tmp2)

        ca.append(days)

    # print ta
    # print ra
    # print ca

    # For each teacher
    for teacher_id in range(len(ta)):
        class_timetable = np.ones((1, 4)) * np.inf
        room_timetable = np.ones((1, 4)) * np.inf
        for class_id in range(len(ta[teacher_id])):
            if ta[teacher_id][class_id]:
                room_id = None
                for i in range(len(ROOMS)):
                    if ra[i][class_id]:
                        room_id = i
                        break
                for day in range(DAYS):
                    for slot in range(SLOTS):
                        if ca[class_id][day][slot]:
                            class_timetable[day][slot] = class_id
                            room_timetable[day][slot] = room_id
        timetable = list()
        for d in range(DAYS):
            tmp = list()
            for s in range(SLOTS):
                if class_timetable[d][s] != np.inf:
                    cls = CLASSES[int(class_timetable[d][s])]
                    room = ROOMS[int(room_timetable[d][s])]
                    tmp.append((cls, room))
                else:
                    tmp.append('-')
            timetable.append(tmp)
        print(timetable)
        print("============")
