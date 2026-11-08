from {{ cookiecutter.package_name }} import sum


def test_sum_adds_numbers():
    assert sum(2, 3) == 5
