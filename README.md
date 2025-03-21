# Trendyol Selenium Automation Project
This project is developed using Selenium and Python to automate test scenarios and actions on the Trendyol e-commerce platform. The project follows the Page Object Model (POM) design pattern to provide maintainable and modular test cases.
## Project Structure
```commandline
/trendyol_selenium
│
├── /cases              # Test scenarios
│   ├── /auth           # User authentication tests
│   ├── /basket         # Cart operations
│   ├── /product_page   # Product page operations
│   └── /wishlist       # Wishlist operations
├── /datas              # Test data and product information
├── /generic            # Helper functions
├── /pages              # Page objects (Page Object Model)
├── /tests              # Base test class and test runner
├── .gitignore          # Git ignore file
├── env-local           # Local environment variables
├── requirements.txt    # Required Python libraries
├── run_cases.py        # Main file to run test scenarios
└── README.md           # Project documentation

```
## Getting Started
### Requirements
The following dependencies need to be installed for the project to work:
- Python 3.8+
- Selenium
- WebDriver (ChromeDriver)

To install the dependencies:
```commandline
pip install -r requirements.txt
```
### WebDriver Setup
This project is compatible with ChromeDriver. You can download the appropriate version from ChromeDriver.

Running Test Scenarios
To run the tests, use the following command:
```commandline
python run_cases.py
```
This command will sequentially run all the test scenarios from the cases folder.

## Project Features
### Test Scenarios (Cases)
Test cases are organized into modules within the cases folder:

- [x] auth: User sign-in and validation (sign_in.py, sign_in_validation.py)
- [x] basket: Cart operations (add_to_cart.py)
- [x] product_page: Product page operations and combination check (check_item_has_combinations.py)
- [x] wishlist: Add to wishlist (add_to_wishlist.py)
### Page Objects (Pages)
The pages folder contains page objects that represent each page. These objects abstract user interactions and element locators:

- [x] cart_page.py: Cart page.
- [x] home_page.py: Home page.
- [x] listing_page.py: Product listing page.
- [x] product_page.py: Product page.
### Helper Functions (Generic)
The generic folder contains helper functions for repeated actions across tests:

- [x] auth.py: User authentication and sign-in processes.
- [x] initialize.py: Initialization of WebDriver and settings.
### Test Data (Datas)
The datas folder contains necessary test data, such as product details and user credentials for the test scenarios.




