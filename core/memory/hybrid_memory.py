import os
import sys
from typing import Dict, List, Tuple

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from vector_memory import LocalVectorMemory
# Importacion dinamica para graph-navigator con guion medio
import importlib.util
spec = importlib.util.spec_from_file_location("graph_navigator", os.path.join(CURRENT_DIR, "graph-navigator.py"))
graph_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph_mod)
DependencyGraphNavigator = graph_mod.DependencyGraphNavigator

class HybridMemoryFusion:
    def __init__(self, dependency_graph: Dict[str, List[Tuple[str, float]]]):
        self.vector_engine = LocalVectorMemory()
        self.graph_navigator = DependencyGraphNavigator(dependency_graph)

    def index_document(self, doc_id: str, content: str):
        self.vector_engine.add_document(doc_id, content)

    def prepare(self):
        self.vector_engine.build_index()

    def resolve_context(self, natural_query: str, token_budget: float = 16384.0) -> Dict[str, any]:
        # 1. Recuperacion semantica (Punto de entrada)
        top_matches = self.vector_engine.search(natural_query, top_k=1)
        if not top_matches:
            return {"entry_node": None, "subgraph": [], "cost": 0.0}

        entry_node, similarity = top_matches[0]

        # 2. Poda determinista por camino minimo (Dijkstra)
        pruned_nodes = self.graph_navigator.prune_context_subgraph(entry_node, token_budget)

        return {
            "query": natural_query,
            "entry_node": entry_node,
            "entry_similarity": similarity,
            "pruned_subgraph": pruned_nodes,
            "token_budget": token_budget
        }

if __name__ == "__main__":
    mock_dependencies = {
        "errors.ts": [("bucket.ts", 40.0)],
        "bucket.ts": [("index.ts", 10.0), ("bucket.test.ts", 120.0)],
        "bucket.test.ts": [("audit-log.json", 30.0)],
        "circuit_breaker.py": [],
        "index.ts": []
    }

    fusion = HybridMemoryFusion(mock_dependencies)
    fusion.index_document("errors.ts", "Network timeout and token bucket rate limit exceeded errors.")
    fusion.index_document("bucket.ts", "TokenBucket class implementation with capacity and refill rate in TypeScript.")
    fusion.index_document("circuit_breaker.py", "Circuit breaker state machine monitor stopping infinite loops.")
    fusion.prepare()

    query = "rate limiting errors"
    result = fusion.resolve_context(query, token_budget=150.0)

    print(f"[HybridFusion] Query: '{result['query']}'")
    print(f"  -> Nodo de entrada (Vector): {result['entry_node']} (Sim: {result['entry_similarity']})")
    print(f"  -> Nodos podados (Dijkstra <= {result['token_budget']} tokens): {result['pruned_subgraph']}")