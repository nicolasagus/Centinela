import heapq
import json
import sys
from typing import Dict, List, Tuple

class DependencyGraphNavigator:
    def __init__(self, adjacency_map: Dict[str, List[Tuple[str, float]]]):
        """
        adjacency_map: { "nodo_origen": [("nodo_destino", peso_tokens_o_costo)] }
        """
        self.graph = adjacency_map

    def shortest_path(self, start_node: str, target_node: str) -> Tuple[float, List[str]]:
        queue = [(0.0, start_node, [])]
        seen = set()
        min_dist = {start_node: 0.0}

        while queue:
            (cost, current, path) = heapq.heappop(queue)

            if current in seen:
                continue

            seen.add(current)
            path = path + [current]

            if current == target_node:
                return (cost, path)

            for neighbor, weight in self.graph.get(current, []):
                if neighbor in seen:
                    continue
                prev_cost = min_dist.get(neighbor, None)
                next_cost = cost + weight
                if prev_cost is None or next_cost < prev_cost:
                    min_dist[neighbor] = next_cost
                    heapq.heappush(queue, (next_cost, neighbor, path))

        return (float("inf"), [])

    def prune_context_subgraph(self, root_node: str, max_token_budget: float) -> List[str]:
        """
        Extrae exclusivamente los nodos cuyo camino minimo desde root_node
        no supere el presupuesto de tokens asignado por el Circuit Breaker.
        """
        distances = {root_node: 0.0}
        pq = [(0.0, root_node)]
        valid_nodes = []

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if curr_dist > max_token_budget:
                continue
            valid_nodes.append(u)

            for v, weight in self.graph.get(u, []):
                new_dist = curr_dist + weight
                if new_dist <= max_token_budget and (v not in distances or new_dist < distances[v]):
                    distances[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))

        return valid_nodes

if __name__ == "__main__":
    mock_dependencies = {
        "errors.ts": [("bucket.ts", 40.0)],
        "bucket.ts": [("index.ts", 10.0), ("bucket.test.ts", 120.0)],
        "bucket.test.ts": [("audit-log.json", 30.0)],
        "index.ts": []
    }
    navigator = DependencyGraphNavigator(mock_dependencies)
    cost, path = navigator.shortest_path("errors.ts", "audit-log.json")
    print(f"[GraphNavigator] Ruta minima calculada: {' -> '.join(path)} (Costo: {cost} tokens)")