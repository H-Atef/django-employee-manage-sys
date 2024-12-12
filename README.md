# Django Employment Management System

## Overview

The **Django Employment Management System** is a backend web application developed using Django and Django REST Framework (DRF) that aims to provide a comprehensive solution for managing employees, departments, companies, and onboarding applicants. The system is designed with role-based access control (RBAC) and secure authentication mechanisms, ensuring that different user roles (admin, manager, employee) have appropriate access levels.

The project utilized Django’s powerful ORM for database management, RESTful APIs for interaction, and JWT for secure authentication. The system is scalable and can be extended with additional features in the future.

## Main Apps in the Project

1. **users**: Manages authentication, user registration, and role-based permissions. Handles user login via JWT.
2. **departments**: Responsible for managing departments within different companies. It enables CRUD operations for department details, and ensures proper relationships between departments and employees.

3. **companies**: Manages company details, such as the number of departments and employees in a company.

4. **employees**: Manages employee records, including employee status, personal details, designation, and employment duration.

5. **onboard_applicants_wf**: Handles the onboarding process of new applicants. The app supports the workflow to track the status of applicants (Application Received, Interview Scheduled, Hired, Not Accepted) and can be further expanded to handle more interactive features in the future.

## Features

The following are the mandatory features to be delivered:

- **Models**:
  - User Model
  - UserInfo Model
  - Company Model
  - Department Model
  - Employee Model
  - OnboardingApplicant Model
  
- **Functionalities**:
  - Implement CRUD operations for User, Company, Department, and Employee models.
  - Implement a workflow for onboarding applicants.
  - Implement role-based access control (RBAC).
  - Implement RESTful APIs for all models with proper HTTP methods.
  - Validate data and ensure required fields are filled.
  - Ensure cascading deletions and manage related records.

- **Security**:
  - JWT authentication with secure authorization.
  - Role-based access control (Admin, Manager, Employee).
  - Implement middleware for global security management.

## Security and Permissions

The application employs **JWT** for secure authentication and role-based access control. Three types of users are supported:

1. **Employee**
2. **Manager**
3. **Admin**

The application also uses **middleware** to manage global security. Once users register, they can log in once, and JWT tokens are stored in HTTP-only cookies for secure handling of user sessions.

The **Strategy Design Pattern** is used in the **employee app**. During the sign-up process, Basic data is collected, while detailed employee information is handled separately according to their role. This allows for easier management and expansion in the future.

## Role Permissions

- **Employee**: Can view their own profile and access basic company and department data.
- **Manager**: Can manage employee data within their company and change the status of applicants.
- **Admin**: Has full permission to perform all CRUD operations across all entities.

## Technical Concepts, Tools, and Technologies

The project uses the following tools and concepts:

- **JWT Authentication**: Implemented using the simpleJWT package, customized to handle role-based authentication and authorization.
- **Django REST Framework (DRF)**: Utilizes class-based views and viewsets for the API implementation.
- **Strategy Design Pattern**: Used in the employee management app for separating basic sign-up data from detailed employee data.
- **Exception Handling**: Proper exception handling for managing errors and ensuring smooth API responses.
- **Database Joins & Relationships**: Managed using Django's ORM for model relationships (e.g., ForeignKey, ManyToMany).
- **Middleware**: Ensures global security management (e.g., JWT handling).

Django REST Framework also provides automatic API documentation for endpoints, and the system includes validation to ensure data integrity.

## How to Use

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

5. Hit the login endpoint to authenticate:

    ```URL: http://localhost:8000/api/v1/user/login/
    Username: admin
    Password: admin
    ```

    If you face any issue with login, you can use the register endpoint to create a new user:

    ```URL: http://localhost:8000/api/v1/user/register/
    Provide: username, password, email, and role (Manager/Admin/Employee)
    ```

6. Explore the different endpoints for each app, such as `/api/v1/companies/`, `/api/v1/employees/`, etc.

## Future Work

1. **Onboarding Applicants App**:
   - The onboarding process will be enhanced to support functionalities like resume uploads, passing data through OCR APIs, and running pattern detection or AI models to assess the applicant's fit based on the job description.
2. **Notification Service**:
   - A notification service or app could be integrated to notify employees, managers, or admins about important events (e.g., new applicant status changes, department updates, etc.).

3. **Business Web Scraper App**:
   - A business web scraper could be added to allow managers and employees to gather data related to their interests, industry news, or relevant business trends.
