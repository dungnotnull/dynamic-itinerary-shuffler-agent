import pytest
from app.core.encryption import encryption_manager
from app.services.optimizer import VRPTWSolver
from app.services.venue_ranker import VenueRanker
import numpy as np

def test_encryption_security():
    secret_data = {"user_id": 1, "pref": "loves quiet cafes", "budget": "medium"}
    encrypted = encryption_manager.encrypt_data(secret_data)
    assert encrypted != str(secret_data)
    decrypted = encryption_manager.decrypt_data(encrypted)
    assert decrypted == secret_data

def test_vrptw_solver_edge_cases():
    # Case 1: Impossible time window
    dist_matrix = [[0, 10], [10, 0]]
    time_windows = [(0, 100), (1000, 1100)] 
    service_times = [0, 10]
    solver = VRPTWSolver(dist_matrix, time_windows, service_times)
    result = solver.solve()
    assert result is None

    # Case 2: Single stop
    dist_matrix_single = [[0, 5], [5, 0]]
    time_windows_single = [(0, 100), (0, 100)]
    service_times_single = [0, 10]
    solver_single = VRPTWSolver(dist_matrix_single, time_windows_single, service_times_single)
    result_single = solver_single.solve()
    assert result_single["route"] == [0, 1, 0]

def test_venue_ranker_logic():
    ranker = VenueRanker()
    user_vec = [0.1, 0.2, 0.3]
    cand_vecs = [[0.1, 0.2, 0.3], [-0.1, -0.2, -0.3], [0.5, 0.0, 0.1]]
    sims = ranker.calculate_similarity(user_vec, cand_vecs)
    assert sims[0] > sims[2] > sims[1]
    assert np.isclose(sims[0], 1.0)

if __name__ == "__main__":
    try:
        test_encryption_security()
        test_vrptw_solver_edge_cases()
        test_venue_ranker_logic()
        print("UNIT TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        raise e
