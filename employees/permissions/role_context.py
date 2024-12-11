from employees.users_strategies.user_strategy import UserStrategy
from employees.users_strategies.admin_strategy import AdminStrategy
from employees.users_strategies.manager_strategy import ManagerStrategy
from employees.users_strategies.employee_strategy import EmployeeStrategy


class RoleContext:
    def __init__(self, role):
        self.role = role
        self.strategies = {
            'Admin': AdminStrategy(),
            'Manager': ManagerStrategy(),
            'Employee': EmployeeStrategy(),
        }

    def get_strategy(self) -> UserStrategy:
        return self.strategies.get(self.role, None)
