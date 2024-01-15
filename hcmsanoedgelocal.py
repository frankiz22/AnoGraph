from submatrix import Submatrix
from hcms import Hcms
import numpy as np

class HcmsAnoedgeLocal(Hcms):
    def __init__(self, r: int, b: int, d : int):
        """
        Initializes an Hcms object.

        Parameters:
        - r (int): Number of rows.
        - b (int): Number of buckets.
        - d (int): Number of dense submatrices

        """
        super().__init__(r, b)
        self.num_dense_submatrices = d
        self.densest_matrices = []
    
    def decay(self, decay_factor: float) -> None:
        """
        Decays the count values and optionally decays the densest_matrices using NumPy operations.

        Parameters:
        - decay_factor (float): Factor to decay the count values.
        """
        self.count *= decay_factor

        for row in self.densest_matrices:
            for submatrix in row:
                submatrix.decay(decay_factor)
    

    def initialize_dense_submatrices(self) -> None:
        """
        Initializes dense submatrices based on count values.
        """

        for i in range(self.num_rows):
            cur_dense_submatrix = []
            flat_counts = []

            for j in range(self.num_buckets):
                for k in range(self.num_buckets):
                    flat_counts.append((self.count[i][j][k], (j, k)))

            flat_counts.sort(key=lambda x: x[0], reverse=True)

            for j in range(self.num_dense_submatrices):
                initial_submatrix = Submatrix(j, j, 0.0)
                cur_dense_submatrix.append(initial_submatrix)

            self.densest_matrices.append(cur_dense_submatrix)
        
    def get_anoedgelocal_score(self, src: int, dst: int) -> float:
        """
        Computes the minimum dsubgraph value for given source and destination nodes.

        Parameters:
        - src (int): Source node.
        - dst (int): Destination node.

        Returns:
        - float: Minimum dsubgraph value.
        """
        min_dsubgraph = float('inf')

        for i in range(self.num_rows):
            src_bucket = self.hash(src, i)
            dst_bucket = self.hash(dst, i)

            for j in range(self.num_dense_submatrices):
                if self.densest_matrices[i][j].checkAndAdd(src_bucket, dst_bucket, self.count[i]):
                    flag = True
                    del_cnt = -1
                    while flag:
                        flag = self.densest_matrices[i][j].checkAndDel(self.count[i])
                        del_cnt += 1

            cur_dsubgraph = 0.0
            for j in range(self.num_dense_submatrices):
                cur_likelihood = self.densest_matrices[i][j].getLikelihoodScore(src_bucket, dst_bucket, self.count[i])
                cur_dsubgraph += cur_likelihood

            min_dsubgraph = min(min_dsubgraph, cur_dsubgraph)
        return min_dsubgraph