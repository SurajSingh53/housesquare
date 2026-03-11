# 🏡 HouseSquare — Real Estate Listing Platform

A full-stack Django real estate platform where owners can list properties and buyers/renters can browse, filter, and inquire.

---

## 🗂️ Project Structure

```
housesquare/
├── manage.py
├── requirements.txt
├── db.sqlite3                    ← Created on first migrate
│
├── housesquare/                  ← Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── listings/                     ← Main app
│   ├── models.py                 ← Property, Agent, Inquiry, City, EnlistRequest
│   ├── views.py                  ← Home, List, Detail, Enlist, Agents
│   ├── urls.py                   ← All URL routes
│   ├── forms.py                  ← InquiryForm, EnlistForm, SearchForm
│   ├── admin.py                  ← Full admin panel config
│   └── management/
│       └── commands/
│           └── seed_data.py      ← Seeds DB with sample listings
│
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── navbar.html
│   │   └── footer.html
│   └── listings/
│       ├── home.html             ← Homepage with featured listings
│       ├── listing_list.html     ← Browse + filter page
│       ├── listing_detail.html   ← Property detail + inquiry form
│       ├── enlist.html           ← Submit your property form
│       ├── enlist_success.html
│       ├── agents.html
│       └── agent_detail.html
│
├── static/
│   ├── css/style.css             ← Full stylesheet (terracotta + cream theme)
│   ├── js/main.js                ← Navbar, scroll reveal, interactions
│   └── assets/images/
│       ├── hero-house.jpg        ← SVG hero image
│       ├── placeholder.svg       ← Fallback image
│       └── properties/           ← 8 dummy property SVG images
│
└── media/                        ← User-uploaded files (images)
    └── properties/
```

---

## ⚡ Quick Start

### 1. Clone / extract the project
```bash
cd housesquare
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed sample data (8 properties, 4 agents, 8 cities)
```bash
python manage.py seed_data
```

### 6. Create admin user
```bash
python manage.py createsuperuser
```

### 7. Start the server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser 🎉

---

## 🔐 Admin Panel

Visit **http://127.0.0.1:8000/admin**

Manage:
- **Properties** — with inline image uploads and inquiry viewing
- **Agents** — verified/unverified status
- **Inquiries** — mark as New / Contacted / Closed
- **Enlist Requests** — Approve or Reject submitted listings
- **Cities** — manage city data

---

## 🌐 URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | `home` | Homepage with featured listings |
| `/properties/` | `listing_list` | Browse & filter all properties |
| `/properties/<slug>/` | `listing_detail` | Property detail page |
| `/enlist/` | `enlist` | Owner property submission form |
| `/enlist/success/` | `enlist_success` | Submission confirmation |
| `/agents/` | `agent_list` | All verified agents |
| `/agents/<id>/` | `agent_detail` | Agent profile + their listings |
| `/admin/` | Admin panel | Django admin |

---

## 📦 Models

| Model | Description |
|-------|-------------|
| `City` | Cities with state names |
| `Agent` | Verified real estate agents |
| `Property` | Full property listing (30+ fields) |
| `PropertyImage` | Gallery images per property |
| `Inquiry` | Buyer/renter contact messages |
| `PropertyEnlistRequest` | Public owner form submissions |

---

## 🎨 Tech Stack

- **Backend**: Django 4.2 + SQLite (swap to Postgres for production)
- **Frontend**: Vanilla HTML/CSS/JS, Google Fonts (Playfair Display + DM Sans)
- **Images**: Pillow for upload handling, SVG dummy images included
- **Theme**: Terracotta + Cream luxury editorial palette

---

## 🚀 Production Checklist

- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Switch to PostgreSQL
- [ ] Configure S3/Cloudinary for media files
- [ ] Run `python manage.py collectstatic`
- [ ] Deploy with Gunicorn + Nginx
