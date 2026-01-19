# Database Configuration Guide

## PostgreSQL Setup with UUID Primary Keys

This project is configured to use PostgreSQL as the primary database with UUID primary keys for all models.

## UUID Primary Keys

All models in this project inherit from `BaseModel` which provides:
- **UUID Primary Key**: Automatically generated UUID v4 for each record
- **Created At**: Timestamp when the record was created
- **Updated At**: Timestamp when the record was last updated

### Benefits of UUIDs
- **Globally Unique**: No conflicts across distributed systems
- **Non-Sequential**: Better security (no enumeration attacks)
- **Merge-Friendly**: Safe for database replication and merging
- **URL-Safe**: Can be used in URLs without exposing database size

### Example Model
```python
from forge.models import BaseModel

class MyModel(BaseModel):
    name = models.CharField(max_length=200)
    # id, created_at, and updated_at are automatically included
```

## Database Configuration

### PostgreSQL (Production/Default)

By default, the project uses PostgreSQL. Configure via environment variables:

```bash
# Required PostgreSQL environment variables
export DB_NAME=forge_db
export DB_USER=forge_user
export DB_PASSWORD=your_secure_password
export DB_HOST=localhost
export DB_PORT=5432
```

### SQLite (Development/Testing)

For quick local development, you can use SQLite:

```bash
export USE_SQLITE=True
python manage.py migrate
python manage.py runserver
```

## PostgreSQL Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### macOS
```bash
brew install postgresql
brew services start postgresql
```

### Create Database and User

```sql
-- Connect to PostgreSQL
sudo -u postgres psql

-- Create database and user
CREATE DATABASE forge_db;
CREATE USER forge_user WITH PASSWORD 'your_secure_password';
ALTER ROLE forge_user SET client_encoding TO 'utf8';
ALTER ROLE forge_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE forge_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE forge_db TO forge_user;

-- For PostgreSQL 15+ (required for Django)
\c forge_db
GRANT ALL ON SCHEMA public TO forge_user;

-- Exit
\q
```

## Running Migrations

### With PostgreSQL
```bash
# Make sure environment variables are set
python manage.py migrate
```

### With SQLite
```bash
export USE_SQLITE=True
python manage.py migrate
```

## Models with UUID Primary Keys

All the following models use UUID primary keys:

### Pages App
- `Page`: Static pages content

### Services App
- `Service`: Enterprise services

### Hosting App
- `HostingPlan`: Hosting plans and solutions

### Pricing App
- `PricingPlan`: Pricing plans
- `PricingFeature`: Features for pricing plans

### Portfolio App
- `PortfolioItem`: Portfolio projects

### Notes App (Blog)
- `BlogPost`: Blog posts and articles
- `BlogComment`: Comments on blog posts

## Admin Interface

All models are registered in the Django admin with:
- UUID display (read-only)
- Created/Updated timestamps (read-only)
- Appropriate filters and search fields

Access at: http://localhost:8000/admin/

## Production Deployment

### Environment Variables

Create a `.env` file (DO NOT commit to version control):

```bash
# Django Settings
SECRET_KEY=your-very-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL Database
DB_NAME=forge_db
DB_USER=forge_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

### Security Checklist
- [ ] Use strong, unique SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong database password
- [ ] Enable SSL/TLS for database connections
- [ ] Regular database backups
- [ ] Monitor database performance

## Backing Up PostgreSQL

```bash
# Backup
pg_dump -U forge_user forge_db > backup.sql

# Restore
psql -U forge_user forge_db < backup.sql
```

## Common Issues

### Connection Refused
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in environment variables
- Check `pg_hba.conf` for authentication settings

### UUID Import Error
- Ensure migrations are up to date: `python manage.py migrate`
- Check Python UUID module is available (built-in)

### Permission Denied
- Grant proper permissions to database user
- For PostgreSQL 15+, explicitly grant schema permissions
