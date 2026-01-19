# TG11 Forge - URL Structure

## Main URLs

### Pages App (/)
- `/` - Home page
- `/about/` - About page
- `/contact/` - Contact page

### Services App (/services/)
- `/services/` - Services listing page
- `/services/<int:service_id>/` - Individual service detail page

### Hosting App (/hosting/)
- `/hosting/` - Hosting solutions listing page
- `/hosting/<int:hosting_id>/` - Individual hosting solution detail page

### Pricing App (/pricing/)
- `/pricing/` - Pricing plans page

### Portfolio App (/portfolio/)
- `/portfolio/` - Portfolio listing page
- `/portfolio/<int:portfolio_id>/` - Individual portfolio item detail page

### Notes/Blog App (/blog/)
- `/blog/` - Blog/articles listing page
- `/blog/<int:note_id>/` - Individual blog post detail page

### Admin
- `/admin/` - Django admin interface

## Static Files
- `/static/css/main.css` - Main stylesheet
- `/static/css/theme.css` - Theme styles (light, dark, high contrast)
- `/static/js/main.js` - Main JavaScript functionality
- `/static/js/theme.js` - Theme and accessibility toggles

## Template Structure

### Base Template
- `templates/base.html` - Shared base template with header, footer, theme picker, and dyslexia toggle

### App Templates
Each app has its own templates directory:
- `pages/templates/pages/` - Home, about, contact templates
- `services/templates/services/` - Service list and detail templates
- `hosting/templates/hosting/` - Hosting list and detail templates
- `pricing/templates/pricing/` - Pricing template
- `portfolio/templates/portfolio/` - Portfolio list and detail templates
- `notes/templates/notes/` - Blog list and detail templates
