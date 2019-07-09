def quaternion_mult(q, r):
    return [r[0]*q[0] - r[1]*q[1] - r[2]*q[2] - r[3]*q[3],
            r[0]*q[1] + r[1]*q[0] - r[2]*q[3] + r[3]*q[2],
            r[0]*q[2] + r[1]*q[3] + r[2]*q[0] - r[3]*q[1],
            r[0]*q[3] - r[1]*q[2] + r[2]*q[1] + r[3]*q[0]]

def point_rotation_by_quaternion(point, q):
    r = [0] + point
    q_conj = [q[0], -1 * q[1], -1 * q[2], -1 * q[3]]
    return quaternion_mult(quaternion_mult(q, r), q_conj)[1:]


def axis_angle_to_quaternion(x, y, z, a);
    return [math.cos(a / 2.), 
            math.sin(a / 2.) * x, 
            math.sin(a / 2.) * y, 
            math.sin(a / 2.) * z]

 print(point_rotation_by_quaternion([1, 0, 0],[0.7071203316249954, 0.0, 0.7071203316249954, 0.0])   