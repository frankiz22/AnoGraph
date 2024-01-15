import numpy as np

class Submatrix:
    def __init__(self, row_idx, col_idx, value):
        """
        Initialize a Submatrix object.

        Parameters:
        - row_idx (int): Index of the row.
        - col_idx (int): Index of the column.
        - value (float): Initial value for the submatrix.

        """
        
        self.rows_sum = {row_idx: value}
        self.cols_sum = {col_idx: value}
        self.submatrix_sum = value
        self.submatrix_rows_count = 1
        self.submatrix_cols_count = 1
    
    def getSubmatrixSum(self) -> float:
        """Return the sum of the submatrix."""
        return self.submatrix_sum

    def updateSubmatrixSum(self, value: float) -> None:
        """Update the submatrix sum by adding a specified value."""
        self.submatrix_sum += value

    def getSubmatrixRowsCount(self) -> int:
        """Return the number of rows in the submatrix."""
        return self.submatrix_rows_count

    def getSubmatrixColsCount(self) -> int:
        """Return the number of columns in the submatrix."""
        return self.submatrix_cols_count
    

    def addSubmatrixRow(self, row_idx: int, value: float, mat: np.ndarray) -> None:
        """
        Add a row to the submatrix and update column sums using the provided matrix.
        
        Parameters:
        - row_idx (int): Index of the row to be added.
        - value (float): Value to be assigned for the row.
        - mat (np.ndarray): Numpy array representing the matrix.

        """
        self.submatrix_rows_count += 1
        self.rows_sum[row_idx] = value
        for col_idx in self.cols_sum:
            self.cols_sum[col_idx] += mat[row_idx][col_idx]

    def addSubmatrixCol(self, col_idx: int, value: float, mat: np.ndarray) -> None:
        """
        Add a column to the submatrix and update row sums using the provided matrix.
        
        Parameters:
        - col_idx (int): Index of the column to be added.
        - value (float): Value to be assigned for the column.
        - mat (np.ndarray): Numpy array representing the matrix.

        """
        self.submatrix_cols_count += 1
        self.cols_sum[col_idx] = value
        for row_idx in self.rows_sum:
            self.rows_sum[row_idx] += mat[row_idx][col_idx]
    
    def delSubmatrixRow(self, row_idx: int, mat: np.ndarray) -> None:
        """
        Delete a row from the submatrix and update column sums using the provided matrix.
        
        Parameters:
        - row_idx (int): Index of the row to be deleted.
        - mat (np.ndarray): Numpy array representing the matrix.

        """
        self.submatrix_rows_count -= 1
        del self.rows_sum[row_idx]
        for col_idx in self.cols_sum:
            self.cols_sum[col_idx] -= mat[row_idx][col_idx]

    def delSubmatrixCol(self, col_idx: int, mat: np.ndarray) -> None:
        """
        Delete a column from the submatrix and update row sums using the provided matrix.
        
        Parameters:
        - col_idx (int): Index of the column to be deleted.
        - mat (np.ndarray): Numpy array representing the matrix.

        """
        self.submatrix_cols_count -= 1
        del self.cols_sum[col_idx]
        for row_idx in self.rows_sum:
            self.rows_sum[row_idx] -= mat[row_idx][col_idx]
    
    def getSubmatrixRowSum(self, row_idx: int) -> float:
        """
        Return the sum of a specific row in the submatrix.
        
        Parameters:
        - row_idx (int): Index of the row.

        Returns:
        - float: Sum of the specified row.

        """
        return self.rows_sum.get(row_idx, 0.0)

    def getSubmatrixColSum(self, col_idx: int) -> float:
        """
        Return the sum of a specific column in the submatrix.
        
        Parameters:
        - col_idx (int): Index of the column.

        Returns:
        - float: Sum of the specified column.

        """
        return self.cols_sum.get(col_idx, 0.0)

    def updateSubmatrixRowSum(self, row_idx: int, value: float) -> None:
        """
        Update the sum of a specific row in the submatrix by adding a specified value.
        
        Parameters:
        - row_idx (int): Index of the row.
        - value (float): Value to be added to the row sum.

        """
        self.rows_sum[row_idx] = self.rows_sum.get(row_idx, 0.0) + value

    def updateSubmatrixColSum(self, col_idx: int, value: float) -> None:
        """
        Update the sum of a specific column in the submatrix by adding a specified value.
        
        Parameters:
        - col_idx (int): Index of the column.
        - value (float): Value to be added to the column sum.

        """
        self.cols_sum[col_idx] = self.cols_sum.get(col_idx, 0.0) + value

    def getDensity(self) -> float:
        """
        Calculate and return the density of the submatrix.
        
        Returns:
        - float: Density of the submatrix.

        """
        return self.submatrix_sum / np.sqrt(self.submatrix_rows_count * self.submatrix_cols_count)



    def checkAndAdd(self, row_idx: int, col_idx: int, mat: np.ndarray) -> bool:
        """
        Checks if adding a specific row and column increases the submatrix density. 
        If it does, adds the row and/or column to the submatrix.
        
        Parameters:
        - row_idx (int): Index of the row.
        - col_idx (int): Index of the column.
        - mat (np.ndarray): Numpy array representing the matrix.

        Returns:
        - bool: True if the addition increases density and row/column is added, False otherwise.

        """
        cur_rows = self.submatrix_rows_count
        cur_cols = self.submatrix_cols_count
        cur_submatrix_row_sum = 0.0
        cur_submatrix_col_sum = 0.0
        cur_submatrix_sum = 0.0

        row_flag = row_idx in self.rows_sum
        col_flag = col_idx in self.cols_sum

        if row_flag and col_flag:
            self.submatrix_sum += 1.0
            self.rows_sum[row_idx] += 1.0
            self.cols_sum[col_idx] += 1.0
            return False

        if not row_flag:
            cur_submatrix_row_sum = np.sum(mat[row_idx, list(self.cols_sum.keys())])
            cur_rows += 1

        if not col_flag:
            cur_submatrix_col_sum = np.sum(mat[list(self.rows_sum.keys()), col_idx])
            cur_cols += 1

        if not row_flag and not col_flag:
            cur_submatrix_sum = self.submatrix_sum + cur_submatrix_row_sum + cur_submatrix_col_sum + mat[row_idx, col_idx]
        else:
            cur_submatrix_sum = self.submatrix_sum + cur_submatrix_row_sum + cur_submatrix_col_sum

        if self.getDensity() < cur_submatrix_sum / np.sqrt(cur_rows * cur_cols):
            if not row_flag and not col_flag:
                self.addSubmatrixRow(row_idx, cur_submatrix_row_sum + mat[row_idx, col_idx], mat)
                #####################################################################################
                self.addSubmatrixCol(col_idx, cur_submatrix_col_sum + mat[row_idx, col_idx], mat)

            elif not row_flag:
                self.addSubmatrixRow(row_idx, cur_submatrix_row_sum, mat)
            elif not col_flag:
                self.addSubmatrixCol(col_idx, cur_submatrix_col_sum, mat)
            self.submatrix_sum = cur_submatrix_sum
            return True
        return False
    

    def checkAndDel(self, mat: np.ndarray) -> bool:
        """
        Checks if deleting a row or column increases the submatrix density.
        If it does, deletes the row/column with the minimum sum from the submatrix.

        Parameters:
        - mat (np.ndarray): Numpy array representing the matrix.

        Returns:
        - bool: True if a row or column is deleted, False otherwise.

        """
        min_row = (-1, float('inf'))
        if self.submatrix_rows_count > 1:
            for row_idx, row_sum in self.rows_sum.items():
                if row_sum < min_row[1]:
                    min_row = (row_idx, row_sum)

        min_col = (-1, float('inf'))
        if self.submatrix_cols_count > 1:
            for col_idx, col_sum in self.cols_sum.items():
                if col_sum < min_col[1]:
                    min_col = (col_idx, col_sum)

        #row_del_density = 0.0
        row_del_density = float('inf')

        if min_row[0] != -1:
            row_del_density = (self.submatrix_sum - min_row[1]) / np.sqrt((self.submatrix_rows_count - 1) * self.submatrix_cols_count)

        #col_del_density = 0.0
        col_del_density = float('inf')
        if min_col[0] != -1:
            col_del_density = (self.submatrix_sum - min_col[1]) / np.sqrt(self.submatrix_rows_count * (self.submatrix_cols_count - 1))

        cur_density = self.getDensity()

        if cur_density > row_del_density and col_del_density < row_del_density:
            self.delSubmatrixRow(min_row[0], mat)
            self.submatrix_sum -= min_row[1]
            return True
        
        elif cur_density > col_del_density and row_del_density < col_del_density:
            self.delSubmatrixCol(min_col[0], mat)
            self.submatrix_sum -= min_col[1]
            return True

        return False
    

    def decay(self, decay_factor: float) -> None:
        """
        Decay the submatrix and associated sums by a specified decay factor.

        Parameters:
        - decay_factor (float): Factor by which the submatrix and sums are decayed.

        """
        self.submatrix_sum *= decay_factor
        for row_idx in self.rows_sum:
            self.rows_sum[row_idx] *= decay_factor
        for col_idx in self.cols_sum:
            self.cols_sum[col_idx] *= decay_factor


    def getLikelihoodScore(self, row_idx: int, col_idx: int, mat: np.ndarray) -> float:
        """
        Calculate the likelihood score for a given row and column index.

        Parameters:
        - row_idx (int): Index of the row.
        - col_idx (int): Index of the column.
        - mat (np.ndarray): Numpy array representing the matrix.

        Returns:
        - float: The likelihood score for the given row and column.

        """
        row_indices = list(self.rows_sum.keys())
        col_indices = list(self.cols_sum.keys())

        score = np.sum(mat[row_indices, col_idx]) + np.sum(mat[row_idx, col_indices])

        row_flag = row_idx in self.rows_sum
        col_flag = col_idx in self.cols_sum

        ctr = len(row_indices) + len(col_indices)

        if row_flag and col_flag:
            score -= mat[row_idx, col_idx]
            ctr -= 1

        return score / ctr if ctr != 0 else 0.0
    
    def getRows(self):
        """
        Get a list of rows in the submatrix.

        Returns:
        - list: List of rows.

        """
        return list(self.rows_sum.keys())

    def getCols(self):
        """
        Get a list of columns in the submatrix.

        Returns:
        - list: List of columns.

        """
        return list(self.cols_sum.keys())



