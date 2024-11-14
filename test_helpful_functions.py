import unittest
from math import isclose
import helpful_functions as hf

class TestHelpfulFunctions(unittest.TestCase):

    #def test_doesLineIntersect(self):
    #    # Grundlegender Fall: Vektor schneidet die Linie
    #    self.assertTrue(hf.doesLineIntersect((0, 0), (2, 1), (1, 0), (-1, 1)))  # Vector intersects the line
#
    #    # Fall: Vektor schneidet die Linie nicht (parallel)
    #    self.assertFalse(hf.doesLineIntersect((0, 0), (1, 1), (1, 0), (1, 1)))  # Parallel lines, no intersection
#
    #    # Randfall: Vektor schneidet genau am Endpunkt der Linie
    #    self.assertTrue(hf.doesLineIntersect((0, 0), (1, 1), (2, 2), (-1, -1)))  # Vector intersects at the end point (p2)
#
    #    # Fall: Vektor geht in die falsche Richtung und schneidet nicht
    #    self.assertFalse(hf.doesLineIntersect((0, 0), (1, 1), (2, 2), (1, 1)))  # Vector points away from the line, no intersection
#
    #    # Linie und Vektor sind deckungsgleich, aber keine Schnittmenge
    #    self.assertFalse(hf.doesLineIntersect((0, 0), (2, 2), (0, 0), (2, 2)))  # Same direction, no intersection since it's the same line
#
    #    # Randfall: Linie ist ein Punkt (p1 == p2), Vektor zeigt auf diesen Punkt
    #    self.assertTrue(hf.doesLineIntersect((1, 1), (1, 1), (1, 1), (0, 0)))  # Single point, intersection at that point
#
    #    # Randfall: Linie ist ein Punkt (p1 == p2), Vektor zeigt nicht auf diesen Punkt
    #    self.assertFalse(hf.doesLineIntersect((1, 1), (1, 1), (2, 2), (0, 0)))  # No intersection because vector points elsewhere
#
    #    # Test: Vektor und Linie sind exakt parallel, aber Vektor liegt nicht auf der Linie
    #    self.assertFalse(hf.doesLineIntersect((0, 0), (1, 1), (1, 0), (2, 2)))  # Parallel lines, no intersection
#
    #    # Test: Vektor schneidet, aber außerhalb des Segments
    #    self.assertFalse(hf.doesLineIntersect((0, 0), (1, 1), (3, 3), (-1, -1)))  # Vector cuts the line, but not within the segment


    def test_lineIntersection(self):
        # Fall: Linien schneiden sich innerhalb der Segmente
        self.assertEqual(hf.lineIntersection((0, 0), (2, 2), (0, 2), (2, 0)), (1, 1))

        # Randfall: Linien schneiden sich genau an einem Endpunkt
        self.assertEqual(hf.lineIntersection((0, 0), (2, 2), (1, 1), (1, 3)), (1, 1))

        # Linien sind parallel und schneiden sich nicht
        self.assertIsNone(hf.lineIntersection((0, 0), (1, 1), (0, 1), (1, 2)))

        # Linien überschneiden sich außerhalb der Segmente (Schnittpunkt existiert, aber nicht auf den Segmenten)
        self.assertIsNone(hf.lineIntersection((0, 0), (1, 1), (2, 2), (3, 3)))

        # Linien sind identisch, Schnittpunkt nicht eindeutig (koexistente Linien)
        self.assertIsNone(hf.lineIntersection((0, 0), (2, 2), (0, 0), (2, 2)))

    def test_dot2(self):
        self.assertEqual(hf.dot2([1, 2], [3, 4]), 11)
        self.assertEqual(hf.dot2([0, 0], [5, -3]), 0)
        self.assertEqual(hf.dot2([2, 3], [4, 5]), 23)
        # Edge cases
        self.assertEqual(hf.dot2([-1, 2], [3, -4]), -11)
        self.assertEqual(hf.dot2([1.5, 2.5], [3.5, 4.5]), 16.5)
        # Common Mistakes
        with self.assertRaises(ValueError): hf.dot2([1, 2, 3],[4, 5])
        with self.assertRaises(ValueError): hf.dot2([1], [2, 3])
        with self.assertRaises(ValueError): hf.dot2([1, 2], "StupidValue")
        with self.assertRaises(ValueError): hf.dot2([1, 2], "[3, 4]")
        
    def test_dot3(self):
        self.assertEqual(hf.dot3([1, 2, 3], [4, 5, 6]), 32)
        with self.assertRaises(ValueError): hf.dot3([1, 2], [3, 4, 5])

    def test_makeMatrix(self):
        # Standardfälle
        self.assertEqual(hf.makeMatrix(2, 2), [[[], []], [[], []]])
        self.assertEqual(hf.makeMatrix(1, 1), [[[]]])
        # 3D-Matrix
        self.assertEqual(hf.makeMatrix(2, 2, 2), [[[[], []], [[], []]], [[[], []], [[], []]]])
        # Fehlerhafte Eingaben
        with self.assertRaises(TypeError): hf.makeMatrix("2", 2)
        with self.assertRaises(TypeError): hf.makeMatrix(2, [2])

    def test_transpose(self):
        # Standardfälle
        self.assertEqual(hf.transpose([[1, 2], [3, 4]]), [[1, 3], [2, 4]])
        self.assertEqual(hf.transpose([[1, 2, 3]]), [[1], [2], [3]])
        # Leere Matrix
        self.assertEqual(hf.transpose([]), [])
        # Fehlerhafte Eingaben
        with self.assertRaises(TypeError): hf.transpose("not a matrix")

    def test_HSVpercentToRGB(self):
        # Standardfälle
        self.assertEqual(hf.HSVpercentToRGB(0), (255.0, 0.0, 0.0))
        self.assertEqual(hf.HSVpercentToRGB(100), (255.0, 0.0, 0.0))
        # Randfälle und ungültige Eingaben
        with self.assertRaises(ValueError): hf.HSVpercentToRGB(110)
        with self.assertRaises(ValueError): hf.HSVpercentToRGB(-10)

    def test_RGBtoKivyColorCode(self):
        # Standardfälle
        self.assertEqual(hf.RGBtoKivyColorCode((255, 0, 0)), (1.0, 0.0, 0.0))
        self.assertEqual(hf.RGBtoKivyColorCode((0, 255, 0)), (0.0, 1.0, 0.0))
        # Randfälle
        self.assertEqual(hf.RGBtoKivyColorCode((0, 0, 0)), (0.0, 0.0, 0.0))
        self.assertEqual(hf.RGBtoKivyColorCode((255, 255, 255)), (1.0, 1.0, 1.0))

    def test_normalizeVector(self):
        # Standardfälle
        self.assertTrue(all(isclose(a, b) for a, b in zip(hf.normalizeVector((3, 4)), [0.6, 0.8])))
        # Fehlerhafte Eingaben
        with self.assertRaises(ValueError): hf.normalizeVector((0, 0))

    def test_vector_add(self):
        self.assertEqual(hf.vector_add([1, 2], [3, 4]), [4, 6])
        self.assertEqual(hf.vector_add([-1, -2], [1, 2]), [0, 0])

    def test_vector_subtract(self):
        self.assertEqual(hf.vector_subtract([1, 2], [3, 4]), [-2, -2])
        self.assertEqual(hf.vector_subtract([5, 5], [2, 3]), [3, 2])

    def test_scalar_vector_mult(self):
        self.assertEqual(hf.scalar_vector_mult(2, [1, 2, 3]), [2, 4, 6])

    def test_mag2(self):
        self.assertAlmostEqual(hf.mag2([3, 4]), 5)

    def test_mag3(self):
        self.assertAlmostEqual(hf.mag3([1, 2, 2]), 3)

    def test_vec2angleRad(self):
        self.assertAlmostEqual(hf.vec2angleRad([1, 0], [0, 1]), 1.5708, places=4)

    def test_vec3angleRad(self):
        self.assertAlmostEqual(hf.vec3angleRad([1, 0, 0], [0, 1, 0]), 1.5708, places=4)

    def test_timeFormat(self):
        self.assertEqual(hf.timeFormat(86461), "01d 00h 01m 01s 000ms")

if __name__ == "__main__":
    unittest.main()