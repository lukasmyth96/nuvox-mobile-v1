import numpy as np


def angle(vectors: np.ndarray) -> np.ndarray:
    """Returns the angles between vectors.

    Parameters
    ------------
    vectors: np.ndarray
        A 2D-array of shape (N,M) representing N vectors in M-dimensional space.

    Returns
    ------------
    angles: np.ndarray
        A 1D-array of values of shape (N-1,), with each value between 0 and pi where:
            - 0 implies the vectors point in the same direction
            - pi/2 implies the vectors are orthogonal
            - pi implies the vectors point in opposite directions
    """

    # For the point at index i, vectors_inbound[i] is the (x, y) vector
    # inbound to that point and vectors_outbound[i] is the vector outbound.
    vectors_inbound = vectors[:-1]
    vectors_outbound = vectors[1:]

    # Using law of cosines: θ = arcos(a•b / |a||b|)
    inbound_dot_outbound = (vectors_inbound * vectors_outbound).sum(axis=1)  # a•b
    mod_inbound_mod_outbound = (np.sqrt((vectors_inbound ** 2).sum(axis=1) * (vectors_outbound ** 2).sum(axis=1)))  # |a||b|
    cosine_angles = inbound_dot_outbound / mod_inbound_mod_outbound  # cos(θ)
    angles = np.arccos(cosine_angles)

    return angles
