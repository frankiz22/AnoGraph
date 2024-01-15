from river import anomaly
from river.anomaly.base import AnomalyDetector
from hcmsanoedgeglobal import HcmsAnoedgeGlobal
from hcmsanoedgelocal import HcmsAnoedgeLocal
from hcms import Hcms

class AnoedgeDetector(anomaly.base.AnomalyDetector):
    def __init__(self, rows: int, buckets: int, decay_factor: float, type: str, num_dense_submatrices: int = 1):
        """
        Initialize AnoedgeGlobal class.

        Args:
        - rows (int): Number of rows.
        - buckets (int): Number of buckets.
        - decay_factor (float): Decay factor.
        - type (str): global or local.
        - num_dense_submatrices (int): Number of dense submatrices.
        """

        self.decay_factor = decay_factor
        self.last_time = 0
        self.type = type

        if type == 'global':
            self.hcms = HcmsAnoedgeGlobal(rows, buckets)
        elif type == 'local':
            self.hcms = HcmsAnoedgeLocal(rows, buckets, num_dense_submatrices)
            self.hcms.initialize_dense_submatrices()
        else:
            ValueError(f"Invalid value: {type}. Value must be either local or global.")
    
    def get_rows(self):
        return self.hcms.num_rows
    
    def get_buckets(self):
        return self.hcms.num_buckets

    def learn_one(self, x: dict):
        """
        Add a new element x to the graph

        Parameters:
        - x (dict): Input to add to the graph.
        keys ares:
            - src : Source node
            - dst : Destination node
            - time: Time corresponding to the node

        """

        if x['time'] > self.last_time:
            self.hcms.decay(self.decay_factor)
        
        self.last_time = x['time']

        self.hcms.insert(x['src'], x['dst'], 1)
        
    def score_one(self, x: dict) -> float:
        """
        Calculate scores based on the records for an element x

        Parameters:
        - x (dict): Input to add to the graph.
        keys ares:
            - src : Source node
            - dst : Destination node
            - time: Time corresponding to the node

        Returns:
        - float: the anomaly score.
        """

        if self.type == 'global':
            return self.hcms.get_anoedgeglobal_score(x['src'], x['dst'])
        else:
            return self.hcms.get_anoedgelocal_score(x['src'], x['dst'])