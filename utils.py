from typing import List, Tuple, Dict
import numpy as np
import pandas as pd
import numpy as np

import os

def compute_labels(data_base_path: str, dataset_name: str, time_window: int, edge_threshold: int) -> List[int]:
    """
    Compute labels for each graph based on the dataset provided.

    Args:
    - data_base_path (str): Path to the base directory containing dataset files.
    - dataset_name (str): The name of the dataset.
    - time_window (int): Time window used to delimit graphs.
    - edge_threshold (int): Minimum number of anomalous edges for the graph to be considered anomalous.
    

    Returns:
    - List[int]: A list of computed labels.
    """
    records = []
    graphs_file = f"{data_base_path}/{dataset_name}/Data.csv"
    with open(graphs_file, "r") as f:
        for line in f:
            if len(line) <= 1:
                continue
            src, dst, time = line.split("\n")[0].split(",")
            records.append((int(src), int(dst), int(time)))

    labels = []
    labels_file = f"{data_base_path}/{dataset_name}/Label.csv"
    with open(labels_file, "r") as f:
        for line in f:
            if len(line) <= 1:
                continue
            label = line.split("\n")[0]
            labels.append(int(label))

    assert len(records) == len(labels)

    record_labels = [(record[0], record[1], record[2], label) for record, label in zip(records, labels)]

    data = pd.DataFrame(np.array(record_labels))

    labels = []
    data[2] = (data[2]/time_window).astype(int)
    for i in pd.unique(data[2]):
        labels.append(sum(data[data[2]==i][3]))

    labels = np.array(labels)
    labels = labels >= edge_threshold
    labels = labels * 1

    return labels

def compute_graphs(data_base_path: str, dataset_name: str, time_window: int, edge_threshold: int) -> List[Tuple[List[int], List[int]]]:
    """
    Compute graphs based on the dataset information, time window, and edge threshold.

    Args:
    - data_base_path (str): Path to the base directory containing dataset files.
    - dataset_name (str): The name of the dataset.
    - time_window (int): Time window used to delimit graphs.
    - edge_threshold (int): Minimum number of anomalous edges for the graph to be considered anomalous.
    
    Returns:
    - List[Tuple[List[int], List[int]]]: A list of tuples representing computed graphs.
    """
    graphs = []
    graphs_file = f"{data_base_path}/{dataset_name}/Data.csv"

    with open(graphs_file, "r") as graphs_file_ptr:
        cur_time = 0
        cur_src, cur_dst = [], []
        for line in graphs_file_ptr:
            s, d, t = map(int, line.strip().split(','))
            if t // time_window != cur_time:
                graphs.append((cur_src, cur_dst))
                cur_time = t // time_window
                cur_src, cur_dst = [], []
            cur_src.append(s)
            cur_dst.append(d)

    graphs.append((cur_src, cur_dst)) 
    return graphs

def compute_and_save_labels():
    """
    Compute labels for each dataset in a dataset list for each time_window and edge_threshold.
    """
    dataset_list = ['DARPA', 'DDOS2019', 'IDS2018', 'ISCX']
    time_windows = [15, 30, 60, 60]
    edge_thresholds = [25, 50, 50, 100]
    data_base_path = 'DATA'

    
    for dataset_name in dataset_list:
        for time_window, edge_threshold in zip(time_windows, edge_thresholds):
            labels = compute_labels(data_base_path, dataset_name, time_window, edge_threshold)
            label_file = f"{data_base_path}/{dataset_name}/Label_{time_window}_{edge_threshold}.csv"

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(label_file), exist_ok=True)

            # Save labels to file
            with open(label_file, "w") as file:
                file.write('\n'.join(map(str, labels)))


def load_graph_data(data_base_path: str, dataset_name: str, time_window: int, edge_threshold: int) -> Tuple[List[Dict[str, List[int]]], List[int]]:
    """
    Load graph data and corresponding labels for a specific dataset, time window, and edge threshold.

    Args:
    - data_base_path (str): Base path containing dataset files.
    - dataset_name (str): The name of the dataset.
    - time_window (int): Time window used to delimit graphs.
    - edge_threshold (int): Threshold for edges.

    Returns:
    - Tuple[List[Dict[str, Any]], List[int]]: A tuple containing loaded graph records (as dictionaries) and labels.
    """
    graphs = compute_graphs(data_base_path, dataset_name, time_window, edge_threshold)

    label_file = f"{data_base_path}/{dataset_name}/Label_{time_window}_{edge_threshold}.csv"

    # Load labels from file
    with open(label_file, "r") as file:
        labels = [int(line.strip()) for line in file]

    records = []
    for src, dst in graphs:
        records.append({'src': src, 'dst': dst})

    return records, labels