# Django REST API for Course Scheduling

## Overview

This project is a Django-based REST API designed to handle course scheduling for a web application. The API provides endpoints to manage course sections, filter routines, and generate optimized schedules based on user preferences. The backend is built using Django and Django REST Framework, and it supports functionality such as handling large datasets, filtering by course codes and sections, and avoiding specific time periods.

## Features

- **Course Section Management**: Create, update, retrieve, and delete course sections.
- **Routine Generation**: Generate and filter routines based on user-provided course codes, details, and preferences.
- **Avoid Time Periods**: Allow users to specify time periods to avoid in their schedules.
- **Pagination**: Efficiently handle and display large sets of data with pagination.
- **Error Handling**: Robust error handling and validation for user inputs and data processing.

## Installation

### Prerequisites

- Python 3.8+
- Django 4.0+
- Django REST Framework 3.14+
- PostgreSQL or MySQL (as the database)

### Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Create a virtual environment**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use: env\Scripts\activate
    ```

3. **Install the requirements**

    ```bash
    pip install -r requirements.txt
    ```
    
4. **Set up environment variables**

    Create a `.env` file in the root directory of the project and add your environment-specific variables. For example:

    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://user:password@localhost:5432/yourdbname
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

    Ensure you have `django-environ` in your `requirements.txt` to handle environment variables.

5. **Configure the database**

    Update the `DATABASES` setting in `settings.py` with your database configuration.

6. **Apply database migrations**

    ```bash
    python manage.py migrate
    ```

7. **Create a superuser**

    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Course Sections

- **List Course Sections**: `GET /api/course-sections/`
- **Create Course Section**: `POST /api/course-sections/`
- **Retrieve Course Section**: `GET /api/course-sections/{id}/`
- **Update Course Section**: `PUT /api/course-sections/{id}/`
- **Delete Course Section**: `DELETE /api/course-sections/{id}/`

### Routines

- **Generate Routines**: `POST /api/generate-routines/`
  - Request Body: JSON with course codes, details, and preferences.
- **Retrieve Routine**: `GET /api/routines/{id}/`

### Authentication

- **Obtain Token**: `POST /api-token-auth/`
  - Request Body: `{ "username": "your-username", "password": "your-password" }`

## Usage

### Generating Routines

To generate a routine, send a POST request to the `/api/generate-routines/` endpoint with a JSON payload including course codes and details. For example:

```json
{
  "course_codes": ["CSE110", "MAT215"],
  "course_details": ["CSE110-[05]", ""],
  "avoid_time": ["08:00 AM-09:20 AM"],
  "avoid_days": ["Sunday", "Monday"],
  "min_days": 2,
  "max_days": 5
}
```

## Handling Time Periods and Days
Users can specify time periods and days to avoid when generating routines. This ensures that no classes are scheduled during these times.

## Testing
Run tests with:

```bash
python manage.py test
```

## Contributing
Feel free to fork the repository, submit issues, and propose enhancements via pull requests. Make sure to follow the coding standards and add tests for any new features or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or suggestions, please contact me.

- **Email: mehedihtanvir@gmail.com

