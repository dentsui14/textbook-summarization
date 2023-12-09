import csv
import json
import itertools as it
import ast
# Each passage is represented by a tuple of (Name, {keyword:value})
# passage1: tuple[str, dict[str, float]], passage2: tuple[str, dict[str, float]]
# CSV is in the format of Name, {keyword:value}
def find_cosine_similarity(p1: dict[str,float], p2: dict[str,float]): # Returns value from 0 (not similar) to 1 (similar)
    keys1 = set(p1.keys())
    keys2 = set(p2.keys()) 
    union_keys = set(p1.keys()).union(set(p2.keys()))
    p1_norm = 0
    p2_norm = 0
    dot = 0
    for key in union_keys:
        if key in keys1:
            p1_norm += p1[key]**2
        if key in keys2:
            p2_norm += p2[key]**2
        if key in keys1 and key in keys2:
            dot += p1[key] * p2[key]
    if (p1_norm == 0 or p2_norm == 0):
        print("Error")
        return
    p1_norm = p1_norm ** .5
    p2_norm = p2_norm ** .5
    cosine = dot / p1_norm / p2_norm
    return cosine

def read_from_csv(path="keywords_paragraphs.csv"):
    list = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[1]
            dict = list_to_dict(ast.literal_eval(row[2]))
            list.append((name, dict))
    return list

def get_edges(arr: tuple[str, list[dict[str,float]]]):
    edge_list = [("source","target","value")]
    for pair in it.combinations(arr, 2):
        name1 = pair[0][0]
        name2 = pair[1][0]
        similarity = find_cosine_similarity(pair[0][1], pair[1][1])
        edge_list.append((name1, name2, similarity))
    return edge_list

def write_edges_to_csv(edge_list, path="graph_edges.csv"):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(edge_list)

def passages_to_edges():
    data = read_from_csv()
    edges = get_edges(data)
    write_edges_to_csv(edges)

def list_to_dict(arr):
    return_dict = {}
    for i, kw in enumerate(arr):
        return_dict[kw] = 1 - i / 11
    return return_dict

# p1 = ("1.1", {"signal": 1, "acoustic":.3})
# p2 = ("1.2", {"signal": .5})
# p3 = ("1.3", {"acoustic": 1})
# print(get_edges([p1, p2, p3]))
#[('source', 'target', 'value'), ('1.1', '1.2', 0.9578262852211513), ('1.1', '1.3', 0.2873478855663454), ('1.2', '1.3', 0.0)]

passages_to_edges()