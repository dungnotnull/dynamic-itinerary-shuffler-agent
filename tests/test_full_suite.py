import pytest
from app.services.optimizer import VRPTWSolver
from app.core.encryption import encryption_manager

def test_vrptw_solver_complex():
    # 4 Nodes: Depot, Venue A, Venue B, Venue C
    dist_matrix = [
        [0, 10, 20, 30], # Depot
        [10, 0, 15, 25], # A
        [20, 15, 0, 10], # B
        [30, 25, 10, 0]  # C
    ]
    # Narrow time windows to force a specific order
    time_windows = [
        (0, 1000), # Depot
        (10, 30),   # A must be first
        (40, 60),   # B must be second
        (70, 100),  # C must be third
    ]
    service_times = [0, 10, 10, 10]
    
    solver = VRPTWSolver(dist_matrix, time_windows, service_times)
    result = solver.solve()
    
    assert result is not None
    assert result["route"] == [0, 1, 2, 3, 0]

def test_encryption_roundtrip():
    data = {"pref": "artsy", "budget": "high"}
    encrypted = encryption_manager.encrypt_data(data)
    decrypted = encryption_manager.decrypt_data(encrypted)
    assert data == decrypted
