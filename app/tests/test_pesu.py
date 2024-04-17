def test_map_branch_to_short_code_should_correctly_map_branch_to_code(pesu_academy):
    assert pesu_academy.map_branch_to_short_code("Computer Science and Engineering") == "CSE"
    assert pesu_academy.map_branch_to_short_code("Electronics and Communication Engineering") == "ECE"
    assert pesu_academy.map_branch_to_short_code("Electrical and Electronics Engineering") == "EEE"
    assert pesu_academy.map_branch_to_short_code("Mechanical Engineering") == "ME"
    assert pesu_academy.map_branch_to_short_code("Civil Engineering") == "CE"
    assert pesu_academy.map_branch_to_short_code("Biotechnology") == "BT"


