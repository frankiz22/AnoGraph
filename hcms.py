from submatrix import Submatrix
import numpy as np

class Hcms:
    def __init__(self, r: int, b: int):
        """
        Initializes an Hcms object.

        Parameters:
        - r (int): Number of rows.
        - b (int): Number of buckets.

        """
        self.num_rows = r
        self.num_buckets = b
        
        self.hash_a = np.random.randint(1, b, size=r)
        self.hash_b = np.random.randint(0, b, size=r)
        self.count = np.zeros((r, b, b))


    def clear(self) -> None:
        """
        Resets the count attribute to a three-dimensional array filled with zeros.
        """
        self.count = np.zeros((self.num_rows, self.num_buckets, self.num_buckets))


    def hash(self, elem: int, i: int) -> int:
        resid = (elem * self.hash_a[i] + self.hash_b[i]) % self.num_buckets
        return resid + self.num_buckets if resid < 0 else resid

    def insert(self, source_node: int, destination_node: int, edge_weight: float):
        """
        Inserts a weighted edge value into the count matrix based on source and destination nodes.

        Parameters:
        - source_node (int): Source node.
        - destination_node (int): Destination node.
        - edge_weight (float): Weight of the edge to be inserted.

        """
        source_buckets = np.array([self.hash(source_node, i) for i in range(self.num_rows)])
        destination_buckets = np.array([self.hash(destination_node, i) for i in range(self.num_rows)])

        self.count[np.arange(self.num_rows), source_buckets, destination_buckets] += edge_weight
    
    def remove(self, source_node: int, destination_node: int, edge_weight: float):
        """
        Remove a weighted edge value from the count matrix based on source and destination nodes.

        Parameters:
        - source_node (int): Source node.
        - destination_node (int): Destination node.
        - edge_weight (float): Weight of the edge to be inserted.

        """
        source_buckets = np.array([self.hash(source_node, i) for i in range(self.num_rows)])
        destination_buckets = np.array([self.hash(destination_node, i) for i in range(self.num_rows)])

        self.count[np.arange(self.num_rows), source_buckets, destination_buckets] -= edge_weight
    
    def get_count(self, source_node: int, destination_node: int) -> float:
        """
        Returns the minimum count value (an approximation of the weight of the edge) between source and destination nodes.

        Parameters:
        - source_node (int): Source node.
        - destination_node (int): Destination node.

        Returns:
        - float: Minimum count value between the nodes.
        """

        min_count = np.inf

        a_buckets = np.array([self.hash(source_node, i) for i in range(self.num_rows)])
        b_buckets = np.array([self.hash(destination_node, i) for i in range(self.num_rows)])

        min_count = np.min(self.count[np.arange(self.num_rows), a_buckets, b_buckets])

        return min_count

    def decay(self, decay_factor: float) -> None:
        """
        Decays the count values and optionally decays the densest_matrices using NumPy operations.

        Parameters:
        - decay_factor (float): Factor to decay the count values.
        """
        self.count *= decay_factor

    
    

    
