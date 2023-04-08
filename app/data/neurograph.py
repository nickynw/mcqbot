"""Generates a graph from some sample data"""
import networkx as nx

data = { "Neurotransmitter" : ["Serotonin",'Glycine', 'Glutamate', 'GABA', 'Dopamine', 'Epinephrine'],
          "Serotonin" : [],
          "Glycine" : [],
          "Glutamate" : [],
          "GABA" : [],
          'Epinephrine' : [],
          'Dopamine': [],
          'Serine' : [],
          'Histadine': [],
          'Amino Acid': ['Glycine', 'Glutamate', 'Serine', 'Histadine'],
          "Monoamine" : ['Serotonin', 'Epinephrine', 'Dopamine'],
          'L-tryptophan': ['Serotonin'],
          'L-DOPA': ['Dopamine'],
          '5-hydroxytryptophan': ['Serotonin'],
          'Vitamin C': ['Serotonin', 'L-tryptophan', '5-hydroxytryptophan', 'L-DOPA', 'Dopamine'],
          'Precursor': ['L-tryptophan', 'L-DOPA', '5-hydroxytryptophan'],
          'GABA Receptor':['GABA','Muscimol'],
          'Muscimol': []
} 

def graph() -> nx.DiGraph:
    """
    Creates a network x graph from data.

    Returns:
        nx.DiGraph: a directed graph containing nodes representing units of information
    """
    G = nx.DiGraph()
    for item, edges in data.items():
        G.add_node(item)
        for edge in edges:
            G.add_edge(item, edge)
    return G
