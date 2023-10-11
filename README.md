# Storefront

Storefront is a REST API project developed using Django and Django Rest Framework (DRF). It provides a comprehensive solution for efficiently managing e-store data, enabling users to seamlessly create, retrieve, update, and delete store-related information. Designed for web and mobile applications, Storefront streamlines e-commerce data management, ensuring robust and scalable operations.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

### Prerequisites

Before getting started, make sure you have the following installed:

- Python 3.x
- Virtual Environment

### Setup Virtual Environment

```bash
# For Windows
python -m venv storefront-env

# For Unix/Mac
python3 -m venv storefront-env
```
### Activate Virtual Environment
```bash
# For Windows
storefront-env\Scripts\activate.bat

# For Unix/Mac
source storefront-env/bin/activate
```

### Clone the Project and Navigate to the Directory
```bash
git clone https://github.com/tonishantyadav/Storefront.git
cd storefront
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start the Server
```bash
python manage.py runserver
```

## Getting Started
- Access the API at [http://localhost:8000/store/](http://localhost:8000/store/)
- Check this [ENDPOINTS](ENDPOINTS.md) file for available endpoints.


## Contributing
We welcome contributions! If you'd like to contribute to this project, please follow our [Contribution Guidelines](CONTRIBUTING.md).


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact me at [inishantyadav24@gmail.com](mailto:inishantyadav24@gmail.com). 

I hope you find Storefront useful for your store management needs. Happy coding!
