import sys
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_tsp():
    # 5-node sample distance matrix (symmetric for simplicity)
    # 0: Start/End, 1, 2, 3, 4: Venues
    distance_matrix = [
        [0, 10, 15, 20, 25],
        [10, 0, 35, 25, 30],
        [15, 35, 0, 30, 20],
        [20, 25, 30, 0, 15],
        [25, 30, 20, 15, 0],
    ]

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print("Solution found!")
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            # Fix: solution.Value(routing.NextVar(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        print(f"Route: {route}")
        print(f"Total distance: {solution.ObjectiveValue()}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    try:
        solve_tsp()
    except Exception as e:
        print(f"Error: {e}")
