# FinanceZ - Stock Trading Web Application

FinanceZ is a web application built using Python, Flask, DBMS SQL, Bootstrap, HTML, GIT, and CSS. It allows registered users to simulate stock trading by buying and selling stocks using virtual money. Additionally, users can access real-time stock quotes fetched from the IEX API and view their transaction history within their stock portfolio.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributions](#contributions)
- [Disclaimer](#disclaimer)

## Features

- **User Registration**: Users can sign up for an account with a unique username and password.
- **Authentication**: Secure user authentication ensures only registered users can access the app.
- **Virtual Wallet**: Users are provided with a virtual wallet containing virtual currency to trade stocks.
- **Stock Trading**: Users can buy and sell stocks with their virtual funds.
- **Real-time Stock Quotes**: Real stock quotes are fetched from the IEX API, allowing users to make informed trading decisions.
- **Portfolio Management**: Users can view their stock portfolio, including transaction history and current stock holdings.
- **Responsive Design**: The web app is designed with Bootstrap, ensuring a seamless experience on various devices.

## Getting Started

To run FinanceZ locally, follow these steps:

1. Clone this repository to your local machine using Git.

   ```shell
   git clone https://github.com/sachinrao8312/FinanceZ.git
   
2. Install the required Python packages using pip.
  
    ```shell
    Copy code
    pip install -r requirements.txt

3. Create a virtual environment (optional but recommended).

    ```shell
    Copy code
    python -m venv venv
    Activate the virtual environment (if created).

4. For Windows:
    ```shell
    Copy code
    venv\Scripts\activate
5. For macOS and Linux:

   ```shell
    Copy code
    source venv/bin/activate
6. Set up the database by running the following commands:

    ```shell
    Copy code
    flask db init
    flask db migrate
    flask db upgrade

7.Create a .env file in the project root directory and add your IEX API key as follows:

    ```shell
    Copy code
    IEX_API_KEY=your_api_key_here
8. Start the Flask development server.

    ```shell
      Copy code
      flask run
9.Open your web browser and go to http://localhost:5000 to access the FinanceZ application.

Usage
Register for an account or log in if you already have one.
Once logged in, you'll be able to:
Buy and sell stocks using virtual currency.
View real-time stock quotes fetched from the IEX API.
Check your portfolio to see transaction history and current stock holdings.
Contributions
Contributions to FinanceZ are welcome! Feel free to open issues or submit pull requests to help improve the application.


Disclaimer
Disclaimer: FinanceZ is a simulated stock trading application for educational purposes only. It does not provide real financial services, and any gains or losses incurred while using this application have no real-world monetary value. Users should exercise caution and avoid investing real money based on the information provided by this application.
