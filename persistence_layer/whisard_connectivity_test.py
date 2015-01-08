import random
import unittest
from pers_layer import *

class TestSequenceFunctions(unittest.TestCase):

    def test_read_employees(self):
        read_emps_sql = "select * from esadbm.case_employees";
        result =  conn.execute(read_emps_sql);
        for row in result:
            print "row:", row
        

#     def test_most_basic_execution(self):
#         trans = conn.begin()
#         try:
#             create_temp_ee_in_session(conn)
#             insert_something_into_temp_ee(conn)
#             create_temp_viol_in_session(conn)
#             insert_something_into_temp_viol(conn,0)
#             invoke_add_employee_data(conn,0)
#             trans.commit()
#             print "Success! Operations Complete!"
#         except:
#             trans.rollback()
#             raise

    def test_can_create_new_emploee(self):
        case_id = random.randint(0,10000)
        trans = conn.begin()
        try:
            create_temp_ee_in_session(conn)
            insert_random_emp_into_temp_ee(conn,case_id)
            create_temp_viol_in_session(conn)
            insert_something_into_temp_viol(conn,case_id)
            invoke_add_employee_data(conn,case_id)
            trans.commit()
            print "Success! Operations Complete!"
        except:
            trans.rollback()
            raise

if __name__ == '__main__':
    unittest.main()

# Create proper test fixtures setup and teadowns
    conn.close()
