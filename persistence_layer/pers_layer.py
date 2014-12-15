import random
import string
import ibm_db
import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
db2_username = os.environ['DB2INSTL_USERNAME']
db2_password = os.environ['DB2INSTL_PASSWORD']
db2 = create_engine('ibm_db_sa://'+db2_username+':'+db2_password+'@localhost:50009/WHISPROD')

conn = db2.connect()

# GENERAL NOTES
# I suspect, and need to confirm, that "KASE" is the master table for an overall Case.
# In this example, we are workign mostly with the "EE_CASE", which might mean
# Employee Entry.

def create_temp_ee_in_session(connection):
    call_cmd = """
DECLARE GLOBAL TEMPORARY TABLE Temp_Ee 
      ( Tmp_Id           SMALLINT,
        Ee_Case_Id       INTEGER,
        Ee_F_Name        VARCHAR(25),
       Ee_Mi            CHAR(1),
       Ee_L_Name        VARCHAR(25),
       Ee_Addr1         VARCHAR(40),
       Ee_City          VARCHAR(30),
       Ee_State_Id      VARCHAR(2),
       Ee_Zip           VARCHAR(10),
       Ee_Phone1        VARCHAR(25),
       Date_Employ_Beg  DATE,
       Date_Employ_End  DATE,
       EE_Job_Title1    VARCHAR(50),
       EE_Job_Pay_Rate1 DECIMAL(16,2),
       Amt_Bw_Computed  DECIMAL(16,2),
       Date_Beg_Viol    DATE,
       Date_End_Viol    DATE,
       Status           SMALLINT DEFAULT 0) WITH REPLACE ON COMMIT PRESERVE ROWS NOT LOGGED;
"""

    result =  connection.execute(call_cmd);


def create_temp_viol_in_session(connection):
    call_cmd = """
 DECLARE GLOBAL TEMPORARY TABLE Temp_Viol
     ( Tmp_Id SMALLINT,
       Act_Id VARCHAR(6),
       Violation_Id SMALLINT,
       Haz_Occp_Id SMALLINT,
       Compliance_Status SMALLINT,
       Date_Beg_Viol DATE,
       Date_End_Viol DATE,
       Amt_Bw_Computed DECIMAL(16,2),
       Amt_Bw_Assessed DECIMAL(16,2),
       Reason_Id SMALLINT,
       Severity_Id SMALLINT,
       Injury_Level_Id  SMALLINT,
       Specific_Info VARCHAR(30)
     ) WITH REPLACE ON COMMIT PRESERVE ROWS NOT LOGGED
"""
    result =  connection.execute(call_cmd);

class Employee_pl:
    def __init__(self, first, middle, last):
        self.first_name = first;
        self.middle_initial = middle;
        self.last_name = last;

# In reality, this is really a "business layer" function --- I can use this as a reason
# to create a business layer! That is a Todo.
    def full_name(self):
# This needs to handle missing middle initial!
        return self.first_name + " " + self.middle_initial + "." + " " + self.last_name


# Note: There is a danger I may have inserted a record into case_employees by hand.
# We seem to have a problem building records there.  I may have to build a 
# separate way to prepare the database.
# The stored procedure should be able to add, but possibly the "next_id" function
# is not working correctly.  We sadly may have to debug inside the stored procedure
# again to get this working, nonetheless it is the highest priority.
def insert_something_into_temp_ee(connection):
    call_cmd = """
insert into SESSION.Temp_Ee values
     ( 0,
       0,
       'Mickey',
       'L',
       'Mouse',
       'bla blah',
       'FocativeMirrors',
       'TX',
       '55555',
       '555-1212',
       '10/10/2010',
       '10/10/2012',
       'Defender',
       10.25,
       600,
       '10/10/2010',
       '10/10/2010', 
       0
     )
""";
    result =  connection.execute(call_cmd);

def insert_random_emp_into_temp_ee(connection,case_id,employee):
    call_cmd = """
insert into SESSION.Temp_Ee values
     ( {0},
        4,
       '{1}',
       '{2}',
       '{3}',
       'bla blah',
       'FocativeMirrors',
       'TX',
       '55555',
       '555-1212',
       '10/10/2010',
       '10/10/2012',
       'Defender',
       10.25,
       600,
       '10/10/2010',
       '10/10/2010', 
       0
     )
""";
#    insert_emp = call_cmd.format(case_id,'Mickey','M','Mouse'+str(case_id));
    insert_emp = call_cmd.format(case_id,employee.first_name,employee.middle_initial,employee.last_name);
    print insert_emp
    result =  connection.execute(insert_emp);


# In the unlikely event a random collision, this will fail an integrity check.
def insert_something_into_temp_viol(connection,case_id,violation):
    call_cmd0 = """
insert into SESSION.Temp_Viol values
     ( 2,
"""
    call_cmd1 = "'"+violation+"'";
    call_cmd2 = """
       0,
       0,
       0,
       '10/10/2010',
       '10/10/2012',
        300.32,
        150.17,
        0,
        0,
        0,
       'abc'
     )
""";
    cmd = call_cmd0+call_cmd1+","+call_cmd2;
    print cmd
    result =  connection.execute(cmd);

def invoke_add_employee_data(connection,case_id):
    call_cmd = "call esadbm.SP_WH_ADD_EES({0},1,0,1,0,0,0)".format(case_id)
    result =  connection.execute(call_cmd);
    return null

def get_employee_names():
    return get_employee_names_db(conn)

def get_employee_names_db(connection):
    read_emps_sql = "select * from esadbm.case_employees";
    result =  connection.execute(read_emps_sql);
    emps = []
    for emp in result:
        print emp;
        emps.append((emp[5],emp[6],emp[7]));
    return emps

def read_employees_from_case(connection,case_id):
    read_emps_sql = "select * from esadbm.case_employees where case_id = {0}".format(case_id);
    result =  conn.execute(read_emps_sql);
    emps = []
    for row in result:
        emps.append(Employee_pl(row[5],row[6],row[7]));
    return emps

def read_violations_from_case(connection,case_id):
    read_emps_sql = "select * from esadbm.case_act_eer_viol where case_id = {0}".format(case_id);
    result =  conn.execute(read_emps_sql);
    return result

def find_random_case(conn):
    read_cases_sql = "select ee_case_id,case_id from esadbm.case_employees";
    result =  conn.execute(read_cases_sql);
        # Looks like maybe I can't get a length on a reader, so I will slurp..
    cases = []
    for row in result:
        cases.append(row[1])
    case_id = random.choice(cases);
    return case_id

