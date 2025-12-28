class Employee :
    emp_num = 0

    def __init__(self,name,salary) :
        self.name= name
        self.salary = salary
        Employee.emp_num += 1

    def display_count():
        print(f" The Employee count is :{Employee.emp_num}")

    def dispaly_info(self):
        print(f"The name is :{self.name} , The salary is : {self.salary}")
    
    def __str__(self) :
        return f" The Name is : {self.name}"


emp1 = Employee("Tamer", 2000)
emp2 = Employee("Maged", 3000)
emp3 = Employee("Aseel",4000)

Employee.display_count()
emp1.dispaly_info()
Employee.dispaly_info(emp2)
print(emp3)
print(getattr(emp1,"name"))
print(hasattr(emp2,"name"))