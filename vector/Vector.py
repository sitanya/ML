from math import sqrt, pi, acos
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'Zero vector NO UNIQUE PARALLEL COMPONENT'
    ONLY_DEFINED_IN_TOW_THREE_DIMS_MSG = 'ONLY_DEFINED_IN_TOW_THREE_DIMS_MSG'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(Decimal(x) for x in coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def plus(self, v):
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scaler(self, c):
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = Decimal(self.magnitude())
            return self.times_scaler(Decimal('1.0') / magnitude)
        except ZeroDivisionError:
            raise self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(Decimal(u1.dot(u2)).quantize(Decimal('0.000')))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with the zero vector")
            else:
                raise e

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scaler(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_orthogonal_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = Vector([y_1 * z_2 - y_2 * z_1,
                               -(x_1 * z_2 - x_2 * z_1),
                               x_1 * y_2 - x_2 * y_1])
            return new_coordinates
        except Exception as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                slef_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return slef_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or
                          msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TOW_THREE_DIMS_MSG)
            else:
                raise e

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return round(cross_product.magnitude(),3)

    def area_of_triangle_with(self, v):
        cross = self.cross(v)
        return round(Decimal(cross.magnitude())/Decimal('2.0'),3)


    def __str__(self):
        return 'Vector: {}'.format([round(x, 3) for x in self.coordinates])

    def __eq__(self, v):
        return self.coordinates == v.coordinates


# v1 = Vector([8.462, 7.893, -8.187])
# w1 = Vector([6.984, -5.975, 4.778])
#
# v2 = Vector([-8.987, -9.838, 5.031])
# w2 = Vector([-4.268, -1.861, -8.866])
#
# v3 = Vector([1.5, 9.547, 3.691])
# w3 = Vector([-6.007, 0.124, 5.772])
#
# print v1.cross(w1)
#
# print v2.area_of_parallelogram_with(w2)
#
# print v3.area_of_triangle_with(w3)
