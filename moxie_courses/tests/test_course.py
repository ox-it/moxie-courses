import unittest
from datetime import datetime

from moxie_courses.course import Course, Presentation


class CourseTestCase(unittest.TestCase):

    def test_course_object(self):
        c1 = Course("c1_id")
        c1.presentations.append(Presentation("p_id_1", c1))
        c1.presentations.append(Presentation("p_id_2", c1))
        self.assertEqual(len(c1.presentations), 2)

        c2 = Course("c2_id")
        c2.presentations.append(Presentation("p_id_3", c2))
        self.assertEqual(len(c2.presentations), 1)

    def test_presentation_bookable(self):
        start = datetime(2012, 12, 01)
        end = datetime(2012, 12, 15)
        course = Course("c")
        p1 = Presentation("p1", course, apply_from=start, apply_until=end, date_apply=datetime(2012, 12, 10), booking_endpoint="http://fake-endpoint.com")
        p2 = Presentation("p2", course, apply_from=start, apply_until=end, date_apply=datetime(2012, 11, 30))
        p3 = Presentation("p3", course)     # no apply info, shouldn't be bookable
        p4 = Presentation("p1", course, apply_from=start, apply_until=end, date_apply=datetime(2012, 12, 10))   # no booking endpoint, shouldn't be bookable
        self.assertEqual(p1.bookable, True)
        self.assertEqual(p2.bookable, False)
        self.assertEqual(p3.bookable, False)
        self.assertEqual(p4.bookable, False)