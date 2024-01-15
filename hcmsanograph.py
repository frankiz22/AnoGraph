from submatrix import Submatrix
from hcms import Hcms
import numpy as np

class HcmsAnograph(Hcms):
    def __init__(self, r: int, b: int):
        """
        Initializes an Hcms object.

        Parameters:
        - r (int): Number of rows.
        - b (int): Number of buckets

        """
        super().__init__(r, b)
    
    def get_anograph_density(self, mat: np.ndarray) -> float:
        """
        Computes the maximum density of a matrix by iteratively removing rows or columns.

        Parameters:
        - mat (numpy.ndarray): 2D array representing the matrix.

        Returns:
        - float: Maximum density of the matrix.
        """
        num_rows, num_cols = mat.shape
        
        row_flag = np.ones(num_rows, dtype=bool)
        col_flag = np.ones(num_cols, dtype=bool)

        row_sum = np.sum(mat, axis = 1)
        col_sum = np.sum(mat, axis = 0)

        marked_row = num_rows
        marked_col = num_cols

        total_sum = np.sum(row_sum)
        current_density = total_sum/np.sqrt(marked_row * marked_row)
        output = current_density

        for _ in range(num_rows + num_cols):
            
            min_row_idx = np.argmin(row_sum)

            min_col_idx = np.argmin(col_sum)

            if row_sum[min_row_idx] <= col_sum[min_col_idx]:
                row_flag[min_row_idx] = False
                row_sum[min_row_idx] = np.inf
                col_sum -= mat[min_row_idx,:]
                total_sum -= np.sum(mat[min_row_idx, col_flag])
                marked_row -= 1
            else:
                col_flag[min_col_idx] =False
                col_sum[min_col_idx] = np.inf
                row_sum -= mat[:, min_col_idx]
                total_sum -= np.sum(mat[row_flag, min_col_idx])
                marked_col -= 1
            
            if marked_col == 0 or marked_row == 0:
                break
            
            current_density = total_sum/np.sqrt(marked_row * marked_col)

            output = max(output, current_density)
            
        return output

    
    def get_subgraph_density(self, mat: np.ndarray, src: int, dst: int) -> float:
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
    
    def get_anograph_k_density(self, mat: np.ndarray, K: int) -> float:
        """
        Calculate the Anograph-K density based on the input matrix and subgraph count K.
        """
        num_subgraphs = K
        num_rows, num_cols = len(mat), len(mat[0])

        flat_mat = []
        for i in range(num_rows):
            for j in range(num_cols):
                flat_mat.append((mat[i][j], (i, j)))
        flat_mat.sort(key=lambda x: x[0], reverse=True)

        output_density = 0.0
        for idx in range(num_subgraphs):
            output_density = max(output_density, self.get_subgraph_density(mat, flat_mat[idx][1][0], flat_mat[idx][1][1]))

        return output_density
    

    def get_anograph_score(self) -> float:
        """
        Computes the minimum density score of a subgraph for a given algorithm.

        Parameters:
        - count (List[numpy.ndarray]): List of numpy arrays representing matrices.

        Returns:
        - float: Minimum density score of the subgraph.
        """
        min_dsubgraph = float('inf')
        for i in range(self.num_rows):
            cur_dsubgraph = self.get_anograph_density(self.count[i])
            min_dsubgraph = min(min_dsubgraph, cur_dsubgraph)
        return min_dsubgraph
    
    def get_anograph_k_score(self, k: int) -> float:
        """
        Computes the minimum density score of a subgraph for a given algorithm.

        Parameters:
        - count (List[numpy.ndarray]): List of numpy arrays representing matrices.

        Returns:
        - float: Minimum density score of the subgraph.
        """
        min_dsubgraph = float('inf')
        for i in range(self.num_rows):
            cur_dsubgraph = self.get_anograph_k_density(self.count[i], k)
            min_dsubgraph = min(min_dsubgraph, cur_dsubgraph)
        return min_dsubgraph
    

    





