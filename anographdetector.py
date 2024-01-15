from river import anomaly
from river.anomaly.base import AnomalyDetector
from hcmsanograph import HcmsAnograph
from hcms import Hcms

class AnographDetector(anomaly.base.AnomalyDetector):
    def __init__(self, rows: int, buckets: int):
        """
        Initialize AnoedgeGlobal class.

        Args:
        - rows (int): Number of rows.
        - buckets (int): Number of buckets.
        """

        self.hcms = HcmsAnograph(rows, buckets)
    
    def get_rows(self):
        return self.hcms.num_rows
    
    def get_buckets(self):
        return self.hcms.num_buckets

    def learn_one(self, x: dict):
        return
        
    def score_one(self, x: dict, method: str = 'normal', k:int = None) -> float:
        """
        Calculate anomaly scre of a graph described by x

        Parameters:
        - x (dict): Input to add to the graph.
        keys ares:
            - src : list of Source node
            - dst : list of Destination node
        - method (str) method used to get the score either normal or top-k

        Returns:
        - float: the anomaly score.
        """
        self.hcms.clear()
        for i in range(len(x['src'])):
            self.hcms.insert(x['src'][i], x['dst'][i], 1)
            
        
    
        if method == 'normal':
            return self.hcms.get_anograph_score()
        
        elif method == 'top-k':
            if k is None:
                ValueError(f"k can't be None when using top-k method.")
                return
            else:
                return self.hcms.get_anograph_k_score(k)
        else:
            ValueError(f"Invalid value: {type}. Value must be either local or global.")

        