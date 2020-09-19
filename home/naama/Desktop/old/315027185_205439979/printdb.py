from persistance import repo


def printActivities():
    all = repo.activities.findAllActivities()
    for activity in all:
        print(activity)


def printCoffee_stands():
    all = repo.coffee_stands.findAllCoffeeStands()
    for cf in all:
        print(cf)


def printEmployees():
    all = repo.employees.findAllEmployees()
    for emp in all:
        print(emp)


def printProducts():
    all = repo.products.findAllProducts()
    for row in all:
        print(row)


def printSuppliers():
    all = repo.suppliers.findAllSuppliers()
    for row in all:
        print(row)
    print()


def printEmployeesReport():
    repo.printEmployeesReport()
    print()


def printActivityReport():
    all = repo.findActivitiesReport()
    for row in all:
        print(row)


def printEmployeesReport():
    for report in repo.findEmployeeReports():
        newSum = float(0)
        for action in repo.activities.findAllActivities():
            empId = repo.employees.findByName(report.name).id
            if action.activator_id == empId:
                product = repo.products.find(action.product_id)
                newSum = newSum - (action.quantity) * (product.price)
        print ('{} {} {} {}'.format(report.name, report.salary, report.location, newSum))


def run():
    print("Activities")
    printActivities()
    print("Coffee stands")
    printCoffee_stands()
    print("Employees")
    printEmployees()
    print("Products")
    printProducts()
    print("Suppliers")
    printSuppliers()
    print("Employees report")
    printEmployeesReport()
    print("Activities")
    printActivityReport()


if __name__ == '__main__':
    run()
