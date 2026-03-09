"""
Girma Dingeto
Brady Heinz
Samuel Sidzyik
Module 10.1
3/4/26

Create python code to run sql queries
"""

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")
 
""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}
try:
    """ try/catch block for handling potential MySQL database errors """ 

    'Connection to DB'
    db = mysql.connector.connect(**config) # connect to the wine database 
    cursor = db.cursor()

    'Query for 1'
    cursor.execute("""SELECT TrackingNumber,
                    datediff(COALESCE(DeliveryDate, curdate()),shipdate) AS days_difference,
                    CASE
                        when DATEDIFF(COALESCE(DeliveryDate, curdate()),shipdate) > 4
                        THEN 'LATE'
                        ELSE 'OK'
                    END as 'Status'
                    FROM winery.distributororder
                    Order by status;""")
    Lines = cursor.fetchall()
    print(f"\n-- DISPLAYING DELIVERY STATUS --")
    for Line in Lines:
        print(f"Tracking Number: {Line[0]}\nDelivery Time in Days: {Line[1]}\nStatus: {Line[2]}\n")

    'Query for 2'
    cursor.execute("""SELECT LocationName, ItemName, QuantityOnHand FROM winery.inventorybalance
                    join winery.inventoryitem on inventorybalance.itemID = inventoryitem.itemid
                    join winery.location on location.locationID = inventorybalance.locationID
                    where category = 'Finished good';;""")
    Lines = cursor.fetchall()
    print(f"\n-- DISPLAYING WINE LOCATIONS --")
    for Line in Lines:
        print(f"Locale: {Line[0]}\nWine: {Line[1]}\nAmount: {Line[2]} bottle(s)\n")

    'Query for 3'
    cursor.execute("""SELECT employeeID, `Q-1Hours`  as 'Last Quarter' , `Q-2Hours` as '2 Quarters Ago', `Q-3Hours` as '3 Quarters Ago', `Q-4Hours` as '4 Quarters Ago',
                    sum(ifnull(`Q-1Hours`,0)+ ifnull(`Q-2Hours`,0)+ ifnull(`Q-3Hours`,0)+ ifnull(`Q-4Hours`,0))as 'Total for Last 4 Complete Quarters' FROM winery.employee
                    group by employeeID;""")
    Lines = cursor.fetchall()
    print(f"\n-- DISPLAYING EMPLOYEE HOURS BY QUARTER AND TOTAL --")
    for Line in Lines:
        print(f"Emp ID: {Line[0]}\nQ4: {Line[1]}\nQ3: {Line[2]}\nQ2: {Line[3]}\nQ1: {Line[4]}\nTotal: {Line[5]}\n")   



except mysql.connector.Error as err:
    """ on error code """
 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
 
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
 
    else:
        print(err)
 
finally:
    """ close the connection to MySQL """
 
    db.close()