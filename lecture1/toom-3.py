import numpy as np

def pad_to_length(poly, length):
    """Pad polynomial to the specified length with zeros."""
    return np.pad(poly, (0, length - len(poly)), 'constant')

def split_poly(poly, n):
    """Split polynomial into n parts."""
    k = (len(poly) + n - 1) // n
    parts = [poly[i * k:(i + 1) * k] for i in range(n)]
    for i in range(len(parts)):
        while len(parts[i]) < k:
            parts[i] = np.append(parts[i], 0)
    return parts

def interpolate(points, values):
    """Perform interpolation using Lagrange polynomial."""
    n = len(points)
    result = np.zeros_like(values, dtype=float)
    #
    for i in range(n):
        term = np.copy(values[i])
        for j in range(n):
            if i != j:
                term *= (0.0 - points[j]) / (points[i] - points[j])
        result += term
    return result

def toom3_multiply_polys(poly1, poly2):
    """Multiply two polynomials using Toom-3 algorithm with NumPy."""
    n = 3
    len1, len2 = len(poly1), len(poly2)
    max_len = max(len1, len2)
    padded_length = max_len + (n - max_len % n) % n

    # Pad polynomials with zeros
    poly1_padded = pad_to_length(poly1, padded_length)
    poly2_padded = pad_to_length(poly2, padded_length)

    # Split polynomials into parts
    parts1 = split_poly(poly1_padded, n)
    parts2 = split_poly(poly2_padded, n)

    # Evaluate polynomials at specific points
    eval_points = np.array([0, 1, -1, 2, -2], dtype=float)
    evals1 = np.array([np.polyval(part[::-1], eval_points) for part in parts1])
    evals2 = np.array([np.polyval(part[::-1], eval_points) for part in parts2])

    # Multiply the evaluated values using element-wise multiplication
    prod_evals = np.multiply(evals1, evals2) # evals1 * evals2
    # Interpolate to get the coefficients of the result polynomial
    interpolated_values = np.array([interpolate(eval_points, prod_evals[i, :]) for i in range(prod_evals.shape[0])])
    #interpolated_values = np.array([interpolate(eval_points, prod_evals[:, i]) for i in range(prod_evals.shape[1])])

    # Combine the parts to form the final product polynomial
    result_length = len(poly1) + len(poly2) - 1
    product = np.zeros(result_length, dtype=float)
    part_length = len(poly1_padded) // n

    # Ensure product has the right size and add interpolated values
    for i in range(len(interpolated_values)):
        shift = i * part_length
        for j in range(len(interpolated_values[i])):
            if shift + j < result_length:
                product[shift + j] += interpolated_values[i][j]

    return np.round(product[:result_length]).astype(int)

# Example usage
poly1 = np.array([1, 2, 3, 4, 5])  # Coefficients of first polynomial
poly2 = np.array([4, 5, 6])  # Coefficients of second polynomial

product = toom3_multiply_polys(poly1, poly2)
print("Product polynomial coefficients:", product, np.polyval(product, 10))

# Expected result using NumPy's convolution for verification
expected_product = np.convolve(poly1, poly2)
print("Expected product polynomial coefficients:", expected_product, np.polyval(expected_product, 10))
