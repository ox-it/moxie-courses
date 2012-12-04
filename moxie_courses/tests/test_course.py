import unittest

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