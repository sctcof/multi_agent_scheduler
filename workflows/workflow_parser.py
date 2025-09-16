# workflows/workflow_parser.py
import yaml
from .workflow import Workflow, Node, Edge

class WorkflowParser:
    @staticmethod
    def from_yaml(yaml_str: str) -> Workflow:
        data = yaml.safe_load(yaml_str)
        workflow = Workflow(data["workflow"])
        for node_data in data["nodes"]:
            node = Node(
                id=node_data["id"],
                agent_type=node_data["agent_type"],
                config=node_data["config"]
            )
            workflow.add_node(node)
        for edge_data in data["edges"]:
            edge = Edge(**edge_data)
            workflow.add_edge(edge)
        workflow.start_node = data["start_node"]
        return workflow

    @staticmethod
    def from_file(filepath: str) -> Workflow:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return WorkflowParser.from_yaml(content)