# workflows/workflow.py
from typing import Dict, Any, List
from dataclasses import dataclass
import yaml

@dataclass
class Node:
    id: str
    agent_type: str
    config: Dict[str, Any]

@dataclass
class Edge:
    source: str
    target: str
    condition: str = "always"

class Workflow:
    def __init__(self, name: str):
        self.name = name
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        self.start_node: str = None

    def add_node(self, node: Node):
        self.nodes.append(node)
        if not self.start_node:
            self.start_node = node.id

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def to_yaml(self) -> str:
        data = {
            "workflow": self.name,
            "nodes": [{"id": n.id, "agent_type": n.agent_type, "config": n.config} for n in self.nodes],
            "edges": [{"source": e.source, "target": e.target, "condition": e.condition} for e in self.edges],
            "start_node": self.start_node
        }
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    def save_to_yaml(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_yaml())