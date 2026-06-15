from scipy.sparse import csr_matrix


class SparseOptimizer:

    @staticmethod
    def convert(matrix):

        return csr_matrix(
            matrix.values
        )