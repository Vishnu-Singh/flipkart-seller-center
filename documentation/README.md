# Documentation App

A comprehensive web-based documentation system for the Flipkart Seller Center API project.

## Overview

The documentation app provides an interactive, user-friendly interface to explore:
- Project setup and installation instructions
- API endpoint documentation for all 6 applications
- Quick start guides
- Troubleshooting information
- API changelog and version history

## Features

### 📚 Multiple Documentation Sections

1. **Home** - Overview with quick stats and application cards
2. **Quick Start** - Get up and running in minutes
3. **Setup Guide** - Detailed installation and configuration
4. **API Reference** - Complete endpoint documentation
5. **API Documentation** - Individual app API details
6. **Changelog** - Version history and changes
7. **Troubleshooting** - Common issues and solutions

### 🎨 Beautiful UI

- Modern, responsive design
- Clean card-based layout
- Color-coded API methods (GET, POST, PUT, DELETE)
- REST/SOAP badges for easy identification
- Code syntax highlighting

### 📊 Dynamic Content

- Loads API documentation from `api_documentation.py`
- Database-backed changelog and setup guides
- Automatic fallback for missing data

### 🔍 Easy Navigation

- Top navigation bar with all sections
- Related API links on each page
- Breadcrumb-style organization

## Access

Once the server is running, access documentation at:
```
http://localhost:8000/docs/
```

## Pages

- `/docs/` - Documentation home
- `/docs/quick-start/` - Quick start guide
- `/docs/setup/` - Setup instructions
- `/docs/api/<app_name>/` - API docs for specific app (orders, inventory, etc.)
- `/docs/api-reference/` - Complete API reference
- `/docs/changelog/` - Version history
- `/docs/troubleshooting/` - Help and troubleshooting

## Models

### APIChangelog
Tracks API version history and changes.

### APIEndpointDoc
Documents individual API endpoints with examples.

### SetupGuide
Step-by-step setup instructions organized by category.

## Admin Interface

All documentation models can be managed through Django admin:
```
http://localhost:8000/admin/documentation/
```

## Customization

### Adding Content

1. **Via Admin Panel**: Add changelog entries, endpoint docs, and setup steps
2. **Via Templates**: Edit templates in `documentation/templates/`
3. **Via api_documentation.py**: Update fallback API documentation

### Styling

The app uses inline CSS in `base.html`. To customize:
- Edit the `<style>` section in `templates/documentation/base.html`
- Colors, fonts, and layout can all be modified

## Integration

The documentation automatically integrates with:
- `api_documentation.py` for API reference
- All 6 app URL patterns
- SOAP WSDL endpoints

## Future Enhancements

- Search functionality
- Code examples in multiple languages
- Interactive API testing
- PDF export
- Dark mode toggle
