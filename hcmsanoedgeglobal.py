from submatrix import Submatrix
from hcms import Hcms
import numpy as np

class HcmsAnoedgeGlobal(Hcms):
    def __init__(self, r: int, b: int):
        """
        Initializes an Hcms object.

        Parameters:
        - r (int): Number of rows.
        - b (int): Number of buckets

        """
        super().__init__(r, b)
    
    def find_max(self, slice_sum, flag):

        indices = np.where(~flag)[0]
        valid_values = slice_sum[indices]
        max_row_index = indices[np.argmax(valid_values)]
        return max_row_index, slice_sum[max_row_index]
    


    def get_anoedgeglobal_density(self, mat: np.ndarray, src: int, dst: int) -> float:
        num_rows, num_cols = mat.shape

        row_flag = np.full(num_rows, False)
        col_flag = np.full(num_cols, False)

        row_slice_sum = mat[:, dst].copy()
        col_slice_sum = mat[src, :].copy()

        row_flag[src] = True
        col_flag[dst] = True
        row_slice_sum[src] = mat[src, dst]
        col_slice_sum[dst] = mat[src, dst]

        max_row = (-1, -1.0)
        for i in range(num_rows):
            if not row_flag[i] and row_slice_sum[i] >= max_row[1]:
                max_row = (i, row_slice_sum[i])

        max_col = (-1, -1.0)
        for i in range(num_cols):
            if not col_flag[i] and col_slice_sum[i] >= max_col[1]:
                max_col = (i, col_slice_sum[i])

        marked_rows = 1
        marked_cols = 1

        cur_mat_sum = mat[src, dst]
        output = cur_mat_sum / np.sqrt(marked_rows * marked_cols)

        ctr = num_rows + num_cols - 2
        while ctr > 0:
            if max_row[1] >= max_col[1]:
                row_flag[max_row[0]] = True
                marked_rows += 1

                max_col = (-1, -1.0)
                for i in range(num_cols):
                    if col_flag[i]:
                        cur_mat_sum += mat[max_row[0], i]
                    else:
                        col_slice_sum[i] += mat[max_row[0], i]
                        if col_slice_sum[i] >= max_col[1]:
                            max_col = (i, col_slice_sum[i])

                max_row = (-1, -1.0)
                for i in range(num_rows):
                    if not row_flag[i] and row_slice_sum[i] >= max_row[1]:
                        max_row = (i, row_slice_sum[i])
            else:
                col_flag[max_col[0]] = True
                marked_cols += 1

                max_row = (-1, -1.0)
                for i in range(num_rows):
                    if row_flag[i]:
                        cur_mat_sum += mat[i, max_col[0]]
                    else:
                        row_slice_sum[i] += mat[i, max_col[0]]
                        if row_slice_sum[i] >= max_row[1]:
                            max_row = (i, row_slice_sum[i])

                max_col = (-1, -1.0)
                for i in range(num_cols):
                    if not col_flag[i] and col_slice_sum[i] >= max_col[1]:
                        max_col = (i, col_slice_sum[i])

            output = max(output, cur_mat_sum / np.sqrt(marked_rows * marked_cols))
            ctr -= 1

        return output

    
    def get_anoedgeglobal_score(self, src: int, dst: int) -> float:
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
            cur_dsubgraph = self.get_anoedgeglobal_density(self.count[i], src_bucket, dst_bucket)
            min_dsubgraph = min(min_dsubgraph, cur_dsubgraph)

        return min_dsubgraph