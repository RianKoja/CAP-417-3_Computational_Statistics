from ejemplo import check_limit

def test_check_limit():
    flag = check_limit(4)
    assert flag
