import random
import string
import ibm_db
import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
db2_username = os.environ['DB2INSTL_USERNAME']
db2_password = os.environ['DB2INSTL_PASSWORD']
db2 = create_engine('ibm_db_sa://'+db2_username+':'+db2_password+'@localhost:50009/WHISPROD')

print 'ibm_db_sa://'+db2_username+':'+db2_password+'@localhost:50009/WHISPROD'
conn = db2.connect()


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

def getRandomSixString():
    # Thanks to Ignacio Vasquez-Abrams from Stack Exchnage
    r = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return r;

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

def insert_random_emp_into_temp_ee(connection,case_id):
    call_cmd = """
insert into SESSION.Temp_Ee values
     ( {0},
       3,
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
    insert_emp = call_cmd.format(case_id,'Mickey','M','Mouse'+str(case_id));
    print insert_emp
    result =  connection.execute(insert_emp);


# In the unlikely event a random collision, this will fail an integrity check.
def insert_something_into_temp_viol(connection,case_id):
    call_cmd0 = """
insert into SESSION.Temp_Viol values
     ( 2,
"""
    call_cmd1 = "'"+getRandomSixString()+"'";
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
        emps.append((str(emp[5]),str(emp[6]),str(emp[7])));
    return emps

