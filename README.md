<<<<<<< HEAD
# Cosmetic-Store
=======
# Cosmetics Store - Django E-commerce Platform

A full-featured e-commerce platform built with Django, focusing on cosmetics products with integrated payment gateways for Nepal (eSewa and Khalti).

## Features

### 1. User Management
- User registration and authentication
- Profile management
- Password reset functionality
- Email verification
- User dashboard

### 2. Product Management
- Product catalog with categories
- Advanced search and filtering
- Product details with reviews
- Stock management
- Wishlist functionality
- Product recommendations

### 3. Shopping Experience
- Shopping cart functionality
- Real-time cart updates
- Order management
- Order tracking
- Order history

### 4. Payment Integration
- eSewa payment gateway
- Khalti payment gateway
- Payment verification
- Payment history
- Email notifications
- Refund management

### 5. Admin Dashboard
- Sales analytics
- Product management
- Order management
- User management
- Category management
- Payment tracking
- Newsletter management

### 6. Additional Features
- Newsletter subscription
- Product reviews and ratings
- Email notifications
- Responsive design
- Mobile-friendly interface

## Technology Stack

- **Backend Framework:** Django 4.x
- **Frontend:** HTML5, CSS3, Tailwind CSS
- **Database:** PostgreSQL
- **Payment Gateways:** eSewa, Khalti
- **Email Service:** SMTP (Gmail)
- **Image Storage:** Local/Cloud Storage

## Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js (for Tailwind CSS)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cosmetics-store.git
cd cosmetics-store
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Configuration

### Payment Gateway Settings
Update the following in `settings.py`:

```python
ESEWA_MERCHANT_CODE = 'your_esewa_merchant_code'
ESEWA_PAYMENT_URL = 'https://uat.esewa.com.np/epay/main'
KHALTI_PUBLIC_KEY = 'your_khalti_public_key'
KHALTI_SECRET_KEY = 'your_khalti_secret_key'
```

### Email Settings
Configure email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

## Project Structure

```
cosmetics-store/
├── store/                 # Main project directory
├── products/             # Product management app
├── orders/              # Order management app
├── users/               # User management app
├── payment/             # Payment integration app
├── newsletter/          # Newsletter management app
├── static/              # Static files
├── templates/           # HTML templates
├── media/              # User-uploaded files
└── manage.py           # Django management script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Framework
- Tailwind CSS
- eSewa Payment Gateway
- Khalti Payment Gateway

## Support

For support, email support@cosmeticsstore.com or create an issue in the repository.

## Roadmap

- [ ] Multi-language support
- [ ] Advanced product filtering
- [ ] Social media integration
- [ ] Mobile app development
- [ ] Analytics dashboard
- [ ] API development

## Screenshots

[Add screenshots of key features here]

## Contact

Your Name - your.email@example.com
Project Link: [https://github.com/yourusername/cosmetics-store](https://github.com/yourusername/cosmetics-store) 
>>>>>>> 95d861f (Initial commit but almost many works are completed.)
