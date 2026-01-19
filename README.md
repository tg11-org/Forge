# Forge

TG11 Forge - Industrial Enterprise Services Website

## Overview

TG11 Forge is a Django-based website for industrial enterprise services. The project features a clean app-based architecture with multiple apps for different sections of the site.

## Features

- **Clean App Structure**: Organized into logical apps (pages, services, hosting, pricing, portfolio, notes)
- **PostgreSQL Database**: Configured for PostgreSQL with UUID primary keys
- **UUID Primary Keys**: All models use UUIDs instead of incremental integers for better security and distributed system compatibility
- **Responsive Design**: Mobile-friendly layout with responsive navigation
- **Theme Picker**: Toggle between Light, Dark, and High Contrast themes
- **Dyslexia-Friendly Mode**: Optional dyslexia-friendly font toggle for improved accessibility
- **Reusable Templates**: Base template with shared header and footer
- **Static Files**: Organized CSS and JavaScript files

## Database

This project uses **PostgreSQL** with **UUID primary keys** for all models. See [DATABASE.md](DATABASE.md) for detailed setup instructions.

### Quick Database Setup

**For Development (SQLite)**:
```bash
export USE_SQLITE=True
python manage.py migrate
```

**For Production (PostgreSQL)**:
```bash
# Set up PostgreSQL and configure environment variables
export DB_NAME=forge_db
export DB_USER=forge_user
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432

python manage.py migrate
```

## Project Structure

```
Forge/
├── forge/              # Main project settings
├── pages/              # General pages (Home, About, Contact)
├── services/           # Enterprise services
├── hosting/            # Hosting solutions
├── pricing/            # Pricing plans
├── portfolio/          # Portfolio showcase
├── notes/              # Blog/articles
├── templates/          # Shared templates (base.html)
├── static/             # Static files (CSS, JS)
│   ├── css/
│   │   ├── main.css
│   │   └── theme.css
│   └── js/
│       ├── main.js
│       └── theme.js
├── manage.py
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tg11-org/Forge.git
cd Forge
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Visit http://localhost:8000 in your browser

## URLs

- `/` - Home page
- `/about/` - About page
- `/contact/` - Contact page
- `/services/` - Services listing
- `/services/<id>/` - Service detail
- `/hosting/` - Hosting solutions listing
- `/hosting/<id>/` - Hosting solution detail
- `/pricing/` - Pricing plans
- `/portfolio/` - Portfolio listing
- `/portfolio/<id>/` - Portfolio item detail
- `/blog/` - Blog/articles listing
- `/blog/<id>/` - Blog post detail
- `/admin/` - Admin interface

## Accessibility Features

### Theme Picker
Click the theme toggle button (🌓) in the header to cycle through themes:
- Light theme (default)
- Dark theme
- High contrast theme

Theme preferences are saved in local storage.

### Dyslexia-Friendly Mode
Click the dyslexia toggle button (Aa) in the header to enable a dyslexia-friendly font with increased letter spacing and line height.

## Development

### Creating a Superuser

To access the Django admin panel:
```bash
python manage.py createsuperuser
```

### Running Tests

```bash
python manage.py test
```

### Static Files

Static files are located in the `static/` directory:
- `static/css/` - Stylesheets
- `static/js/` - JavaScript files

## License

See LICENSE file for details.

## Contact

For more information, visit the contact page or email info@tg11forge.com