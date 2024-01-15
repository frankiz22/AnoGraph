AnoEdge-G and AnoEdge-L identify edge anomalies by examining if the mapped position of the received edge in a sketch matrix belongs to a dense submatrix. AnoEdge-G identifies a global dense submatrix, showing strong practical performance. Meanwhile, AnoEdge-L manages and updates a local dense submatrix around the matrix element, resulting in improved time complexity.

It is implemented with the class AnoedgeDetector. Attribute type allows to define either a global (AnoEdge-G) or local (AnoEdge-L) detecor.
With learn_one and score_one function

AnoGraph and AnoGraph-K identify graph anomalies by initially transforming the graph into a higher-order sketch and subsequently examining it for dense submatrices. AnoGraph utilizes a greedy approach to locate a dense submatrix, guaranteeing a 2-approximation on the density measure. Meanwhile, AnoGraph-K adeptly identifies dense submatrices around K strategically chosen matrix elements, demonstrating comparable practical performance.

It is implemented with the class AnographDetector. the score_one fucntion has a parameter method which is either normal (AnoGraph) or top-k (AnoGraph-K)

Experiments are doneon datasets:
DARPA
ISCX-IDS2012
CIC-IDS2018
CIC-DDoS2019
