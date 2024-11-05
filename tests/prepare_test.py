from main import get_pool 
import numpy as np

def test_get_pool():
    pool = get_pool()

    sample_relation = np.array([
        [0.0, 1.087, 0.087],
        [-1.087, 0.0, 0.0],
        [-0.087, 0.0, 0.0]
    ])

    assert np.allclose(pool.relation[0][0], sample_relation[0][0],atol=1e-2)
    assert np.allclose(pool.relation[0][1], sample_relation[0][1],atol=1e-2)
    assert np.allclose(pool.relation[0][2], sample_relation[0][2],atol=1e-2)
    assert np.allclose(pool.relation[1][0], sample_relation[1][0],atol=1e-2)
    assert np.allclose(pool.relation[1][1], sample_relation[1][1],atol=1e-2)
    assert np.allclose(pool.relation[1][2], sample_relation[1][2],atol=1e-2)
    assert np.allclose(pool.relation[2][0], sample_relation[2][0],atol=1e-2)
    assert np.allclose(pool.relation[2][1], sample_relation[2][1],atol=1e-2)
    assert np.allclose(pool.relation[2][2], sample_relation[2][2],atol=1e-2)

def test_extract_team_by_index():
    pool = get_pool()
    extracted_relation = pool.extract_team_by_index([0,1,2],[0,1,2])
    sample_relation = np.array([
        [0.0, 1.087, 0.087],
        [-1.087, 0.0, 0.0],
        [-0.087, 0.0, 0.0]
    ])
    assert np.allclose(extracted_relation, sample_relation,atol=1e-2)


def test_extract_team_by_name():
    pool = get_pool()
    extracted_relation = pool.extract_team_by_name(my_team=["プクリン","オコリザル","ウインディ"],op_team=["プクリン","オコリザル","ウインディ"])
    sample_relation = np.array([
        [0.0, 1.087, 0.087],
        [-1.087, 0.0, 0.0],
        [-0.087, 0.0, 0.0]
    ])
    assert np.allclose(extracted_relation, sample_relation,atol=1e-2)
    extracted_relation = pool.extract_team_by_name(my_team=["プクリン","オコリザル","ウインディ"],op_team=["オコリザル","プクリン","ウインディ"])
    sample_relation = np.array([
        [  1.087,0.0,   0.087],
        [ 0.0, -1.087, 0.0],
        [ 0.0, -0.087, 0.0]
    ])
    assert np.allclose(extracted_relation, sample_relation,atol=1e-2)
