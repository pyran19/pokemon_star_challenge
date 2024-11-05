import pytest

@pytest.fixture(autouse=True)
def setup_test():
    # 実数比較の相対許容誤差をデフォルトで1e-6に設定
    pytest.approx._default_rel = 1e-6 