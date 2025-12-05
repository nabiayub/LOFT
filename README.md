# LOFT - Online Furniture Store

![LOFT Logo](https://via.placeholder.com/150x150?text=LOFT+Logo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26.svg)](https://html5.org/)

## 🚀 Overview

LOFT is a comprehensive online furniture store built with Django and modern HTML/CSS. This pet project showcases a complete e-commerce solution with product catalogs, user authentication, shopping cart functionality, and order management.

### Key Features:
✅ **Complete Product Catalog** - Browse through a wide variety of furniture items
✅ **User Authentication** - Secure login and registration system
✅ **Shopping Cart** - Add, modify, and remove items from your cart
✅ **Checkout Process** - Complete purchase workflow
✅ **Order Management** - Track your orders and history
✅ **Favorites System** - Save products you're interested in
✅ **Responsive Design** - Works on all device sizes
✅ **Admin Panel** - Easy management of products and categories

LOFT is perfect for developers looking to build a complete e-commerce solution from scratch, or for anyone interested in furniture shopping with a modern, user-friendly interface.

---

## ✨ Features

### Core Functionality:
- **Product Browsing**: Filter by category, color, price range, and type
- **Detailed Product Pages**: View images, specifications, and descriptions
- **Shopping Cart**: Add multiple items with quantity control
- **Checkout Process**: Multiple payment options (Stripe integration)
- **User Accounts**: Manage your profile, orders, and favorites

### Advanced Features:
- **Product Filtering**: Advanced search and filtering capabilities
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Admin Dashboard**: Easy management of all store content
- **Order Tracking**: View your complete purchase history
- **Favorites System**: Save products for later consideration

### Technical Features:
- **Django Framework**: Robust backend with ORM support
- **Stripe Integration**: Secure payment processing
- **Custom Templates**: Modern, responsive HTML/CSS design
- **Database Models**: Comprehensive product and order management

---

## 🛠️ Tech Stack

### Primary Technologies:
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Django 5.1
- **Database**: SQLite (with easy migration to PostgreSQL)
- **Payment Processing**: Stripe API

### Additional Tools:
- **Admin Interface**: Django Admin + Jazzmin
- **Static Files**: Django's built-in static files handling
- **Templates**: Django Template Language (DTL)
- **Build Tools**: None (pure Django development)

### System Requirements:
- Python 3.8+
- Django 5.1+
- SQLite (default) or PostgreSQL/MySQL
- Node.js (for development environment, optional)

---

## 📦 Installation

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher installed
- Git installed for version control
- Basic knowledge of Django development

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/loft-furniture-store.git
   cd loft-furniture-store
Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

pip install -r requirements.txt
Set up the database:

python manage.py migrate
Create a superuser (for admin access):

python manage.py createsuperuser
Run the development server:

python manage.py runserver
Access the application: Open your browser to http://127.0.0.1:8000/
