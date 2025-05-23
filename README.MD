# 📦 Correos CL Postal Code Scraper

![GitHub release](https://img.shields.io/github/release/Matteuzzz/correos-cl-postal-code-scraper.svg) ![Python version](https://img.shields.io/badge/python-3.8%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

Welcome to the **Correos CL Postal Code Scraper**! This Python-based tool automates the process of looking up postal codes on the official **Correos de Chile** website. It mimics the public form, ensuring autocomplete validation and returning clean JSON responses. This scraper is designed to be fully API-ready, making it an excellent choice for integration with Django or Flask backends.

## 🌐 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)
- [Releases](#releases)

## 🚀 Features

- **Automated Postal Code Lookup**: Quickly fetch postal codes without manual input.
- **Autocomplete Validation**: The scraper ensures that inputs are validated against the official form.
- **Clean JSON Output**: Responses are structured in a JSON format, making them easy to work with.
- **API-Ready**: Seamlessly integrate with Django or Flask applications.
- **Headless Browser**: Utilizes Playwright for efficient web scraping.
- **Cross-Platform**: Works on any system that supports Python.

## 📥 Installation

To get started with the **Correos CL Postal Code Scraper**, you need to have Python 3.8 or higher installed on your machine. You can install the necessary dependencies using pip.

1. Clone the repository:
   ```bash
   git clone https://github.com/Matteuzzz/correos-cl-postal-code-scraper.git
   cd correos-cl-postal-code-scraper
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

To use the scraper, you need to execute the main script. The script will take the postal code as input and return the corresponding information in JSON format.

```bash
python scraper.py <postal_code>
```

Replace `<postal_code>` with the actual postal code you want to look up.

## 🔍 How It Works

The scraper uses Playwright, a powerful web automation library, to interact with the Correos de Chile website. Here’s a brief overview of the process:

1. **Initialization**: The scraper initializes a headless browser instance.
2. **Form Simulation**: It navigates to the postal code lookup form and fills in the required fields.
3. **Autocomplete Handling**: The scraper waits for the autocomplete suggestions to load, ensuring accurate results.
4. **Data Extraction**: Once the postal code is validated, the scraper extracts the relevant data.
5. **JSON Response**: Finally, the data is structured into a clean JSON format and returned.

## 📡 API Integration

This scraper is designed to be easily integrated into your web applications. Here’s a basic example of how you can set it up with Flask:

```python
from flask import Flask, request, jsonify
from scraper import PostalCodeScraper

app = Flask(__name__)

@app.route('/api/postal-code', methods=['GET'])
def get_postal_code():
    postal_code = request.args.get('code')
    scraper = PostalCodeScraper()
    result = scraper.lookup(postal_code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

In this example, a GET request to `/api/postal-code?code=<postal_code>` will return the postal code information in JSON format.

## 🤝 Contributing

We welcome contributions to improve the **Correos CL Postal Code Scraper**. Here’s how you can help:

1. **Fork the repository**: Create your own copy of the project.
2. **Create a branch**: Make a new branch for your feature or bug fix.
3. **Make your changes**: Implement your changes and test them.
4. **Submit a pull request**: Once you're happy with your changes, submit a pull request for review.

Please ensure your code follows the project's coding standards and includes tests where applicable.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📦 Releases

You can find the latest releases of the **Correos CL Postal Code Scraper** [here](https://github.com/Matteuzzz/correos-cl-postal-code-scraper/releases). Download the latest version and follow the installation instructions to get started.

## 🌟 Conclusion

The **Correos CL Postal Code Scraper** is a powerful tool for anyone needing to automate postal code lookups in Chile. Its clean JSON output and API-ready design make it suitable for various applications. Whether you are building a web app or just need quick access to postal codes, this scraper can simplify your workflow.

For further information and updates, feel free to check the [Releases](https://github.com/Matteuzzz/correos-cl-postal-code-scraper/releases) section.

Happy scraping!