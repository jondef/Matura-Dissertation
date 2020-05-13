import unittest

from main import Polynomial

testing = [
#   function,       degree, derivative,         integral,                                            zeros,                                    call(0), call(-10), extrempoints
    ["3x",               1, "3",                "1.5x^2",                                            "[0]",                                          0,  -30,     [[], [], []]                                                                                                          ],
    ["x",                1, "1",                "0.5x^2",                                            "[0]",                                          0,  -10,     [[], [], []]                                                                                                          ],
    ["-1/2x^2",          2, "-x",               "-0.16666666666666666x^3",                           "[0, 0]",                                       0,  -50,     [[], [], [(0, 0.0)]]                                                                                                  ],
    ["x^2+0",            2, "2x",               "0.3333333333333333x^3",                             "[0, 0]",                                       0,  100,     [[(0, 0.0)], [], []]                                                                                                  ],
    ["4x^5-2x^3+x",      5, "20x^4 - 6x^2 + 1", "0.6666666666666666x^6 - 0.5x^4 + 0.5x^2",           "[0]",                                          0,  -398010, [[], [(-0.3872983346, -0.30596568433897803), (0, 0), (0.3872983346, 0.30596568433897803)], []]                        ],
    ["-x^3-3/2x^2+8x-2", 3, "-3x^2 - 3.0x + 8", "-0.25x^4 - 0.5x^3 + 4.0x^2 - 2.0x",                 "[-3.7655644371, 0.2655644371, 2.0]",           -2, 768,     [[(-2.2078251277, -16.212313244682942)], [(-0.5, -6.25)], [(1.2078251277, 3.712313244682943)]]                        ],
    ["x^3-6x^2+9x-2",    3, "3x^2 - 12x + 9",   "0.25x^4 - 2.0x^3 + 4.5x^2 - 2.0x",                  "[0.2679491924, 2.0, 3.7320508076]",            -2, -1692,   [[(3.0, -2.0)], [(2.0, 0.0)], [(1.0, 2.0)]]                                                                           ],
    ["-4x^3+4x^2+8x",    3, "-12x^2 + 8x + 8",  "-x^4 + 1.3333333333333333x^3 + 4.0x^2",             "[-1.0, 0, 2.0]",                               0,  4320,    [[(-0.5485837704, -2.5245212377635955)], [(0.3333333333, 2.9629629626518517)], [(1.215250437, 8.450447163689521)]]    ],
    ["x^3-6x^2+9x",      3, "3x^2 - 12x + 9",   "0.25x^4 - 2.0x^3 + 4.5x^2",                         "[0, 2.9999996424, 3.0000003576]",              0,  -1690,   [[(3.0, 0.0)], [(2.0, 2.0)], [(1.0, 4.0)]]                                                                            ],
    ["-2x^2+x+1",        2, "-4x + 1",          "-0.6666666666666666x^3 + 0.5x^2 + x",               "[-0.5, 1.0]",                                  1,  -209,    [[], [], [(0.25, 1.125)]]                                                                                             ],
    ["2x^5+4x^2-1",      5, "10x^4 + 8x",       "0.3333333333333333x^6 + 1.3333333333333333x^3 - x", "[-1.1794043143, -0.5183777764, 0.4862225017]", -1, -199601, [[(0, -1)], [(-0.5848035476, 0.23118268145783993)], [(-0.9283177667, 1.0682573024306086)]]                            ],
    ["2x^4+3x^2-2x+1",   4, "8x^3 + 6x - 2",    "0.4x^5 + x^3 - x^2 + x",                            "[]",                                           1,  20321,   [[(0.298035819, 0.6861842956155538)], [], []]                                                                         ],
    ["-4x^3+3x^2-2x+1",  3, "-12x^2 + 6x - 2",  "-x^4 + x^3 - x^2 + x",                              "[0.6058295862]",                               1,  4321,    [[], [(0.25, 0.625)], []]                                                                                             ],
    ["4x^5-2x^3+x+1",    5, "20x^4 - 6x^2 + 1", "0.6666666666666666x^6 - 0.5x^4 + 0.5x^2 + x",       "[-0.782968399]",                               1,  -398009, [[], [(-0.3872983346, 0.694034315661022), (0, 1), (0.3872983346, 1.305965684338978)], []]                             ],
    ["3x^3-x^2+2x-1",    3, "9x^2 - 2x + 2",    "0.75x^4 - 0.3333333333333333x^3 + x^2 - x",         "[0.4598632694]",                               -1, -3121, [[], [(0.1111111111, -0.7860082304736625)], []]                                                                         ],
    ["4x^4+2x^2-2",      4, "16x^3 + 4x",       "0.8x^5 + 0.6666666666666666x^3 - 2.0x",             "[-0.7071067812, 0.7071067812]",                -2, 40198, [[(0, -2)], [], []]                                                                                                     ],

    ["9x^9-8x^8+7x^7-6x^6+5x^5-4x^4+3x^3-2x^2+x+1", 9, "81x^8 - 64x^7 + 49x^6 - 36x^5 + 25x^4 - 16x^3 + 9x^2 - 4x + 1", "0.9x^10 - 0.8888888888888888x^9 + 0.875x^8 - 0.8571428571428571x^7 + 0.8333333333333334x^6 - 0.8x^5 + 0.75x^4 - 0.6666666666666666x^3 + 0.5x^2 + x", "[-0.3821609762]", 1, -9876543209, [[], [(0.4358419755, 1.2130755570561793)], []]]
]


class TestMain(unittest.TestCase):

    def test_repr(self):
        function = Polynomial.from_string("x^2")
        self.assertEqual(str(function.__repr__()), "Polynomial((1, 0, 0))")

    def test_len(self):
        function = Polynomial.from_string("x^2")
        self.assertEqual(function.__len__(), 3)

    def test_degree(self):
        for index, function in enumerate(testing):
            function = Polynomial.from_string(function[0])
            self.assertEqual(function.degree, testing[index][1])  # degree

    def test_derivative(self):
        for index, group in enumerate(testing):
            function = Polynomial.from_string(group[0])
            self.assertEqual(str(function.derivative()), testing[index][2])  # derivative

    def test_integral(self):
        for index, group in enumerate(testing):
            function = Polynomial.from_string(group[0])
            self.assertEqual(str(function.integral()), testing[index][3])  # Integral

    def test_zeros(self):
        for index, group in enumerate(testing):
            function = Polynomial.from_string(group[0])
            self.assertEqual(str(function.find_all_zero()), testing[index][4])  # zeros

    def test_call_zero(self):
        for index, group in enumerate(testing):
            function = Polynomial.from_string(group[0])
            self.assertEqual(function(0), testing[index][5])  # f(0)

    def test_call_neg_ten(self):
        for index, group in enumerate(testing):
            function = Polynomial.from_string(group[0])
            self.assertEqual(function(-10), testing[index][6])  # f(-10)

    def test_extrempoints(self):
        for index, group in enumerate(testing):
            function = Polynomial.from_string(group[0])
            self.assertEqual(function.get_extreme_points(), testing[index][7])  # extrempoints

    def test_addition(self):
        function_1 = Polynomial.from_string("x^3+3x^2-5x-90")
        function_2 = Polynomial.from_string("-3x^3-3x^2-10x+45")
        self.assertEqual(str(function_1 + function_2), "-2x^3 - 15x - 45")

    def test_subtraction(self):
        function_1 = Polynomial.from_string("x^3+3x^2-5x-90")
        function_2 = Polynomial.from_string("-3x^3-3x^2-10x+45")
        self.assertEqual(str(function_1 - function_2), "4x^3 + 6x^2 + 5x - 135")

    def test_tangent(self):
        function_1 = Polynomial.from_string("2x^2")
        self.assertEqual(str(function_1.calculate_tangent(0)), "0")  # tangent at x=0

        function_2 = Polynomial.from_string("-3x^3-3x^2-10x+45")
        self.assertEqual(str(function_2.calculate_tangent(-10)), "-850x - 5655")  # tangent at x=-10

        function_3 = Polynomial.from_string("x^3+3x^2-5x-90")
        self.assertEqual(str(function_3.calculate_tangent(-5)), "40x + 85")  # tangent at x=-5

    def test_calculate_area(self):
        function_1 = Polynomial.from_string("x^3+5")
        self.assertEqual(function_1.calculate_area(-5, 9), 1829.3248196000754)  # -5,9
        self.assertEqual(function_1.calculate_area(-0, 0), 0)  # 0,0

        function_2 = Polynomial.from_string("-3x^3-3x^2-10x+45")
        self.assertEqual(function_2.calculate_area(-10, -5), 6756.25)  # -10,-5
        self.assertEqual(function_2.calculate_area(5, 10), 8056.25)  # 5,10

    def test_generate_x_array(self):
        self.assertEqual(Polynomial.generate_x_array(0, 10, 6), [0, 2, 4, 6, 8, 10])
        self.assertEqual(Polynomial.generate_x_array(0, 20, 10),
                         [0, 2.2222222222222223, 4.444444444444445, 6.666666666666667, 8.88888888888889,
                          11.11111111111111, 13.333333333333334, 15.555555555555557, 17.77777777777778, 20])


if __name__ == "__main__":
    unittest.main(verbosity=2)
