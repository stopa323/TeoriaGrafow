import logging
import numpy as np

LOG = logging.getLogger(__name__)


class BaseResource(object):
    
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "[%s]_%s" % (self.id, self.name)


class Teacher(BaseResource):
    W1 = 0.6
    W2 = 0.2
    W3 = 0.1
    W4 = 0.1
    NUMBER_OF_SLOTS = 6


    def __init__(self, id, name, preferences, expertise, max_classes, max_break, min_break):
        super(Teacher, self).__init__(id, name)
        self.expertise = expertise
        self.pref_mtx = preferences
        self.max_class_mtx = np.ones(preferences.shape)
        self.max_break_mtx = np.ones(preferences.shape)
        self.min_break_mtx = np.ones(preferences.shape)
        self.schedule = ["" for x in range(self.NUMBER_OF_SLOTS)]

        self.max_classes = max_classes
        self.max_break = max_break
        self.min_break = min_break

    def get_preference(self):
        pref = self.W1 * self.pref_mtx + \
               self.W2 * self.max_class_mtx + \
               self.W3 * self.max_break_mtx + \
               self.W4 * self.min_break_mtx
        return pref


class Class(BaseResource):

    NUMBER_OF_SLOTS = 6

    def __init__(self, id, name, duration, req_seats, req_table=False,
                 req_comp=False, req_swim_pool=False):
        super(Class, self).__init__(id, name)
        self.duration = duration
        self.req_seats = req_seats
        self.req_table = req_table
        self.req_comp = req_comp
        self.req_swim_pool = req_swim_pool

        self.reserv_mtx = np.ones(self.NUMBER_OF_SLOTS)

        self._avail_rooms = list()
        self._avail_teachers = list()

        self.sort_score = 0

    def assign_available_rooms(self, rooms):
        def is_room_suitable(room):
            if room.seats < self.req_seats:
                return False
            if self.req_table and not room.has_table:
                return False
            if self.req_comp and not room.has_comp:
                return False
            if self.req_swim_pool and not room.has_swim_pool:
                return False
            return True

        rooms_filtered = list(filter(lambda x: is_room_suitable(x), rooms))
        self._avail_rooms = sorted(rooms_filtered,
                                   key=lambda x: self.req_seats / x.seats,
                                   reverse=True)

    def assign_avail_teachers(self, teachers):
        teachers_filtered = list(filter(lambda x: self.id in x.expertise,
                                        teachers))
        self._avail_teachers = teachers_filtered

    def print_avail_rooms(self):
        for r in self._avail_rooms:
            LOG.debug(r)

    def print_avail_teachers(self):
        for t in self._avail_teachers:
            LOG.debug(t)

    def get_avail_teachers_count(self):
        return len(self._avail_teachers)

    def get_avail_rooms_count(self):
        return len(self._avail_rooms)


class Room(BaseResource):
    
    def __init__(self, id, name, seats, has_table=False, has_comp=False,
                 has_swim_pool=False):
        super(Room, self).__init__(id, name)
        self.seats = seats
        self.has_table = has_table
        self.has_comp = has_comp
        self.has_swim_pool = has_swim_pool
