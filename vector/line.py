from decimal import Decimal, getcontext

from Vector import Vector

getcontext().prec = 30


class Line(object):
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Line.first_nonzero_index(n)
            list = []
            for x in n.coordinates:
                list.append(x)
            initial_coefficient = list[initial_index]

            basepoint_coords[initial_index] = c / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i == initial_index)) + 'x_{}'.format(i + 1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def first_nonzero_index(vector):
        for k, item in enumerate(vector.coordinates):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel_to(self, ell):
        n1 = self.normal_vector
        n2 = ell.normal_vector

        return n1.is_parallel_to(n2)

    def __eq__(self, ell):
        if not self.is_parallel_to(ell):
            return False
        x0 = self.basepoint
        y0 = ell.basepoint

        basepoint_difference = x0.minus(y0)
        n = self.normal_vector
        return basepoint_difference.is_orthogonal_to(n)

    def intersection_with(self, ell):
        try:
            A, B = self.normal_vector.coordinates
            C, D = ell.normal_vector.coordinates
            k1 = self.constant_term
            k2 = ell.constant_term
            x_numerator = D * k1 - B * k2
            y_numerator = -C * k1 + A * k2
            one_over_denom = Decimal('1') / (A * D - B * C)

            return Vector([x_numerator, y_numerator]).times_scaler(one_over_denom)

        except ZeroDivisionError:
            if self == ell:
                return self
            else:
                return None




class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

#
# v1 = Line(normal_vector=Vector([4.046, 2.836]), constant_term=1.21)
# w1 = Line(normal_vector=Vector([10.115, 7.09]), constant_term=3.025)
#
# v2 = Line(normal_vector=Vector([7.204, 3.182]), constant_term=8.68)
# w2 = Line(normal_vector=Vector([8.172, 4.114]), constant_term=9.883)
#
# v3 = Line(normal_vector=Vector([1.182, 5.562]), constant_term=6.774)
# w3 = Line(normal_vector=Vector([1.773, 8.343]), constant_term=9.525)
#
# print v1.is_parallel_to(w1)
# print v1 == w1
# print v1.intersection_with(w1)
#
# print "============="
#
# print v2.is_parallel_to(w2)
# print v2 == w2
# print v2.intersection_with(w2)
#
# print "============="
#
# print v3.is_parallel_to(w3)
# print v3 == w3
# print v3.intersection_with(w3)
