from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import logging

logger = logging.getLogger("Optimizer")

class VRPTWSolver:
    """
    Professional VRPTW Implementation.
    Optimizes routes based on distance, time windows, and service durations.
    """
    def __init__(self, 
                 distance_matrix: List[List[float]], 
                 time_windows: List[Tuple[int, int]], 
                 service_times: List[int],
                 depot_index: int = 0):
        self.distance_matrix = distance_matrix
        self.time_windows = time_windows
        self.service_times = service_times
        self.depot_index = depot_index

    def solve(self, time_limit_seconds: int = 10) -> Optional[Dict[str, Any]]:
        num_locations = len(self.distance_matrix)
        
        # 1. Initialize Manager and Model
        manager = pywrapcp.RoutingIndexManager(num_locations, 1, self.depot_index)
        routing = pywrapcp.RoutingModel(manager)

        # 2. Distance Callback (The cost of traveling between two points)
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(self.distance_matrix[from_node][to_node])

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # 3. Time Callback (Distance + Service Time at origin)
        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            # Service time is how long the user stays at the venue
            return int(self.distance_matrix[from_node][to_node]) + self.service_times[from_node]

        time_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.AddDimension(
            time_callback_index,
            120, # Max waiting time at a venue before opening (slack)
            1440, # Max travel time for the whole trip (minutes)
            False, 
            "Time"
        )
        time_dimension = routing.GetDimensionOrDie("Time")

        # 4. Apply Time Windows to each location
        for location_idx, (start, end) in enumerate(self.time_windows):
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(start, end)

        # 5. Search Parameters
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = time_limit_seconds

        # 6. Solve
        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            route = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            
            # Calculate arrival times based on the solver's CumulVar
            arrivals = []
            for node in route:
                arrivals.append(solution.Min(time_dimension.CumulVar(manager.NodeToIndex(node))))
                
            return {
                "success": True,
                "route": route,
                "total_distance": solution.ObjectiveValue(),
                "arrival_times": arrivals,
                "stop_details": [
                    {"node": node, "arrival": time} 
                    for node, time in zip(route, arrivals)
                ]
            }
        
        logger.error("VRPTW Solver could not find a feasible solution within constraints.")
        return None
