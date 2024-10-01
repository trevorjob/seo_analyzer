# Project Title

This project is an SEO Analyzer API built using Django REST Framework and a React.js frontend with TailwindCSS. The SEO Analyzer allows users to submit a URL and receive a detailed report on various SEO metrics such as page title, meta description, canonical URL, mobile friendliness, keyword density, page speed, and more.

## Features

- Analyze any URL for SEO performance.
- Get detailed information about:
  - Page Title
  - Meta Description
  - Canonical URL
  - Mobile Friendliness
  - SSL Certificate presence
  - Robots.txt presence
  - Images without Alt Text
  - Page Speed (in milliseconds)
  - SEO Score
  - Keyword Density
  - Open Graph Tags (visualized in the frontend)
  - Broken Links
  - Headings and Hreflang Tags
- Responsive frontend built with React and TailwindCSS.
- Backend API built with Django REST Framework.

## project structure

```.
├── backend/
|   ├──analyzer/
│   ├── seo_analyzer/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   ├── manage.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   ├── tailwind.config.js
│   ├── package.json
├── README.md
└── .gitignore
```

## Installation

### Backend Setup

- Clone the Repository:

```
git clone https://github.com/your-username/seo-analyzer.git
cd seo-analyzer/backend
```

- Create and Activate a Virtual Environment:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

- Install Backend Dependencies:

```
pip install -r requirements.txt
```

- Run Migrations:

```
python manage.py migrate
```

Start the Django Development Server:

```
python manage.py runserver
```

The backend should now be running on http://localhost:8000.

### Frontend Setup

- Navigate to the Frontend Directory:

```
cd ./frontend
```

- Install Frontend Dependencies:

```
npm install
```

- Start the React Development Server:

```
npm start
```

The frontend should now be running on http://localhost:3000.

## API Reference

#### analyze site

```http
  GET /api/analyze/
```

| Parameter | Type     | Description   |
| :-------- | :------- | :------------ |
| `url`     | `string` | **Required**. |

## Tech Stack

**Client:** React, TailwindCSS, Axios

**Server:** Django rest framework, python, beautifullsoup4

## Future Enhancements

- **Advanced SEO Metrics**: Implement additional - \*\*SEO metrics such as structured data (Schema.org), more detailed mobile analysis, and richer keyword analysis.
- **User Authentication**: Add user authentication for storing historical analyses for registered users.
- **Historical Reports**: Allow users to view past SEO analysis results and track changes over time.
- **Pagination**: Improve frontend performance by adding pagination for large results.
- **Multilingual Support**: Analyze hreflang tags to detect multi-language support for websites.

## Contributing

Contributions to the SEO Analyzer are welcome! Here's how you can contribute:

- Fork the repository.
- Create a new feature branch.
- Commit your changes.
- Open a pull request describing the changes.
