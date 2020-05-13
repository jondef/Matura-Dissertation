# -*- coding: utf-8 -*-
# Python 3.6.6

# begin: 23 nov 2018

try:
    import matplotlib.pyplot as plt  # pip install matplotlib
except ModuleNotFoundError as exc:
    print("Matplotlib not found. Plotting will not work.")


class Polynomial:
    def __init__(self, coeffs: tuple):
        if type(coeffs) != tuple:
            raise TypeError("Only tuples are allowed.")

        self.coeffs = coeffs

    @classmethod
    def from_string(cls, string: str):
        """ 2nd init function (overloading in c++)"""
        coeffs = []  # contains coefficients
        exponent_list = []  # contains powers that are present

        string = string.replace(" ", "")
        string = string.replace("-", "+-")

        string = string.split("+")

        for term in string:
            # skip bits that are empty.
            # They are caused if the user enters
            # a function like -x
            if term == "":
                continue

            pow_sign_pos = term.find("^")

            # need to use eval to convert
            # fractions to float
            # if only x or constant
            if pow_sign_pos == -1:
                if 'x' in term:
                    term = term.replace("x", "")
                    term = term.replace("*", "")
                    term = "1" if term == "" else term  # support for x
                    term = "-1" if term == "-" else term  # support for -x
                    coeffs.append(eval(term))
                    exponent_list.append(1)
                else:
                    # constants
                    coeffs.append(eval(term))
                    exponent_list.append(0)

            else:
                # bits from x^2
                base = term[:pow_sign_pos]
                base_multiplier = base.replace('x', '').replace('*', '')
                base_multiplier = 1 if base_multiplier == "" else base_multiplier
                base_multiplier = -1 if base_multiplier == "-" else base_multiplier
                exponent = term.replace(f"{base}^", "")
                exponent_list.append(int(exponent))
                coeffs.append(eval(str(base_multiplier)))

        # fix for the last zero (constant)
        if exponent_list[-1] != 0:
            exponent_list.append(0)
            coeffs.append(0)

        # add missing zeros in the coeffs list
        fixes = 0
        for position, iter in enumerate(exponent_list):
            if position == 0:
                continue

            previous = exponent_list[position - 1]

            if previous - iter != 1:
                for _ in range(previous - iter - 1):
                    coeffs.insert(position + fixes, 0)
                    fixes += 1

        return cls(tuple(coeffs))

    @property
    def degree(self):
        """ Use this to get the degree of the function """
        return len(self.coeffs) - 1

    def __repr__(self):
        """ must be = to how you created the instance """
        return f"{__class__.__name__}({self.coeffs})"

    def __str__(self):
        """ executed on print """
        final_str = ""
        power = self.degree
        for coeff in self.coeffs:
            if float(coeff) == 0:
                power -= 1
                continue

            # important for formatting
            # don't replace the + 1 at the end without an x
            if power != 0:
                if float(coeff) == 1.0:
                    coeff = ""
                elif float(coeff) == -1.0:
                    coeff = "-"

            if power == 1:
                final_str += f"{coeff}x + "
            elif power == 0:
                final_str += f"{coeff} + "
            else:
                final_str += f"{coeff}x^{power} + "

            power -= 1

        final_str = final_str.replace("+ -", "- ")

        return "0" if final_str == "" else final_str[:-3]

    def __len__(self):
        """
        :return: the length of the coefficient tuple
        """
        return len(self.coeffs)

    def __call__(self, x: float):
        """
        Usage: instance(x) is equal to f(x)
        :param x: the x in f(x)
        :return: the image of x
        """
        result = 0
        for counter, coeff in enumerate(self.coeffs):
            result += coeff * x ** (self.degree - counter)

        return result

    def __add__(self, other):
        """
        :param other: Polynomial instance
        :return: Polynomial instance of addition
        """
        # find the biggest polynomial to add missing zeros
        if self.degree > other.degree:
            other.coeffs = (len(self) - len(other)) * (0,) + other.coeffs
        elif self.degree < other.degree:
            self.coeffs = (len(other) - len(self)) * (0,) + self.coeffs

        # add the coefficients up
        final = ()
        for counter, coeff in enumerate(self.coeffs):
            final += (coeff + other.coeffs[counter],)

        return Polynomial(final)

    def __sub__(self, other):
        """
        :param other: Polynomial instance
        :return: Polynomial instance of addition
        """
        # find the biggest polynomial to add missing zeros
        if self.degree > other.degree:
            other = (len(self.coeffs) - len(other)) * (0,) + other.coeffs
        elif self.degree < other.degree:
            self.coeffs = (len(other) - len(self)) * (0,) + self.coeffs

        # add the coefficients up
        final = ()
        for counter, coeff in enumerate(self.coeffs):
            final += (coeff - other.coeffs[counter],)

        return Polynomial(final)

    def __floordiv__(self, other: float):
        """ Horner division
        :param other: (float/int) divisor
        :return: Polynomial instance of division without rest
        """
        result = ()
        for counter, coefficient in enumerate(self.coeffs):
            if counter == 0:
                result += (coefficient,)
            else:
                result += (coefficient + result[counter - 1] * other,)

        return Polynomial(result[:-1])  # remove the rest

    def derivative(self):
        """
        :return: derivative of given function
        """
        result = ()
        for counter, coeff in enumerate(self.coeffs):
            exponent = self.degree - counter
            result += (exponent * coeff,)

        return Polynomial(result[:-1])  # remove the last zero

    def integral(self):
        """
        :return: integral of given function
        """
        coeffs = self.coeffs + (0,)  # add a zero

        result = ()
        for counter, coeff in enumerate(coeffs):
            if coeff == 0:
                result += (0,)
                continue
            expo = len(coeffs) - counter - 1
            result += (coeff / expo,)

        return Polynomial(result)

    def calculate_area(self, low_lim: float, high_lim: float):
        """
        :param low_lim: float / int
        :param high_lim: float / int
        :return: area of function
        """
        # add zeros that are inside bounds to zeros array
        zeros = []
        for zero in self.find_all_zero(single=True):
            if low_lim < zero < high_lim:
                zeros.append(zero)

        # add bounds to the array
        zeros.insert(0, low_lim)
        zeros = zeros + [high_lim]

        # Finally, calculate the area that is
        # between each zero and add it up
        result = 0
        for counter, zero in enumerate(zeros):
            if counter == 0:
                last = zeros[counter]
                continue

            result += abs(self.integral()(zero) - (self.integral()(last)))
            last = zeros[counter]

        return result

    def calculate_tangent(self, x_cord: float):
        """
        :param x_cord: (int/float) the x cord where to calculate the tangent
        :return: Polynomial instance of the tangent
        """
        first_derivative = self.derivative()

        m = first_derivative(x_cord)

        y = self(x_cord)

        h = -(m * x_cord - y)  # solve for h

        return Polynomial((m, h))

    def get_extreme_points(self):
        """
        This method finds all extreme points ofa function
        :return: list of format [lowpoints, turningpoints, highpoints]
        """
        highpoints = []
        lowpoints = []
        turningpoints = []

        first_deriv = self.derivative()
        second_deriv = first_deriv.derivative()

        # High-, lowpoints
        zeros = first_deriv.find_all_zero()
        for zero in zeros:
            if second_deriv(zero) < 0:  # high point
                highpoints.append((zero, self(zero)))

            elif second_deriv(zero) > 0:  # low point
                lowpoints.append((zero, self(zero)))

        # turning points
        zeros = second_deriv.find_all_zero()
        for zero in zeros:
            turningpoints.append((zero, self(zero)))

        return [lowpoints, turningpoints, highpoints]

    def solve_zero_newton(self):
        """
        :return: None if no zero found else zero
        """
        first_derivative = self.derivative()

        # this variable is the zero to be found
        y_cord = 0

        # if function has no zeros, the
        # the loop is never going to end
        iteration = 0
        # /!\ The rounding might be too big /!\
        while round(self(y_cord), 12) != 0:
            iteration += 1
            try:
                y_cord = y_cord - (self(y_cord) / first_derivative(y_cord))
            except ZeroDivisionError:
                # If unable to divide, move the starting x position
                y_cord += 1

            if iteration > 100:
                return None  # no solution

        return y_cord

    def find_all_zero(self, rounded=10, single=False):
        """
        :param single: whether to remove or leave the double zeros
        :param rounded: how many decimals to round the zeros to after comma
        :return: sorted list with all zeros
        """
        results = []
        function = self

        # if function is a constant
        # it has no zeros except
        # f(x)=0, which has infinite solutions
        if self.degree < 1:
            return []

        # The idea here is to find a zero of the function
        # using the Newton algorithm and then divide the
        # function by the zero until there is none left.
        # A function divided by its only zero will be equal to 1
        while str(function) != "1":
            # find a zero
            zero = function.solve_zero_newton()

            # solve_zero_newton will return None if
            # it didn't find a zero
            if zero is not None:
                results.append(round(zero, rounded))
                function = function // zero
            else:
                break

        if single:
            return sorted(list(set(results)))

        return sorted(results)

    @staticmethod
    def generate_x_array(lower_lim: int, upper_lim: int, values=1000):
        """
        This function calculates the x array
        For example: generate_x_array(0, 10, 6)
        will return:
        [0,2,4,6,8,10]
        :param lower_lim: int
        :param upper_lim: int0
        :param values: values to be included in the array
        :return: an array with the x points
        """
        final_array = []
        difference = upper_lim - lower_lim
        increment = difference / (values - 1)

        for iter in range(values):
            final_array.append(lower_lim + increment * iter)

        return final_array


def menu():
    sign = "\n>>> "

    # user function | format: (function: instance of class)
    user_functions = {}

    # Default plot limits
    lower_lim, upper_lim = -10, 10

    menu_dict = {"1": "Polynomial addition",
                 "4": "Calculate derivative",
                 "5": "Calculate tangent",
                 "6": "Calculate extreme points",
                 "7": "Calculate integral",
                 "8": "Calculate area",
                 "9": "Calculate zeros",
                 "+": "Add function",
                 "-": "Remove function",
                 ".": "Change plot limits",
                 "*": "Show functions",
                 "0": "Show Plot",
                 "h": "Show this help",
                 "e": "Exit"}

    # print the help menu once
    [print(f"[{x}]", menu_dict[x]) for x in menu_dict]

    """ MAIN PROGRAM LOOP """
    while True:
        user_choice = input(sign)
        if user_choice not in menu_dict:
            continue

        # """ ADDITION """
        if menu_dict[user_choice] == "Polynomial addition":
            first_poly = Polynomial.from_string(input(f"Enter first polynomial{sign}"))
            second_poly = Polynomial.from_string(input(f"Enter second polynomial{sign}"))
            print(f"Result (addition): {first_poly + second_poly}\n")

        # """ DERIVATIVE, TANGENT, EXTREME POINTS """
        elif menu_dict[user_choice] == "Calculate derivative":
            poly = Polynomial.from_string(input(f"Enter polynomial to derive{sign}"))
            print(f"Result (derivative): {poly.derivative()}\n")

        elif menu_dict[user_choice] == "Calculate tangent":
            tangent_function = Polynomial.from_string(input(f"Enter function to calculate tangent{sign}"))
            x_coord = float(input(f"Enter x point at which to calculate the tangent{sign}"))
            tan = tangent_function.calculate_tangent(x_coord)
            print(f"Result (tangent at x={x_coord}): {tan if str(tan) != '' else '0'}")

        elif menu_dict[user_choice] == "Calculate extreme points":
            point_function = Polynomial.from_string(input(f"Enter function to Extrempoints{sign}"))
            print(f"Result (Highpoints): {point_function.get_extreme_points()[2]}")
            print(f"Result (turningpuntke): {point_function.get_extreme_points()[1]}")
            print(f"Result (Lowpoints): {point_function.get_extreme_points()[0]}")

        # """ INTEGRAL, AREA, ZEROS """
        elif menu_dict[user_choice] == "Calculate integral":
            poly = Polynomial.from_string(input(f"Enter polynomial to integrate{sign}"))
            print(f"Result (integration): {poly.integral()}\n")

        elif menu_dict[user_choice] == "Calculate area":
            # request functino from user and convert it to Polynomial
            area_function = Polynomial.from_string(input(f"Enter function{sign}"))

            # request limits of the area and convert them to integers
            low_bound, high_bound = input(f"Enter lower & upper limit separated by a comma{sign}").split(",")
            low_bound, high_bound = float(low_bound), float(high_bound)

            print(f"Result (area): {area_function.calculate_area(low_bound, high_bound)}")

        elif menu_dict[user_choice] == "Calculate zeros":
            zeros = Polynomial.from_string(input(f"Enter function{sign}"))
            print(zeros.find_all_zero())

        elif menu_dict[user_choice] == "Add function":
            function_to_add = input(f"Enter function to add:{sign}")
            user_functions[function_to_add] = Polynomial.from_string(function_to_add)

        elif menu_dict[user_choice] == "Remove function":  # TODO: FIX REMOVE FUNCTION THAT DOESNT EXIST
            function_to_remove = input(f"Enter function to remove:{sign}")
            user_functions.pop(function_to_remove)

        elif menu_dict[user_choice] == "Change plot limits":
            lower_lim, upper_lim = input("Enter upper and lower limit separated by a comma: ").split(",")
            lower_lim, upper_lim = float(lower_lim), float(upper_lim)

        elif menu_dict[user_choice] == "Show functions":
            print(user_functions)
            [print(f"[{counter}] {func}") for counter, func in enumerate(user_functions, 1)]

        elif menu_dict[user_choice] == "Show Plot":
            x_array = Polynomial.generate_x_array(lower_lim, upper_lim)

            for func in user_functions:
                # generate y array for each function
                y_array = []
                for x in x_array:
                    # access the instance of that function in the dict
                    y_array.append(user_functions[func](x))

                plt.plot(x_array, y_array)

            plt.gca().legend([f"${str(function)}$" for function in user_functions])  # add function to legend
            plt.grid(True)
            plt.show()

        elif menu_dict[user_choice] == "Show this help":
            [print(f"[{x}]", menu_dict[x]) for x in menu_dict]

        elif menu_dict[user_choice] == "Exit":
            if input(f"Exit (y/n)? ") == "y":
                exit(0)


if __name__ == "__main__":
    menu()
