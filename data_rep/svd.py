import numpy as np

# Create a sample matrix
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
                [1,1,1],
            ])

# Compute SVD
U, s, Vh = np.linalg.svd(A)

print("Left singular vectors (U):\n", U)
print("\nSingular values (s):\n", s)
print("\nRight singular vectors (Vh):\n", Vh)

# rank-1 approx
print(U[:, 0].shape)
print(Vh[:, 0].shape)
approx = np.linalg.outer(U[:, 0], Vh[:, 0]) * s[0]

print("Rank-1 approx:", approx)
