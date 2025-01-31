from Thirdtry import *

def test_open_File():
    open_File("Test_fichiers/SmokeDetector_M1.capella")
    # print(open_File("Test_fichiers/SmokeDetector_M1.capella"))
    
def test_parse_to_tree():
    print(parse_to_tree(open_File("Test_fichiers/SmokeDetector_M1.capella")))

def test_print_tree():
    print_tree(parse_to_tree(open_File("Test_fichiers/SmokeDetector_M1.capella")))

# Run the tests
# test_open_File()
# test_parse_to_tree()
test_print_tree()

