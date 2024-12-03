# Havmore with Us - Full Stack Application

## Project Overview

**Havmore with Us** is a web application developed for **Ram Enterprises**. It provides an interactive platform for customers to place orders, manage their orders, and simulate card payments. The application uses a modern full-stack approach, combining Python, Django for the backend, and HTML, CSS, JavaScript for the frontend.

### Key Features:
- User Registration and Login
- Order Placement and Management
- Payment Simulation
- Invoice Generation 
- Order History and Tracking
- Admin Dashboard for Order Management

### Note:
The payment functionality in this project is a **dummy implementation**. It simulates the process of entering card details and performing payment, but it does not interact with a real payment gateway. For production use, integration with a real payment gateway (such as Stripe or Razorpay) would be required.

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Version Control**: Git, GitHub

## Installation Instructions

### Prerequisites

Before running the project, make sure you have the following installed on your system:
- Python 3.x
- MySQL
- Git

### Steps to Run the Project Locally

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Adarsh203-cmd/havmore-with-us.git
    ```

2. **Navigate to the Project Folder**:
    ```bash
    cd havmore-with-us
    ```

3. **Create a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv env
    ```

4. **Activate the Virtual Environment**:
    - For Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - For MacOS/Linux:
        ```bash
        source env/bin/activate
        ```

5. **Install Required Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Set up Database**:
    - Make sure you have a MySQL database set up and update the `settings.py` file with your database credentials.
    - Run migrations:
        ```bash
        python manage.py migrate
        ```

7. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

    Now, open your browser and go to `http://127.0.0.1:8000/views` to access the application.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request. Ensure that your changes are well-tested and follow the existing code structure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to **Ram Enterprises** for providing the opportunity to work on this project.

