import heapq
from itertools import permutations

def dijkstra(grid, start, keys, end):
    def get_neighbors(index):
        # Define a function to get neighboring cells of a given index
        neighbors = []
        x, y = grid.checkCellXandYIndex(index)  
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.num_cols and 0 <= ny < grid.num_rows:
                neighbor_index = grid.checkCellArrayIndex(nx, ny)
                if not grid.cell_array[neighbor_index].wall:  # Check if not a wall
                    neighbors.append(neighbor_index)
        return neighbors

    def dijkstra_single_source(start):
        # Implement Dijkstra's algorithm to find shortest paths from a single source
        distances = {index: float('inf') for index in range(grid.num_cols * grid.num_rows)}
        distances[start] = 0
        prev = {index: None for index in range(grid.num_cols * grid.num_rows)}
        pq = [(0, start)]  # Priority queue for storing distances and vertices
        while pq:
            current_distance, current_index = heapq.heappop(pq)
            if current_distance > distances[current_index]:
                continue
            for neighbor in get_neighbors(current_index):
                additional_cost = 6 if grid.cell_array[neighbor].obstacle else 1  # Additional cost for obstacles
                distance = current_distance + additional_cost
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    prev[neighbor] = current_index
                    heapq.heappush(pq, (distance, neighbor))
        return distances, prev

    def reconstruct_path(prev, start, goal):
        # Reconstruct the shortest path from previous node dictionary
        path = []
        at = goal
        while at is not None:
            path.append(at)
            at = prev[at]
        path.reverse()
        return path

    def find_shortest_path_through_keys(start, keys, end):
        # Find the shortest path through a set of keys in a specific order
        distances_from_start, prev_from_start = dijkstra_single_source(start)
        all_distances = {key: dijkstra_single_source(key)[0] for key in keys}
        all_prev = {key: dijkstra_single_source(key)[1] for key in keys}

        def calculate_total_distance(order):
            # Calculate total distance for a given order of keys
            total_distance = 0
            total_distance += distances_from_start[order[0]]
            for i in range(len(order) - 1):
                    total_distance += all_distances[order[i]][order[i + 1]]
            total_distance += all_distances[order[-1]][end]
            return total_distance

        best_order = None
        best_distance = float('inf')
        for order in permutations(keys):
            total_distance = calculate_total_distance(order)
            if total_distance < best_distance:
                best_order = order
                best_distance = total_distance

        if best_order is not None:
            path = reconstruct_path(prev_from_start, start, best_order[0])
            for i in range(len(best_order) - 1):
                path.extend(reconstruct_path(all_prev[best_order[i]], best_order[i], best_order[i + 1])[1:])
            path.extend(reconstruct_path(all_prev[best_order[-1]], best_order[-1], end)[1:])
            return path, best_distance
        else:
            return None

    # Call the function to find the shortest path through keys
    path, path_cost = find_shortest_path_through_keys(start, keys, end)

    if path:
        # Update the grid's agent position if a path is found
        grid.agent_position = path[-1]
        coordinate = [grid.checkCellXandYIndex(index) for index in path]
    return coordinate, path_cost