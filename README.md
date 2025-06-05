# Jeddie Wedding Website

A Flask-based wedding website featuring RSVP management and a gift registry with Stripe integration. The website supports both English and Romanian languages.

## Features

- **Multi-language Support**: Full support for English and Romanian languages
- **RSVP System**: 
  - Guest search functionality
  - Individual guest RSVP management
  - Meal selection
  - Dietary restrictions
  - Song requests
- **Gift Registry**:
  - Pre-defined gift items
  - Custom gift amounts
  - Stripe payment integration
  - Gift tracking and availability
- **Static Pages**:
  - Home
  - Our Story
  - Wedding Details
  - Photo Gallery
  - Hotel Information

## Screenshots

![home](https://github.com/eddie-cosma/jeddie-wedding/assets/36821604/69095801-5c28-4b23-9159-ef405faee01c)
![wedding](https://github.com/eddie-cosma/jeddie-wedding/assets/36821604/d98461b5-ac87-44df-a8ca-221a3e89f8e0)
![rsvp](https://github.com/eddie-cosma/jeddie-wedding/assets/36821604/86ac95fb-76a1-4853-a606-b7eeed9c7597)
![registry](https://github.com/eddie-cosma/jeddie-wedding/assets/36821604/5a7addfa-74ca-42a7-81b7-320bc3b84afd)

| English | Romanian |
| ------- | -------- |
| ![registry_responsive](https://github.com/eddie-cosma/jeddie-wedding/assets/36821604/6bd6adf7-1855-4641-aa92-0b12cb3d0c47) | ![registry_romanian](https://github.com/eddie-cosma/jeddie-wedding/assets/36821604/09765707-b139-4c8c-b2ce-1a046bd1e85d) |

## Technical Stack

- **Backend**: Flask 2.2
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Payment Processing**: Stripe API
- **Testing**: pytest
- **Security**: reCAPTCHA integration

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - `FLASK_APP=jeddie`
   - `FLASK_ENV=development`
   - `STRIPE_SECRET_KEY=your_stripe_secret_key`
   - `RECAPTCHA_SITE_KEY=your_recaptcha_site_key`
   - `RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key`

## Running the Application

### Development server
```bash
flask run
```

### Production server
Please review the Flask documentation on [Deploying to Production](https://flask.palletsprojects.com/en/stable/deploying/).

### Transaction Refresh Tool
The application includes a standalone tool (`tools/refresh_transactions.py`) that manages pending Stripe transactions. This tool should be run as a cron job in production to:

1. Check pending payment intents
2. Update gift quantities when payments are confirmed
3. Cancel abandoned payment intents (older than 24 hours)

To set up the cron job, add an entry like this to your crontab:
```bash
*/15 * * * * cd /path/to/jeddie-wedding && ./venv/bin/python -m jeddie.tools.refresh_transactions
```

This will run the tool every 15 minutes to keep gift quantities in sync with payment status.

## Testing

Run the test suite:
```bash
pytest
```

## Project Structure

```
jeddie/
├── config/         # Configuration loader 
├── database/       # Database models and connection
├── exceptions/     # Custom exception handlers
├── logic/         # Business logic
├── middleware/    # Request middleware (reCAPTCHA, Stripe)
├── routes/        # Route handlers
├── static/        # Static assets (CSS, JS, images)
├── templates/     # HTML templates
└── tools/         # Utility functions
```

## Contributing

This is a private project for a wedding website. Please contact the repository owner for any questions or contributions.

## License

See the [LICENSE](LICENSE) file for details.
