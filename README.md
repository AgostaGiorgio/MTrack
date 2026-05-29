# MTrack 💳 - Expense Tracking Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue.js-4C4C4C?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

**MTrack** is a minimal and effective personal expense tracking platform. It provides a clear overview of your spending habits through an interactive dashboard, a transaction list with category reassignment, and a full category/subcategory management system. **Data ingestion is fully automated** via an external n8n pipeline that reads from your financial sources and populates the database — MTrack focuses purely on visualization and categorization.

---

## ✨ Key Features

| Emoji | Feature | Description |
|:-----:|---------|-------------|
| 📊 | **Dashboard Overview** | Current month total spent, per-card breakdown, category pie chart, and monthly trends |
| 💳 | **Card Tracking** | See spending aggregated by payment card |
| 🏷️ | **Category Hierarchy** | Two-level categorization system (primary + secondary/subcategories) with custom Lucide icons |
| ✏️ | **Transaction Editing** | Reassign primary and secondary categories to any transaction |
| 📈 | **Monthly Trends** | Visualize spending evolution over the last 12 months |
| 🤖 | **Automated Ingestion** | All transaction data is inserted by an n8n pipeline — no manual entry needed |
| 🖼️ | **Icon Picker** | Assign Lucide icons to categories for visual clarity |
| 🌐 | **REST API** | Full FastAPI backend with async operations |
| 🔒 | **Self-Hosted & Private** | Keep full control over your financial data by running the stack locally |

---

## 🏗️ Project Structure

```
MTrack/
├── backend/                   # 🐍 FastAPI backend
│   ├── src/
│   │   ├── main.py           # 📍 Application entry point
│   │   ├── di.py             # 🧩 Dependency injection container
│   │   ├── config/          # ⚙️ Configuration
│   │   ├── models/          # 📋 Pydantic models
│   │   ├── routers/         # 🛤️ API endpoints
│   │   ├── services/        # 🔧 Business logic
│   │   ├── repositories/    # 🗄️ Database queries
│   │   └── clients/         # 🔌 External clients
│   └── pyproject.toml      # 📦 Python dependencies
├── frontend/                 # 🎨 Vue.js 3 frontend
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── views/          # 📄 Page components
│   │   ├── components/     # 🧱 Reusable UI components
│   │   └── services/       # 📡 API client
│   └── package.json
```

---

## 🌐 API Endpoints

### Dashboard
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/v1/dashboard` | 📊 Get dashboard summary (total spent, cards, categories, trends) |

### Transactions
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/v1/transactions` | 📄 Get all transactions |
| `PUT` | `/api/v1/transactions/{id}` | ✏️ Update transaction categories |

### Categories
| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/v1/categories` | 📋 Get all categories with subcategories |
| `POST` | `/api/v1/categories` | ➕ Create new category |
| `PUT` | `/api/v1/categories/{id}` | ✏️ Update category name/icon |
| `PUT` | `/api/v1/categories/{id}/sub/{sub_id}/unlink` | 🔗 Unlink a subcategory |

---

## 🛠️ Tech Stack

### Backend
| Technology | Icon | Description |
|------------|------|-------------|
| **Python 3.10+** | 🐍 | [Documentation](https://www.python.org/) - Async/await support |
| **FastAPI** | ⚡ | [Documentation](https://fastapi.tiangolo.com/) - Modern async web framework |
| **SQLAlchemy 2.0** | 🗄️ | [Documentation](https://www.sqlalchemy.org/) - Async ORM with asyncpg |
| **Poetry** | 📦 | [Documentation](https://python-poetry.org/) - Dependency management |
| **Dependency Injector** | 🧩 | [Documentation](https://python-dependency-injector.ets-labs.org/) - DI container |
| **Pydantic** | ✅ | [Documentation](https://docs.pydantic.dev/) - Data validation |

### Frontend
| Technology | Icon | Description |
|------------|------|-------------|
| **Vue.js 3** | 💚 | [Documentation](https://vuejs.org/) - Progressive JavaScript framework |
| **Vite** | ⚡ | [Documentation](https://vitejs.dev/) - Next-generation build tool |
| **Tailwind CSS** | 💨 | [Documentation](https://tailwindcss.com/) - Utility-first CSS framework |
| **Chart.js** | 📊 | [Documentation](https://www.chartjs.org/) - Data visualization |
| **vue-chartjs** | 📈 | [Documentation](https://vue-chartjs.org/) - Vue.js wrapper for Chart.js |
| **Axios** | 📡 | [Documentation](https://axios-http.com/) - HTTP client |
| **Vue Router** | 🗺️ | [Documentation](https://router.vuejs.org/) - Client-side routing |
| **Lucide** | 🎨 | [Documentation](https://lucide.dev/) - Icon library |

### Database
> 🐘 **PostgreSQL** - [Documentation](https://www.postgresql.org/) - Relational database

### DevOps
> ☸️ **Kubernetes** & **ArgoCD** - [Documentation](https://github.com/AgostaGiorgio/HomeLab/tree/master/apps/mtrack) - Deployment via ArgoCD Application

---

## 🔄 Automation & Data

All transaction data is ingested automatically via an **n8n pipeline**:
- 🤖 **Automated Insertion:** The n8n workflow fetches transaction data from your financial sources (bank cards, accounts, etc.) and inserts them into the MTrack database
- 🏷️ **Auto-Categorization:** Initial category assignment is handled by the pipeline based on predefined rules
- 👤 **Manual Refinement:** You can reassign categories through the MTrack UI when the automation gets it wrong

---

## 📋 Data Models

### Transaction
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `amount` | float | Transaction amount |
| `date` | datetime | Transaction date |
| `description` | string | Transaction description |
| `card` | string | Payment card name |
| `primary_category` | Category/UUID | Main category |
| `secondary_category` | Category/UUID | Subcategory (optional) |

### Category
| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `name` | string | Category name |
| `icon` | string | Lucide icon name |
| `sub_categories` | list[Category] | Nested subcategories |

### Dashboard Data
| Field | Type | Description |
|-------|------|-------------|
| `current_month` | string | Current month label |
| `total_spent` | float | Total spending for current month |
| `cards_summary` | list[CardSummary] | Spending per card |
| `categories_summary` | list[CategorySummary] | Spending per category with subcategories |
| `monthly_trends` | list[MonthlyTrend] | Monthly spending over the last year |

---

## 🚀 Getting Started

### Quick Start (ArgoCD)
1. Clone the repository
2. Configure your environment variables in `backend/.env` (use `.env.example` as a template)
3. The application is deployed via ArgoCD - see the [ArgoCD Application definition](https://github.com/AgostaGiorgio/HomeLab/tree/master/apps/mtrack) for configuration

### Local Development

#### Backend Setup
```bash
cd backend
poetry install
poetry run uvicorn src.main:app --reload --port 8080
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📄 License

> 📝 **MIT License** - Feel free to use and modify!
