import logging
import numpy as np
import fixtures

# logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class SmartAss(object):

    NUMBER_OF_SLOTS = 24

    def __init__(self):
        self._classes = fixtures.load_classes()
        self._teachers = fixtures.load_teachers()
        self._rooms = fixtures.load_rooms()
        self.schedule = []

    def build_priority_queue(self):
        for c in self._classes.values():
            LOG.debug("Class: %s" % c)
            c.assign_available_rooms(self._rooms.values())
            c.assign_avail_teachers(self._teachers.values())

    def sort_queue(self):
        W1 = 0.6
        W2 = 0.4

        for c in self._classes.values():
            x1 = c.get_avail_teachers_count() / self._get_max_assigned_teachers_count()
            x2 = c.get_avail_rooms_count() / self._get_max_assigned_rooms_count()

            c.sort_score = 1 - (W1 * x1 + W2 * x2)

        sorted_classes = sorted(self._classes.values(), key=lambda x: x.sort_score)
        self._classes = {x.id: x for x in sorted_classes}

        for c in self._classes.values():
            LOG.debug("%s: %s" % (c.id, c.sort_score))

    def fit(self, cls):
        best_matches = {}
        for t in cls._avail_teachers:
            teacher = self._teachers[t.id]
            pref = teacher.get_preference()

            # Transform sth like this: [1,1]
            # to sth like this:
            # 1 0 0 0
            # 1 1 0 0
            # 0 1 1 0
            # 0 0 1 1
            x = np.zeros(self.NUMBER_OF_SLOTS)
            x[0:cls.duration] = 1
            H = np.tril(np.transpose(np.array([np.roll(x, i) for i in range(self.NUMBER_OF_SLOTS)])))
            H[len(x)-1, len(x)-1] = 0  # wyzerowanie 'wystającej' jedynki w ostatniej kolumnie
            Y = np.diag(pref) * np.diag(cls.reserv_mtx) * H

            LOG.debug(Y)
            # Zsumuj kolumny
            # print("suma", np.sum(Y, axis=0))
            # best_matches[t.id] = max(np.sum(Y, axis=0))
            best_preference = max(np.sum(Y, axis=0))
            best_column = np.argmax(np.sum(Y, axis=0))
            best_matches[t.id] = [best_preference, H[:, best_column]]

        best_teacher = max(best_matches)
        # print("best_teacher", best_teacher)

        self.refresh_all_mtx_with_infinitives(best_matches, best_teacher, cls)
        self.refresh_max_classes_mtx(best_teacher)
        self.refresh_min_break(best_teacher)
        self.refresh_max_break(best_teacher)

        # print("***MIN_BREAK***", self._teachers[best_teacher].min_break_mtx)
        # print("***MAX_BREAK***", self._teachers[best_teacher].max_break_mtx)
        # print("***PREF***", self._teachers[best_teacher].pref_mtx)
        # print("***MAX_CLASSES***", self._teachers[best_teacher].max_class_mtx)

    def refresh_max_break(self, best_teacher):
        i = 0
        while i < len(self._teachers[best_teacher].max_break_mtx):
            if self._teachers[best_teacher].max_break_mtx[i] != -np.inf:
                if -np.inf in self._teachers[best_teacher].max_break_mtx[
                              i - self._teachers[best_teacher].max_break:i + self._teachers[best_teacher].max_break]:
                    self._teachers[best_teacher].max_break_mtx[i] = 1
                else:
                    self._teachers[best_teacher].max_break_mtx[i] = 0
            i += 1

    def refresh_min_break(self, best_teacher):
        i = 0
        while i < len(self._teachers[best_teacher].min_break_mtx):
            if self._teachers[best_teacher].min_break_mtx[i] != -np.inf:
                if -np.inf in self._teachers[best_teacher].min_break_mtx[
                              i - self._teachers[best_teacher].min_break: i + self._teachers[best_teacher].min_break]:
                    self._teachers[best_teacher].min_break_mtx[i] = 0
                else:
                    self._teachers[best_teacher].min_break_mtx[i] = 1
            i += 1

    def refresh_max_classes_mtx(self, best_teacher):
        class_counter = 0
        i = 0
        while i < len(self._teachers[best_teacher].max_class_mtx):
            if self._teachers[best_teacher].max_class_mtx[i] == -np.inf:
                class_counter += 1
            else:
                if class_counter >= self._teachers[best_teacher].max_classes:
                    self._teachers[best_teacher].max_class_mtx[i] = 0
                class_counter = 0
            i += 1

    def refresh_all_mtx_with_infinitives(self, best_matches, best_teacher, cls):
        i = 0
        while i < len(best_matches[best_teacher][1]):
            if best_matches[best_teacher][1][i] == 1.:
                self._teachers[best_teacher].pref_mtx[i] = -np.inf
                self._teachers[best_teacher].min_break_mtx[i] = -np.inf
                self._teachers[best_teacher].max_break_mtx[i] = -np.inf
                self._teachers[best_teacher].max_class_mtx[i] = -np.inf
                self._teachers[best_teacher].schedule[i] = cls.name
            i += 1

    def _get_max_assigned_teachers_count(self):
        return max([c.get_avail_teachers_count() for c in self._classes.values()])

    def _get_max_assigned_rooms_count(self):
        return max([c.get_avail_rooms_count() for c in self._classes.values()])


def main():
    obj = SmartAss()

    # TODO(jarek): flow powinien byc taki:

    # - build queue
    # - while queue not empty
    #   - sort queue
    #   - x = pop
    #   - fit(x)
    obj.build_priority_queue()
    counter = 1
    while len(obj._classes) != 0:
        obj.sort_queue()
        obj.fit(obj._classes[counter])
        del obj._classes[counter]
        counter += 1

    for teacher in obj._teachers.values():
        print(teacher.schedule)


if __name__ == '__main__':
    main()
