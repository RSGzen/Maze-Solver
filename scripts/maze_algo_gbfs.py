import heapq
from itertools import permutations

def gbfs(grid, start, keys, end):
    def get_neighbors(index):
        neighbors = []
        x, y = grid.checkCellXandYIndex(index)
        # print(f"Getting neighbors for index {index} at coordinates ({x}, {y})")
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.num_cols and 0 <= ny < grid.num_rows:
                neighbor_index = grid.checkCellArrayIndex(nx, ny)
                if not grid.cell_array[neighbor_index].wall:  # Check if not a wall
                    neighbors.append(neighbor_index)
        # print(f"Neighbors: {neighbors}")
        return neighbors

    def heuristic(index, goal):
        x1, y1 = grid.checkCellXandYIndex(index)
        x2, y2 = grid.checkCellXandYIndex(goal)
        h = abs(x1 - x2) + abs(y1 - y2)
        # print(f"Heuristic from {index} to {goal} is {h}")
        return h

    def gbfs_single_source(start, goal):
        visited = set()
        pq = [(heuristic(start, goal), start)]
        prev = {index: None for index in range(grid.num_cols * grid.num_rows)}
        cost = {index: float('inf') for index in range(grid.num_cols * grid.num_rows)}
        cost[start] = 0

        while pq:
            current_priority, current_index = heapq.heappop(pq)
            if current_index in visited:
                continue
            visited.add(current_index)
            if current_index == goal:
                break
            for neighbor in get_neighbors(current_index):
                if neighbor not in visited:
                    additional_cost = 5 if grid.cell_array[neighbor].obstacle else 0
                    new_cost = cost[current_index] + 1 + additional_cost
                    if new_cost < cost[neighbor]:
                        cost[neighbor] = new_cost
                        heapq.heappush(pq, (heuristic(neighbor, goal), neighbor))
                        prev[neighbor] = current_index
        # print(f"Visited: {visited}")
        # print(f"Prev: {prev}")
        # print(f"Cost: {cost}")
        return prev, cost

    def reconstruct_path(prev, start, goal):
        path = []
        at = goal
        while at is not None:
            path.append(at)
            at = prev[at]
        path.reverse()
        # print(f"Reconstructed path: {path}")
        return path

    def find_shortest_path_through_keys(start, keys, end):
        if not keys:
            # If no keys, find the direct shortest path from start to end
            prev_from_start, cost_from_start = gbfs_single_source(start, end)
            path = reconstruct_path(prev_from_start, start, end)
            return path, cost_from_start[end]

        best_order = None
        best_distance = float('inf')
        best_path = []

        for order in permutations(keys):
            total_distance = 0
            current_start = start
            full_path = []

            for key in order:
                prev, cost = gbfs_single_source(current_start, key)
                if cost[key] == float('inf'):
                    break
                segment_path = reconstruct_path(prev, current_start, key)
                full_path.extend(segment_path[:-1])  # Add all but the last to avoid duplication
                total_distance += cost[key]
                current_start = key
            
            # Handle the final segment to the end point
            prev, cost = gbfs_single_source(current_start, end)
            if cost[end] == float('inf'):
                continue
            segment_path = reconstruct_path(prev, current_start, end)
            full_path.extend(segment_path)
            total_distance += cost[end]

            if total_distance < best_distance:
                best_order = order
                best_distance = total_distance
                best_path = full_path

        return best_path, best_distance

    path, path_cost = find_shortest_path_through_keys(start, keys, end)

    if path:
        grid.agent_position = path[-1]
        coordinate = [grid.checkCellXandYIndex(index) for index in path]
    else:
        coordinate = []

    # print(f"Final path: {path}, Path cost: {path_cost}") 
    return coordinate, path_cost