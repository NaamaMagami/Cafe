import atexit
import sqlite3
import os
import imp

DB_NAME = 'moncafe.db'


# Data Transfer Objects:
class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        return '(' + str(self.id) + ', ' + str(self.name) + ', ' + str(self.contact_information) + ')'


class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand

    def __str__(self):
        return '(' + str(self.id) + ', ' + str(self.name) + ', ' + str(self.salary) + ', ' + str(
            self.coffee_stand) + ')'


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return '(' + str(self.id) + ', ' + str(self.description) + ', ' + str(self.price) + ', ' + str(
            self.quantity) + ')'


class Coffee_stand:
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __str__(self):
        return '(' + str(self.id) + ', ' + str(self.location) + ', ' + str(self.number_of_employees) + ')'


class Activity:
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __str__(self):
        return '(' + str(self.product_id) + ', ' + str(self.quantity) + ', ' + str(self.activator_id) + ', ' + str(
            self.date) + ')'


class EmployeesReport:
    def __init__(self, name, salary, location):
        self.name = name
        self.salary = salary
        self.location = location

    def __str__(self):
        return '(' + str(self.name).replace(" ", "") + ', ' + str(self.salary) + ', ' + str(self.location) + ', ' + str(
            self.sum) + ')'


class ActivityReport:
    def __init__(self, date, description, quantity, empName, SupName):
        self.date = date
        self.description = description
        self.quantity = quantity
        self.empName = empName
        self.SupName = SupName

    def __str__(self):
        return '(' + str(self.date).replace(" ", "") + ', ' + str(self.description) + ', ' + str(
            self.quantity) + ', ' + str(
            self.empName) + ', ' + str(self.SupName) + ')'


# --------------------------------------------------------------------------------

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        newName = ("'{}'".format(supplier.name))
        contact = ("'{}'".format(supplier.contact_information))
        self._conn.execute("""
            INSERT INTO suppliers (id,name,contact_information) VALUES (?, ?,?)
        """, [supplier.id, newName, contact])

    def findSupplier(self, supNum):
        c = self._conn.cursor()
        c.execute("""
                SELECT num,expected_output FROM suppliers WHERE id = ?
            """, [supNum])

        return Supplier(*c.fetchone())

    def findAllSuppliers(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM suppliers ORDER BY id""").fetchall()
        return [Supplier(*row) for row in all]


class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        newName = str(employee.name)[1:]
        newName = ("'{}'".format(employee.name))
        newName = str(employee.name)
        self._conn.execute("""
               INSERT INTO employees (id,name,salary,coffee_stand) VALUES (?, ?,?,?)
           """, [employee.id, newName, employee.salary, employee.coffee_stand])

    def find(self, employee_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM employees WHERE id = ?
        """, [employee_id])
        return Employee(*c.fetchone())

    def findByName(self,name):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM employees WHERE name = ?
        """, [name])
        return Employee(*c.fetchone())

    def findAllEmployees(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM employees ORDER BY id""").fetchall()
        return [Employee(*row) for row in all]


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        new = ("'{}'".format(product.description))
        self._conn.execute("""
            INSERT INTO products (id, description, price,quantity) VALUES (?, ?, ?,?)
        """, [product.id, new, product.price, product.quantity])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""SELECT id, description, price, quantity FROM Products WHERE id = ?""",
                  [id])
        return Product(*c.fetchone())

    def findAllProducts(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM products ORDER BY id""").fetchall()

        return [Product(*row) for row in all]

    def updateProduct(self, ID, Q):
        c = self._conn.cursor()
        int_id = int(ID)
        int_q = int(Q)
        c = self._conn.cursor()
        c.execute("""UPDATE products SET quantity = (?) WHERE id=(?)
             """, [int_q, int_id])
        return


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        new = str(coffee_stand.location)[1:]
        new = ("'{}'".format(coffee_stand.location))
        self._conn.execute("""
                INSERT INTO coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
            """, [coffee_stand.id, new, coffee_stand.number_of_employees])

    def findAllCoffeeStands(self):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM coffee_stands ORDER BY id""")
        return [Coffee_stand(*row) for row in c.fetchall()]


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
                INSERT INTO activities (product_id,quantity, activator_id,date) VALUES (?, ?,?,?)
            """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])


    def findAllActivities(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM activities ORDER BY date""").fetchall()
        return [Activity(*row) for row in all]


# ------------------------------------------------------------------------------------


class _Repository:

    def __init__(self):
        self._conn = sqlite3.connect(DB_NAME)
        self.suppliers = _Suppliers(self._conn)
        self.employees = _Employees(self._conn)
        self.products = _Products(self._conn)
        self.coffee_stands = _Coffee_stands(self._conn)
        self.activities = _Activities(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id  INTEGER PRIMARY KEY,
                name    TEXT    NOT NULL,
                salary  REAL NOT NULL,
                coffee_stand    INTEGER INTEGER REFERENCES Coffee_stand(id) 
            );
    
            CREATE TABLE suppliers (
                id  INTEGER PRIMARY KEY,
                name    TEXT    NOT NULL, 
                contact_information TEXT
            );
             
            CREATE TABLE coffee_stands (
                id  INTEGER PRIMARY KEY,
                location    TEXT    NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE products (
                id  INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price   REAL    NOT NULL,
                quantity    INTEGER NOT NULL
            );
             
            CREATE TABLE activities (
                product_id  INTEGER INTEGER REFERENCES Product(id),
                quantity    INTEGER NOT NULL,
                activator_id    INTEGER    NOT NULL,
                date    DATE    NOT NULL
            );
         """)

    def findActivitiesReport(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT activities.date, products.description , activities.quantity , employees.name , suppliers.name
        FROM activities
        INNER JOIN products ON products.id = activities.product_id 
        LEFT JOIN Employees ON employees.id = activities.activator_id 
        LEFT JOIN Suppliers ON suppliers.id = activities.activator_id
        ORDER BY date""").fetchall()
        return [ActivityReport(*row) for row in all]

    def findAllEmployeeByName(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT * FROM employees ORDER BY name""")
        return all

    def findLocationByName(self, empName):
        c = self._conn.cursor()
        stand = c.execute("""SELECT coffee_stand FROM employees WHERE name=(?)""", [empName]).fetchone()
        cofStand = stand[0]
        location = c.execute("""SELECT location FROM coffee_stands WHERE id=(?)""", [cofStand]).fetchone()
        return location

    def findTotalSalesIncome(self, empId):
        c = self._conn.cursor()
        products = c.execute("""SELECT product_id,quantity FROM activities WHERE activator_id=(?)""", [empId])
        sum = float(0)
        for prod in products:
            if prod[1] > 0:
                prodPrice = c.execute("""SELECT price FROM products WHERE id=(?)""", [prod[0]])
                sum = sum + prodPrice * prod[1]
        return sum

    def findEmployeeReports(self):
        c = self._conn.cursor()
        all = c.execute("""
                       SELECT employees.name, employees.salary, coffee_stands.location
                       FROM employees
                       INNER JOIN Coffee_stands ON coffee_stands.id = employees.coffee_stand
                       ORDER BY name 
                   """)
        return [EmployeesReport(*row) for row in all]

repo = _Repository()
atexit.register(repo._close)
