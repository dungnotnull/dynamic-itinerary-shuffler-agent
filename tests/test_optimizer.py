import pytest
from app.services.optimizer import VRPTWSolver

def test_vrptw_solver_basic():
    dist_matrix = [
        [0, 10, 20],
        [10, 0, 15],
        [20, 15, 0]
    ]
    time_windows = [(0, 100), (0, 100), (0, 100)]
    service_times = [0, 10, 10]
    
    solver = VRPTWSolver(dist_matrix, time_windows, service_times)
    result = solver.solve()
    
    assert result["success"] is True
    assert result["route"] == [0, 1, 2, 0] # Optimal route for this matrix
