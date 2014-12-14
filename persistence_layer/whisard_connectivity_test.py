import random
import unittest
from pers_layer import *

def getRandomSixString():
    # Thanks to Ignacio Vasquez-Abrams from Stack Exchnage
    r = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return r;


class TestSequenceFunctions(unittest.TestCase):
    def test_read_employees(self):
        read_emps_sql = "select * from esadbm.case_employees";
        result =  conn.execute(read_emps_sql);

    def add_random_employee_to_case(self,case_id,violation,employee):
        create_temp_ee_in_session(conn)
        insert_random_emp_into_temp_ee(conn,case_id,employee)
        create_temp_viol_in_session(conn)
        insert_something_into_temp_viol(conn,case_id,violation)
        invoke_add_employee_data(conn,case_id)

    def test_can_create_new_employee(self):
        case_id = random.randint(0,10000)
        violation = getRandomSixString()
        employee = Employee_pl("Mickey","M","Mouse"+str(case_id))
        trans = conn.begin()
        try:
            self.add_random_employee_to_case(case_id,violation,employee)
            trans.commit()
            print "Success! Operations Complete!"
        except:
            trans.rollback()
            raise

    def test_can_add_two_employees_to_case(self):
        case_id = random.randint(0,10000)
        violation0 = getRandomSixString()
        violation1 = getRandomSixString()
        employee = Employee_pl("Foghorn","J","Leghorn"+str(case_id))
        trans = conn.begin()
        try:
            self.add_random_employee_to_case(case_id,violation0,employee)
            self.add_random_employee_to_case(case_id,violation1,employee)
            trans.commit()
            print "Success! Operations Complete!"
        except:
            trans.rollback()
            raise

    def test_can_read_cases(self):
# I have no idea what the difference between thse two fields are!
# ee_case_id seems to be irrelevant in my current flawed usage.
        read_cases_sql = "select ee_case_id,case_id from esadbm.case_employees";
        result =  conn.execute(read_cases_sql);

    def test_can_read_employees_from_case(self):
        case_id = find_random_case(conn);
        emps = read_employees_from_case(conn,case_id);
        for emp in emps:
            print "Employee: "+ emp.first_name +" "+emp.middle_initial+" "+emp.last_name

if __name__ == '__main__':
    unittest.main()

# Create proper test fixtures setup and teadowns
    conn.close()
