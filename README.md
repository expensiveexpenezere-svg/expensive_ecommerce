# Expensive Ecommerce

A Django-based marketplace storefront featuring a custom user interface and an integrated Jazzmin admin dashboard.

## Features

* **Marketplace Storefront:** Browse and interact with store items.
* **Jazzmin Admin Dashboard:** Enhanced, user-friendly administrative interface.
* **Environment Configuration:** Secure configuration using `.env` files.

## Project Structure

* `expensive_ecommerce/` - Core Django settings and configurations.
* `store/` - Main application logic for the marketplace.
* `static/css/` - Custom stylesheets for the project.

## Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/expensiveexpenezere-svg/expensive_ecommerce.git](https://github.com/expensiveexpenezere-svg/expensive_ecommerce.git)
   cd expensive_ecommerce

   python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
