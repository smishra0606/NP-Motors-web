# 🛵 N.P. Motors — Komaki Electric Vehicle Dealership

> **Full-stack Django web application** for N.P. Motors, the authorised Komaki Electric Vehicle dealership in Arwal, Bihar (India). The platform serves as both a **public-facing marketing website** and an **internal GST-compliant billing / Point-of-Sale (POS) system**.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Folder Structure](#-folder-structure)
- [Data Models](#-data-models)
- [URL Routes](#-url-routes)
- [Pages & Functionality](#-pages--functionality)
- [Management Commands](#-management-commands)
- [Getting Started (Local Development)](#-getting-started-local-development)
- [Deployment (Render.com)](#-deployment-rendercom)
- [Environment Variables](#-environment-variables)
- [Screenshots](#-screenshots)
- [License](#-license)

---

## ✨ Features

### Public Website
| Feature | Description |
|---|---|
| **Home Page** | Hero image slider (Swiper.js), stats strip, feature cards, vehicle catalog preview, showroom gallery, Google Maps embed, and contact section |
| **Vehicle Catalog** | Full searchable grid of Komaki EV models with specs (battery type, range, price), filter chips, and sort controls |
| **Spare Parts Catalog** | Dedicated section listing genuine Komaki spare parts with pricing |
| **WhatsApp Integration** | One-tap WhatsApp inquiry buttons throughout the site + floating WhatsApp FAB |
| **Click-to-Call** | Direct phone call buttons for instant customer contact |
| **Responsive Design** | Fully responsive with mobile hamburger navigation drawer |
| **SEO Optimised** | Proper `<title>`, `<meta description>`, semantic HTML, heading hierarchy on every page |

### Internal POS / Billing System
| Feature | Description |
|---|---|
| **Multi-Item Invoice Creation** | Staff can create invoices with multiple line items (vehicles + spare parts) via a rich AJAX-based POS interface |
| **Customer Management** | Auto-create or update customers by mobile number with smart duplicate detection (handles 10-digit / prefixed numbers) |
| **GST Tax Calculation** | Automatic CGST (2.5%) + SGST (2.5%) calculation on subtotals |
| **PDF Invoice Generation** | Professional A4 PDF invoices rendered via `xhtml2pdf` with company logo, QR code, itemised breakdown, and GST details |
| **QR Code on Invoices** | Each invoice PDF embeds a QR code linking to its unique URL |
| **UUID-Based Invoice IDs** | Every invoice gets a unique UUID for secure, non-sequential identification |
| **Hardware Serial Tracking** | Line items support optional hardware/serial number details (chassis no., battery no., etc.) |
| **Django Admin Panel** | Full admin interface for managing Vehicles, Spare Parts, Customers, and Invoices with inline items |
| **Login-Protected POS** | Invoice creation and PDF viewing require Django authentication |

### Data Management
| Feature | Description |
|---|---|
| **Excel Data Import** | Custom management command to bulk-import vehicles from `.xlsx` and spare parts from `.xls` files |
| **Gallery Image Management** | Utility script to map and copy asset images into the static gallery directory |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 6.1.1 (Python) |
| **Database** | SQLite (local dev) / PostgreSQL (production via `dj-database-url`) |
| **PDF Generation** | xhtml2pdf |
| **QR Code** | qrcode (Python library) |
| **Image Processing** | Pillow |
| **Data Import** | pandas, openpyxl, xlrd |
| **Frontend** | HTML5, Vanilla CSS (public pages), Tailwind CSS CDN (POS page) |
| **Fonts** | Google Fonts — Playfair Display (serif), Plus Jakarta Sans (sans-serif) |
| **Slider** | Swiper.js v11 (hero image carousel) |
| **Static Files** | WhiteNoise (production static file serving) |
| **WSGI Server** | Gunicorn (production) |
| **Hosting** | Render.com (configured) |

---

## 📁 Folder Structure

```
NP-Motors/                              # Workspace root
├── requirements.txt                    # Python dependencies (pip)
├── Procfile                            # Render.com process declaration
├── build.sh                            # Render.com build script
├── .gitignore                          # Git ignore rules
│
└── np_motors_project/                  # Django project root (manage.py level)
    ├── manage.py                       # Django CLI entry point
    ├── requirements.txt                # Python dependencies (duplicate for flexibility)
    ├── Procfile                        # Process declaration (duplicate)
    ├── build.sh                        # Build script (duplicate)
    ├── .gitignore                      # Git ignore rules
    ├── db.sqlite3                      # SQLite database (local dev)
    │
    ├── KOMAKI DEALER RATE LIST (1)-2.xlsx   # Source data: vehicle models & pricing
    ├── spare parts.xls                      # Source data: spare parts catalog
    ├── copy_gallery_images.py               # Utility: copies asset images to static/gallery
    │
    ├── np_motors_project/              # Django project configuration
    │   ├── __init__.py
    │   ├── settings.py                 # Settings (DB, middleware, static, etc.)
    │   ├── urls.py                     # Root URL configuration
    │   ├── wsgi.py                     # WSGI application entry point
    │   └── asgi.py                     # ASGI application entry point
    │
    ├── billing_app/                    # Main Django application
    │   ├── __init__.py
    │   ├── admin.py                    # Admin panel configuration
    │   ├── apps.py                     # App configuration
    │   ├── forms.py                    # Django ModelForms (Customer, Invoice)
    │   ├── models.py                   # Data models (Vehicle, SparePart, Customer, Invoice, InvoiceItem)
    │   ├── urls.py                     # App URL routes
    │   ├── views.py                    # View functions (home, catalog, create_invoice, view_invoice_pdf)
    │   ├── tests.py                    # Test cases (placeholder)
    │   │
    │   ├── management/
    │   │   └── commands/
    │   │       └── import_data.py      # Custom command: import vehicles & spare parts from Excel
    │   │
    │   ├── migrations/                 # Database migration files
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_invoice_extra_amount_invoice_extra_notes_and_more.py
    │   │   └── 0003_remove_invoice_battery_no_remove_invoice_charger_no_and_more.py
    │   │
    │   ├── assets/                     # Raw source images (showroom/delivery photos)
    │   │   ├── logo.png
    │   │   └── 2.jpeg ... 13.jpeg      # 12 source photographs
    │   │
    │   ├── static/billing_app/         # Static assets served to the browser
    │   │   └── images/
    │   │       ├── logo.png            # Company logo
    │   │       ├── hero_scooter.jpg    # Hero section background
    │   │       ├── feature_no_rto.jpg  # Feature card: No RTO
    │   │       ├── feature_range.jpg   # Feature card: Range
    │   │       ├── feature_spares.jpg  # Feature card: Spares
    │   │       ├── estimate_book.jpg   # Estimate book image
    │   │       ├── visiting_card.jpg   # Visiting card image
    │   │       └── gallery/
    │   │           ├── delivery_1.jpg  # Customer delivery photo
    │   │           ├── delivery_2.jpg  # Customer delivery photo
    │   │           ├── showroom_1.jpg  # Showroom display photo
    │   │           └── showroom_2.jpg  # Showroom display photo
    │   │
    │   └── templates/billing_app/      # Django HTML templates
    │       ├── base.html               # Base layout (navbar, footer, CSS variables, WhatsApp FAB)
    │       ├── home.html               # Home page (hero slider, stats, features, catalog preview, gallery, map)
    │       ├── catalog.html            # Full vehicle & spare parts catalog
    │       ├── create_invoice.html     # POS invoice creation interface (Tailwind CSS)
    │       └── invoice_pdf.html        # PDF invoice template (A4, xhtml2pdf compatible)
    │
    └── staticfiles/                    # Collected static files (generated by collectstatic)
```

---

## 🗃 Data Models

### `Vehicle`
| Field | Type | Description |
|---|---|---|
| `name` | CharField(255) | Model name (e.g., "XGT KM 3000") |
| `battery_type` | CharField(100) | Battery specification (e.g., "Lithium 3.0 KWH") |
| `range_km` | CharField(100) | Distance range (e.g., "120-150 KM") |
| `price` | DecimalField(10,2) | Sale price in INR |
| `image` | ImageField | Optional vehicle photo |

### `SparePart`
| Field | Type | Description |
|---|---|---|
| `name` | CharField(255) | Part name |
| `price` | DecimalField(10,2) | Price in INR |
| `applicable_models` | CharField(255) | Compatible vehicle models |

### `Customer`
| Field | Type | Description |
|---|---|---|
| `name` | CharField(255) | Full name |
| `mobile` | CharField(15) | Mobile number (used for deduplication) |
| `address` | TextField | Full address |
| `aadhar_no` | CharField(20) | Aadhaar number (optional, masked in PDF) |

### `Invoice`
| Field | Type | Description |
|---|---|---|
| `unique_bill_id` | UUIDField | Auto-generated unique invoice identifier |
| `customer` | ForeignKey → Customer | Linked customer |
| `subtotal` | DecimalField(10,2) | Sum of all line item amounts |
| `cgst` | DecimalField(10,2) | Auto-calculated: subtotal × 2.5% |
| `sgst` | DecimalField(10,2) | Auto-calculated: subtotal × 2.5% |
| `total_amount` | DecimalField(10,2) | subtotal + CGST + SGST |
| `created_at` | DateTimeField | Auto-set on creation |

### `InvoiceItem`
| Field | Type | Description |
|---|---|---|
| `invoice` | ForeignKey → Invoice | Parent invoice |
| `item_name` | CharField(255) | Product/service name |
| `hardware_details` | TextField | Optional serial/chassis/battery numbers |
| `hsn_code` | CharField(50) | HSN/SAC code (default: 8714) |
| `quantity` | PositiveIntegerField | Quantity (default: 1) |
| `rate` | DecimalField(10,2) | Unit price |
| `amount` | DecimalField(10,2) | quantity × rate |

---

## 🔗 URL Routes

| URL Pattern | View | Auth | Description |
|---|---|---|---|
| `/` | `home` | ❌ | Public home page |
| `/catalog/` | `catalog` | ❌ | Vehicle & spare parts catalog |
| `/create-invoice/` | `create_invoice` | ✅ | POS invoice creation (GET: form, POST: JSON API) |
| `/invoice/<uuid>/` | `view_invoice_pdf` | ✅ | Generate & serve invoice as PDF |
| `/admin/` | Django Admin | ✅ | Admin panel |

---

## 📄 Pages & Functionality

### 1. Home Page (`/`)
- **Hero Slider**: Full-viewport image carousel with overlay, animated text, CTA buttons (Swiper.js with fade effect, autoplay)
- **Stats Strip**: Animated counters (vehicles sold, models available, years in business, happy customers)
- **Feature Cards**: Three cards highlighting No-RTO models, 100+ KM range, and genuine spare parts
- **Vehicle Preview**: Grid of up to 6 featured vehicles with specs and WhatsApp inquiry buttons
- **Gallery**: Showroom and delivery photos grid
- **Contact Section**: Address, phone numbers, GSTIN, Google Maps iframe, WhatsApp/Call CTAs

### 2. Catalog Page (`/catalog/`)
- **Dark Hero Banner**: Breadcrumb, title, subtitle, vehicle count badge
- **Sticky Filter Bar**: Category filter chips (All, Scooters, High-Speed) + sort dropdown (Price: Low→High, High→Low, Newest)
- **Vehicle Grid**: Full catalog of Komaki models with image, specs (battery, range), price, WhatsApp + Call action buttons
- **Spare Parts Section**: Dedicated section with spare parts table/grid
- **Client-Side Filtering**: JavaScript-based instant filtering and sorting without page reload

### 3. Create Invoice (`/create-invoice/`) — *Login Required*
- **POS-Style Interface**: Dark header with staff name, two-column layout
- **Customer Section**: Name, mobile, address, Aadhaar input fields
- **Item Builder**: Dynamic add/remove line items with vehicle/spare dropdown, auto-populated pricing, quantity, hardware details, HSN code
- **Live Preview Card**: Real-time subtotal, CGST, SGST, and grand total calculation
- **AJAX Submission**: JSON POST to the server, atomic database transaction, redirect to PDF on success
- **Error Handling**: Validation messages for missing fields, duplicate detection

### 4. Invoice PDF (`/invoice/<uuid>/`) — *Login Required*
- **A4 Portrait Layout**: Designed for print with precise margins
- **Header**: Company logo (base64 embedded), dealership name, address, GSTIN, "GST TAX INVOICE" badge
- **Customer Block**: Name, address, mobile, masked Aadhaar
- **Invoice Meta**: Invoice number, date, state code
- **Itemised Table**: Sr. No., Item name, HSN code, hardware details, quantity, rate, amount
- **Tax Breakdown**: Subtotal, CGST @ 2.5%, SGST @ 2.5%, Grand Total
- **Amount in Words**: Total amount in Indian Rupees
- **QR Code**: Links back to the invoice URL
- **Signature Block**: Authorised signatory section
- **Terms & Conditions**: Standard warranty and sales terms

---

## ⚙ Management Commands

### Import Data from Excel
```bash
python manage.py import_data
```
Reads `KOMAKI DEALER RATE LIST (1)-2.xlsx` for vehicle models and `spare parts.xls` for spare parts, then uses `update_or_create` to safely insert/update records in the database.

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd NP-Motors/np_motors_project

# 2. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Create a superuser (for admin & POS access)
python manage.py createsuperuser

# 6. Import vehicle & spare parts data from Excel files
python manage.py import_data

# 7. Start the development server
python manage.py runserver
```

### Access Points
| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/` | Public website |
| `http://127.0.0.1:8000/catalog/` | Vehicle catalog |
| `http://127.0.0.1:8000/create-invoice/` | POS (login required) |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

---

## ☁ Deployment (Render.com)

The project is pre-configured for deployment on [Render.com](https://render.com).

### Deployment Files
| File | Purpose |
|---|---|
| `requirements.txt` | Python package dependencies |
| `build.sh` | Build script (install deps, collectstatic, migrate) |
| `Procfile` | Gunicorn web process declaration |

### Production Configuration (settings.py)
- **SECRET_KEY**: Read from `SECRET_KEY` environment variable
- **DEBUG**: Automatically `False` when `RENDER` env var is present
- **Database**: PostgreSQL via `DATABASE_URL` env var (falls back to SQLite locally)
- **Static Files**: WhiteNoise middleware serves static assets
- **STATIC_ROOT**: `staticfiles/` (generated by `collectstatic`)

### Render Setup Steps

1. **Push to GitHub** — Ensure your repo includes `requirements.txt`, `build.sh`, and `Procfile`
2. **Create Web Service** on Render Dashboard:
   - **Root Directory**: `np_motors_project`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn np_motors_project.wsgi`
3. **Add Environment Variables**:
   - `SECRET_KEY` — A secure random string
   - `DATABASE_URL` — Your Render PostgreSQL Internal Connection String
   - `PYTHON_VERSION` — e.g., `3.12.0`
4. **Create PostgreSQL Database** on Render and link it

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ (production) | Django secret key for cryptographic signing |
| `DATABASE_URL` | ✅ (production) | PostgreSQL connection string |
| `RENDER` | Auto-set | Render.com sets this; toggles `DEBUG = False` |

---

## 📸 Screenshots

> Run the development server and visit the pages to see the live UI.

| Page | URL |
|---|---|
| Home | `http://127.0.0.1:8000/` |
| Catalog | `http://127.0.0.1:8000/catalog/` |
| POS / Create Invoice | `http://127.0.0.1:8000/create-invoice/` |
| Invoice PDF | `http://127.0.0.1:8000/invoice/<uuid>/` |
| Admin | `http://127.0.0.1:8000/admin/` |

---

## 🏢 Business Information

| Detail | Value |
|---|---|
| **Dealership** | N.P. Motors |
| **Brand** | Komaki Electric Vehicles |
| **Location** | Gaura, Near Sainik Canteen, Belkhara Road, Arwal, Bihar — 804402 |
| **Phone** | +91 9546992511, +91 9973738049 |
| **GSTIN** | 10EUKPK8054G1ZN |
| **State Code** | 10 (Bihar) |
| **Hours** | Mon–Sat: 9 AM – 7 PM · Sun: 10 AM – 4 PM |

---

## 📄 License

This project is proprietary software built for N.P. Motors. All rights reserved.

---

<p align="center">
  <strong>Built with ❤️ for N.P. Motors — Komaki Electric Vehicle Division</strong><br>
  <em>© 2026 N.P. Motors. All Rights Reserved.</em>
</p>
