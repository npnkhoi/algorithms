"""
Forward kinematics in 3D

poses: 4x4 matrices
rotations are to be normalized
"""

import numpy as np
from pydantic import BaseModel

class Joints(BaseModel):
    translations: list[list[float]]
    axes: list[list[float]]
    ee_rotation: list[list[float]]
    ee_translation: list[float]
    types: str
    
    def normalize_axes(self):
        normalized_axes = []
        for axis in self.axes:
            axis_np = np.array(axis)
            norm = np.linalg.norm(axis_np)
            if norm == 0:
                raise ValueError("Axis vector cannot be zero.")
            normalized_axis = (axis_np / norm).tolist()
            normalized_axes.append(normalized_axis)
        self.axes = normalized_axes


def load_joints(fn: str) -> Joints:
    joints = Joints.parse_file(fn)
    joints.normalize_axes()
    return joints

def skew_symmetric_matrix(vec: np.ndarray | list) -> np.ndarray:
    vec = np.array(vec)
    assert vec.shape == (3,)
    return np.array([
        [0, -vec[2], vec[1]],
        [vec[2], 0, -vec[0]],
        [-vec[1], vec[0], 0]
    ])

def fk(
    joints: Joints,
    joint_values: list[float]
) -> np.ndarray: # 4x4 array for end-effector pose
    
    # init_joint_translations: np.ndarray, # nx3 array, translation in space frame
    # init_ee_rotation: np.ndarray, # 3x3 in space frame
    # init_ee_translation: np.ndarray,
    # joint_types: list[str], # elements are R or P
    
    p_ee = np.array(joints.translations[-1])
    R_ee = np.array(joints.ee_rotation)
    # print(f"init ee translation: {init_ee_translation}")
    init_ee_pose = np.array([
        [R_ee[0, 0], R_ee[0, 1], R_ee[0, 2], p_ee[0]],
        [R_ee[1, 0], R_ee[1, 1], R_ee[1, 2], p_ee[1]],
        [R_ee[2, 0], R_ee[2, 1], R_ee[2, 2], p_ee[2]],
        [0, 0, 0, 1]
    ])
    
    n = len(joints.types)
    
    if len(joint_values) != n:
        raise ValueError(f"joint_values length {len(joint_values)} != number of joints {n}")
    
    # build body twists (expressed in end-effector frame)
    body_twists = []
    adjoint_bs = np.block([
        [R_ee.T, np.zeros((3, 3))],
        [-R_ee.T @ skew_symmetric_matrix(p_ee), R_ee.T]
    ])
    for i in range(n):
        assert joints.types[i] in ["R", "P"]
        q = np.array(joints.translations[i])
        axis = np.array(joints.axes[i])
        if joints.types[i] == "R":
            w = axis  # axis should already be normalized
            v = -np.cross(w, q)
        else:  # prismatic
            w = np.zeros(3)
            v = axis  # translation direction
        spatial_twist = np.concatenate((w, v))
        body_twist = adjoint_bs @ spatial_twist
        body_twists.append(body_twist)
    
    def exp_twist(xi: np.ndarray, theta: float) -> np.ndarray:
        """Exponential map of a twist (xi: 6-vector [w;v], theta scalar) -> 4x4 transform."""
        w = xi[:3]
        v = xi[3:]
        w_norm = np.linalg.norm(w)
        T = np.eye(4)
        if w_norm > 1e-8:
            # w is assumed normalized (or close); use Rodrigues' formula (w treated as unit axis)
            w_hat = skew_symmetric_matrix(w)
            R = np.eye(3) + np.sin(theta) * w_hat + (1 - np.cos(theta)) * (w_hat @ w_hat)
            G = (np.eye(3) * theta
                 + (1 - np.cos(theta)) * w_hat
                 + (theta - np.sin(theta)) * (w_hat @ w_hat))
            p = G @ v
        else:
            # pure translation
            R = np.eye(3)
            p = v * theta
        T[:3, :3] = R
        T[:3, 3] = p
        return T
    
    # body-product formula: T(θ) = M * exp(B1 θ1) * ... * exp(Bn θn)
    T = init_ee_pose.copy()
    for xi, theta in zip(body_twists, joint_values):
        T = T @ exp_twist(xi, float(theta))
    
    return T


if __name__ == '__main__':
    joints = load_joints("joints_example.json")
    # print(joints)
    T = fk(
        joints,
        [0, 0, 0, 0, np.pi, 0]
    )
    print("End-effector pose:\n", T)
    
    print(np.linalg.inv(T))