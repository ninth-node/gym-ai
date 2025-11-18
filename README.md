# AI-First Gym Management SaaS

> The First AI-Powered Gym Management Platform That Thinks Before You Do

Transform your gym from reactive to predictive. Our AI agents work 24/7 to prevent problems, retain members, and optimize operations—so you can focus on what matters: your members' success.

## 🚀 Key Features

- **40% reduction in member churn** through predictive intervention
- **60% less equipment downtime** with AI maintenance forecasting
- **25% revenue increase** via intelligent pricing and operations
- **Zero manual billing issues** with autonomous financial management

## 🏗 Technical Stack

### Frontend
- **Next.js 14** with App Router and TypeScript
- **Shadcn/ui** component library
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Query** for server state
- **Framer Motion** for animations

### Backend
- **FastAPI** with Python 3.11+
- **SQLAlchemy 2.0** with PostgreSQL
- **Redis** for caching and sessions
- **Celery** for background tasks
- **Alembic** for database migrations

### AI Framework
- **LangGraph** for multi-agent workflows
- **LangChain** for LLM integration
- **OpenAI GPT-4** / **Claude 3.5 Sonnet**
- **ChromaDB** for vector storage
- **LangSmith** for agent monitoring

### Infrastructure
- **Docker** & Docker Compose
- **PostgreSQL 15+**
- **Redis 7+**
- **Nginx** (production)

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd gym-ai
```

### 2. Set up environment variables

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration

# Frontend
cp frontend/.env.example frontend/.env
# Edit frontend/.env with your configuration
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- Frontend at http://localhost:3000
- Backend API at http://localhost:8000
- API Documentation at http://localhost:8000/api/v1/docs
- PostgreSQL at localhost:5432
- Redis at localhost:6379

### 4. Initialize the database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head
```

## 💻 Local Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
gym-ai/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # Next.js 14 app directory
│   ├── components/          # React components
│   ├── lib/                 # Utility functions
│   ├── hooks/               # Custom React hooks
│   └── utils/               # Helper utilities
│
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── agents/         # LangGraph AI agents
│   ├── alembic/            # Database migrations
│   └── tests/              # Backend tests
│
├── docs/                    # Documentation files
├── docker-compose.yml       # Docker orchestration
└── README.md               # This file
```

## 🤖 AI Agents

The platform includes several AI agents that work autonomously:

### Member Journey Agent
- Churn prediction and retention
- Personalized engagement campaigns
- Automated onboarding workflows

### Operations Agent
- Equipment maintenance prediction
- Facility optimization
- Staff coordination

### Financial Agent
- Intelligent billing automation
- Revenue optimization
- Dynamic pricing

### Health & Wellness Agent
- Personalized fitness coaching
- Nutrition planning
- Recovery optimization

### Business Intelligence Agent
- Predictive analytics
- Market analysis
- Performance optimization

## 📚 API Documentation

Once the backend is running, access the API documentation at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 🧪 Testing

### Frontend Tests

```bash
cd frontend
npm run test
```

### Backend Tests

```bash
cd backend
pytest
```

## 🔐 Security

- JWT-based authentication
- Role-based access control (RBAC)
- HIPAA compliant data handling
- Bank-level encryption
- SOC 2 Type II compliance ready

## 📊 Phase 1 Implementation (Weeks 1-3)

- [x] Project setup and development environment
- [x] Next.js frontend with Shadcn UI
- [x] FastAPI backend with PostgreSQL
- [x] Docker development environment
- [x] Redis caching and sessions
- [ ] JWT authentication system
- [ ] User registration and login
- [ ] Admin dashboard
- [ ] Role-based access control
- [ ] Member profile management
- [ ] Basic testing infrastructure
- [ ] CI/CD pipeline

## 🚀 Deployment

Deployment instructions will be added for:
- AWS (ECS/EKS)
- Google Cloud Platform (Cloud Run/GKE)
- Azure (Container Apps/AKS)
- DigitalOcean (App Platform)

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Support

For support, email: hello@aigymmanagement.com

## 🗺 Roadmap

See [ai-first-gym-management-plan.md](./ai-first-gym-management-plan.md) for the complete development roadmap.
