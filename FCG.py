import numpy as np
import networkx as nx
from androguard.core.analysis.analysis import ExternalMethod
from Doc2vec import doc2vec

def getEdgeList(FCG) -> tuple:
    num_nodes = len(FCG.nodes())
    adj_matrix = np.zeros((num_nodes, num_nodes))

    # Xây dựng ma trận kề
    for edge in FCG.edges():
        source = edge[0]
        target = edge[1]
        source_index = list(FCG.nodes()).index(source)
        target_index = list(FCG.nodes()).index(target)
        adj_matrix[source_index][target_index] = 1
    ans = getEdgesFromAdjacencyMatrix(adj_matrix)
    return tuple(ans)

def getEdgesFromAdjacencyMatrix(adj_matrix):
    num_nodes = adj_matrix.shape[0]
    left_list = []
    right_list = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i][j] == 1:
                left_list.append(i)
                right_list.append(j)

    return [left_list, right_list]

def getFeatureMatrix(FCG):
    modelAPI = doc2vec.getModel('api')
    modelUser = doc2vec.getModel('user')

    feature_graph = {}
    for node in FCG.nodes:
        features = []
        if isinstance(node, ExternalMethod):
            name = str(node.class_name)[1:-1]
            features = modelAPI.infer_vector(name.split('/'))
        else:
            opcode_groups = set()
            for instr in node.get_instructions():
                opcode_groups.add(instr.get_name())
            features = modelUser.infer_vector(list(opcode_groups))
        feature_graph[node] = features
    # for k, v in feature_graph.items():
    #     print(f"{k}: \n{v}")
    # print(len(feature_graph.items()))
    feature_matrix = [x for x in feature_graph.values()]
    return feature_matrix