import  pytest

def test_exp():

    assert 3!=1

def test_instances():
    assert isinstance("hello", str)
    assert not  isinstance("12", int)

def test_boolean():
    validate=True
    assert validate is True
    assert ("hello" =="tryn") is False


# def test_type():
#     assert type('hello' str)
#     assert type(12 , int)

class student:
    def __init__(self, first_name, last_name, years):
        self.first_name=first_name
        self.last_name=last_name
        self.years=years

@pytest.fixture
def default_employee():
    return student("bushu", "alee",3) 


def test_oerson_initialization(default_employee):
    p=student("bushu", "alee",3)   
    assert default_employee.first_name=="bushu", 'first name should be bushu'
    assert default_employee.last_name=="alee" , 'last name should be alee'
    assert default_employee.years==3     



        