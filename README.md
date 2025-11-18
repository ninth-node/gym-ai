# AI-First Gym Management SaaS

> The First AI-Powered Gym Management Platform That Thinks Before You Do

Transform your gym from reactive to predictive. Our AI agents work 24/7 to prevent problems, retain members, and optimize operations—so you can focus on what matters: your members' success.

## 📊 Current Implementation Status

✅ **Phase 1 Complete**: Foundation & Core Infrastructure
✅ **Phase 2 Complete**: AI Agent Infrastructure & Core Automation
🚧 **Phase 3-7**: Advanced features (see roadmap)

---

## 🚀 Completed Features

### 🔐 Authentication & Authorization
- ✅ **JWT Authentication System**
  - Access tokens (30-min expiry) & refresh tokens (7-day expiry)
  - Secure password hashing with bcrypt
  - Token-based API authentication
  - Automatic token refresh mechanism
- ✅ **Role-Based Access Control (RBAC)**
  - 4-tier role hierarchy: Super Admin → Admin → Staff → Member
  - Granular permissions per endpoint
  - Role requirement decorators for endpoints

### 👥 Member Management
- ✅ **Member Profiles & Registration**
  - Complete member profiles with personal information
  - QR code generation for contactless check-ins
  - Fitness goals and medical conditions tracking
  - Emergency contact information
  - Member status management (active/inactive/suspended)
- ✅ **Membership Plans**
  - Flexible plan creation with custom pricing and duration
  - Feature flags (max classes per month, personal trainer access)
  - Plan association with members
  - CRUD operations for plans
- ✅ **Check-in/Check-out System**
  - Real-time check-in tracking with timestamps
  - Multiple check-in methods (QR code, manual, biometric)
  - Check-out functionality
  - Active occupancy tracking
  - Historical check-in data

### 📊 Dashboard & Analytics
- ✅ **Admin Dashboard**
  - Real-time statistics (total members, active members, today's check-ins, current occupancy)
  - Quick action buttons for common tasks
  - Responsive stat cards with live updates
  - AI insights section
- ✅ **API Statistics Endpoints**
  - Dashboard metrics aggregation
  - Member activity tracking
  - Occupancy analytics

### 🤖 AI Agent Infrastructure
- ✅ **Base Agent Framework**
  - Abstract base agent class with lifecycle management
  - Agent state management (IDLE, RUNNING, COMPLETED, FAILED)
  - Configurable timeouts and error handling
  - Result tracking with success/failure states
- ✅ **LLM Integration**
  - Multi-provider support (OpenAI GPT-4, Anthropic Claude)
  - Configurable LLM parameters (temperature, max tokens)
  - Fallback handling for API failures
- ✅ **Vector Storage**
  - ChromaDB integration for knowledge base
  - Persistent storage configuration ready
- ✅ **Monitoring Framework**
  - LangSmith integration framework (partial implementation)
  - Local logging capabilities
  - Agent execution tracking

### 🎯 Operational AI Agents

#### Member Engagement Agent
- ✅ **Churn Prediction**
  - Heuristic-based churn risk scoring (0.0-1.0)
  - Multi-factor analysis (attendance, engagement, membership status)
  - At-risk member identification (risk score ≥ 0.7)
- ✅ **Retention Strategies**
  - AI-generated personalized retention messages
  - Custom incentive recommendations
  - Follow-up action suggestions
  - Engagement metric calculations
- ✅ **API Endpoints**
  - `/api/v1/agents/engagement/execute` - Run full analysis
  - `/api/v1/agents/engagement/analyze` - Analyze specific data
  - `/api/v1/agents/engagement/at-risk-members` - Get at-risk list

#### Operations Agent
- ✅ **Equipment Management**
  - Equipment tracking (name, category, status, location)
  - Usage metrics (total count, total hours)
  - Maintenance scheduling (last maintenance, next due date)
  - IoT device field preparation (device_id, last_sync)
  - Maintenance prediction based on usage thresholds
- ✅ **Facility Capacity Analysis**
  - Real-time occupancy tracking
  - Daily check-in trend analysis (7-day rolling)
  - Peak hours identification
  - Capacity utilization calculations
- ✅ **API Endpoints**
  - `/api/v1/agents/operations/execute` - Run operations analysis
  - `/api/v1/agents/operations/maintenance-predictions` - Get maintenance schedule
  - `/api/v1/agents/operations/capacity-analysis` - Get capacity insights

#### Financial Agent
- ✅ **Revenue Analytics**
  - Monthly Recurring Revenue (MRR) calculations
  - Revenue forecasting with growth projections (30/60/90 days)
  - Historical revenue tracking
- ✅ **Membership Financial Management**
  - Expiring membership identification
  - Renewal opportunity tracking
  - Membership duration analysis
- ✅ **Pricing Optimization**
  - Plan-level pricing analysis
  - Demand analysis by plan
  - Price adjustment recommendations
- ✅ **API Endpoints**
  - `/api/v1/agents/financial/execute` - Run financial analysis
  - `/api/v1/agents/financial/revenue-forecast` - Get revenue projections
  - `/api/v1/agents/financial/expiring-memberships` - Get renewal opportunities
  - `/api/v1/agents/financial/pricing-recommendations` - Get pricing insights

### 🗄️ Database & Infrastructure
- ✅ **PostgreSQL Database**
  - Async SQLAlchemy 2.0 ORM
  - 5 main models: User, Member, MembershipPlan, CheckIn, Equipment
  - Alembic migrations (3 migrations completed)
  - Relationship mapping between entities
- ✅ **Redis Caching**
  - Session management
  - Caching layer for frequently accessed data
  - Pub/sub ready for real-time features
- ✅ **ChromaDB Vector Database**
  - Vector storage for AI knowledge base
  - Semantic search capabilities
  - Persistent storage configuration
- ✅ **Background Task Processing**
  - Celery worker for async tasks
  - Celery Beat for scheduled tasks
  - Redis broker integration

### 🎨 Frontend (Next.js 14)
- ✅ **Authentication UI**
  - Login page with form validation
  - Registration page with success flow
  - Protected route handling
  - Auto-redirect on auth state changes
- ✅ **Dashboard Interface**
  - Responsive admin dashboard
  - Real-time statistics display
  - Quick action buttons
  - Modern navigation bar
- ✅ **UI Component Library**
  - Shadcn/ui components (Button, Input, Label, etc.)
  - 15+ Radix UI primitives configured
  - Consistent design system
  - Accessible components
- ✅ **State Management**
  - Zustand store for authentication state
  - API client with automatic token injection
  - Token storage in localStorage
  - Request/response interceptors
- ✅ **Styling System**
  - Tailwind CSS with custom design tokens
  - Dark mode variables defined
  - Responsive breakpoints configured
  - Animation utilities (tailwindcss-animate)

### 🐳 DevOps & Development
- ✅ **Docker Compose Environment**
  - 7 services: PostgreSQL, Redis, ChromaDB, Backend, Frontend, Celery Worker, Celery Beat
  - Health checks for database services
  - Volume persistence for data
  - Hot-reloading for development
- ✅ **Development Tools**
  - Makefile with common commands
  - Environment configuration templates
  - API documentation (Swagger/ReDoc)
- ✅ **Package Management**
  - Python dependencies managed with requirements.txt
  - Node.js dependencies with package.json
  - Version pinning for stability

---

## 🏗 Technical Stack

### Frontend (Next.js 14)
- **Framework**: Next.js 14 with App Router and TypeScript
- **UI Library**: Shadcn/ui component library
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand for auth and global state
- **API Client**: Custom client with automatic token management
- **Animations**: Framer Motion (configured, not yet used)

### Backend (FastAPI + Python 3.11)
- **API Framework**: FastAPI with async/await support
- **Database ORM**: SQLAlchemy 2.0 with PostgreSQL
- **Caching**: Redis for sessions and real-time features
- **Background Tasks**: Celery with Redis broker
- **Migrations**: Alembic for database schema versioning
- **Authentication**: JWT with access and refresh tokens

### AI/ML Stack
- **Agent Framework**: LangGraph for multi-agent orchestration
- **LLM Integration**: LangChain with OpenAI/Anthropic support
- **Vector Database**: ChromaDB for knowledge storage
- **Monitoring**: LangSmith framework (partial implementation)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15+ with async support
- **Cache**: Redis 7+ for sessions and pub/sub
- **Vector Store**: ChromaDB for AI knowledge base

---

## 📁 Detailed Project Structure

```
gym-ai/
├── frontend/                          # Next.js 14 Application
│   ├── app/
│   │   ├── auth/
│   │   │   ├── login/page.tsx        # Login page with form validation
│   │   │   └── register/page.tsx     # Registration with success flow
│   │   ├── dashboard/page.tsx        # Admin dashboard with stats
│   │   ├── layout.tsx                # Root layout with metadata
│   │   ├── page.tsx                  # Landing page
│   │   └── globals.css               # Global styles with design tokens
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── navbar.tsx            # Dashboard navigation
│   │   │   └── stat-card.tsx         # Metric display cards
│   │   └── ui/                       # Shadcn UI components
│   │       ├── button.tsx            # Button with variants
│   │       ├── input.tsx             # Form input field
│   │       └── label.tsx             # Form label
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts             # API client with auth
│   │   │   ├── auth.ts               # Auth API methods
│   │   │   └── members.ts            # Member API methods
│   │   ├── store/
│   │   │   └── auth.ts               # Zustand auth store
│   │   └── utils.ts                  # cn() utility for classnames
│   └── package.json                  # Dependencies
│
├── backend/                           # FastAPI Application
│   ├── app/
│   │   ├── api/
│   │   │   └── api_v1/
│   │   │       ├── api.py            # Router aggregation
│   │   │       └── endpoints/
│   │   │           ├── auth.py       # Auth endpoints
│   │   │           ├── members.py    # Member CRUD
│   │   │           ├── membership_plans.py
│   │   │           └── agents.py     # AI agent endpoints
│   │   ├── core/
│   │   │   ├── config.py             # Settings management
│   │   │   ├── security.py           # JWT & password hashing
│   │   │   ├── dependencies.py       # FastAPI dependencies
│   │   │   └── ai/                   # AI infrastructure
│   │   │       ├── config.py         # AI settings
│   │   │       ├── llm.py            # LLM provider wrapper
│   │   │       ├── vector_store.py   # ChromaDB client
│   │   │       └── monitoring.py     # Agent monitoring
│   │   ├── db/
│   │   │   ├── base.py               # SQLAlchemy base & imports
│   │   │   └── session.py            # Async session factory
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── user.py               # User with roles
│   │   │   ├── member.py             # Member profiles
│   │   │   ├── membership_plan.py    # Subscription plans
│   │   │   ├── check_in.py           # Check-in tracking
│   │   │   └── equipment.py          # Equipment tracking
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── user.py               # User DTOs
│   │   │   └── member.py             # Member DTOs
│   │   ├── services/                 # Business Logic
│   │   │   ├── auth_service.py       # Auth operations
│   │   │   ├── member_service.py     # Member operations
│   │   │   └── membership_plan_service.py
│   │   └── agents/                   # AI Agents
│   │       ├── base/
│   │       │   ├── agent.py          # Base agent class
│   │       │   └── state.py          # Agent state models
│   │       ├── engagement/
│   │       │   └── member_engagement_agent.py
│   │       ├── operations/
│   │       │   └── operations_agent.py
│   │       └── financial/
│   │           └── financial_agent.py
│   ├── alembic/
│   │   ├── versions/
│   │   │   ├── 001_initial_user_table.py
│   │   │   ├── 002_member_and_membership_tables.py
│   │   │   └── 003_equipment_table.py
│   │   ├── env.py                    # Alembic environment
│   │   └── script.py.mako            # Migration template
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile
│
├── docs/                              # Documentation
│   ├── ai-first-gym-management-plan.md    # Full roadmap
│   └── landing-page-content.md            # Marketing content
│
├── docker-compose.yml                # Service orchestration
├── Makefile                          # Development commands
└── README.md                         # This file
```

---

## 🔧 Code Architecture Explained

### Frontend Architecture

#### 1. **Authentication Flow**
```typescript
// lib/store/auth.ts - Zustand store manages auth state
useAuthStore = create((set) => ({
  user: null,
  login: async (email, password) => {
    // Call API, store token, update state
  },
  logout: () => {
    // Clear token, reset state
  }
}))

// lib/api/client.ts - Automatic token injection
class ApiClient {
  setToken(token) {
    localStorage.setItem('access_token', token)
  }

  request(endpoint, options) {
    // Automatically adds Authorization header
  }
}
```

#### 2. **Dashboard Components**
```typescript
// app/dashboard/page.tsx
// - Checks auth on mount
// - Fetches stats from /api/v1/members/dashboard/stats
// - Displays 4 metric cards (total members, active, check-ins, occupancy)
// - Quick action buttons and AI insights section
```

#### 3. **Protected Routes**
```typescript
// Pattern used in dashboard:
useEffect(() => {
  checkAuth() // Validates token
  if (!user) router.push('/auth/login')
}, [user])
```

### Backend Architecture

#### 1. **Database Models** (SQLAlchemy)

```python
# app/models/user.py
class User(Base):
    # 4-tier role system: super_admin, admin, staff, member
    # Includes: email, password, full_name, role, is_active, etc.

# app/models/member.py
class Member(Base):
    # Links to User via user_id foreign key
    # Includes: membership_plan_id, status, dates, personal info
    # QR code for check-ins, fitness goals, medical conditions

# app/models/membership_plan.py
class MembershipPlan(Base):
    # Flexible pricing: price, duration_days
    # Features: max_classes_per_month, has_personal_trainer

# app/models/check_in.py
class CheckIn(Base):
    # Tracks member visits: check_in_time, check_out_time
    # Links to Member, method (qr_code, manual, biometric)

# app/models/equipment.py
class Equipment(Base):
    # Equipment tracking: name, category, status
    # Usage metrics: total_usage_count, total_usage_hours
    # Maintenance: last_maintenance_date, next_maintenance_due
    # IoT ready: iot_device_id, iot_last_sync
```

#### 2. **Service Layer Pattern**

```python
# app/services/member_service.py
class MemberService:
    @staticmethod
    async def create_member(db, member_data):
        # 1. Validate user exists
        # 2. Check for duplicate member profile
        # 3. Generate QR code (UUID)
        # 4. Calculate membership dates from plan
        # 5. Create and return member

    @staticmethod
    async def get_dashboard_stats(db):
        # Aggregates: total_members, active_members,
        # today_check_ins, active_check_ins (not checked out)
```

#### 3. **JWT Authentication**

```python
# app/core/security.py
def create_access_token(data):
    # Creates JWT with 30-min expiry (configurable)
    # Adds {"type": "access"} to payload

def create_refresh_token(data):
    # Creates JWT with 7-day expiry
    # Adds {"type": "refresh"} to payload

# app/core/dependencies.py
async def get_current_user(credentials, db):
    # 1. Extract token from Authorization header
    # 2. Decode and validate JWT
    # 3. Fetch user from database
    # 4. Check is_active status
    # 5. Return user or raise 401

def require_role(required_role):
    # Decorator for role-based access
    # Hierarchy: super_admin > admin > staff > member
```

#### 4. **API Endpoint Structure**

```python
# app/api/api_v1/endpoints/members.py
@router.post("/")  # Create member
async def create_member(
    member_data: MemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF))
):
    # Only staff+ can create members
    return await MemberService.create_member(db, member_data)

@router.get("/{member_id}")  # Get member
async def get_member(
    member_id: int,
    current_user: User = Depends(get_current_user)
):
    # Members can only view their own profile
    # Staff+ can view all profiles
```

### AI Agent Architecture

#### 1. **Base Agent Pattern**

```python
# app/agents/base/agent.py
class BaseAgent(ABC):
    def __init__(self, agent_type, db):
        self.state = AgentState(agent_type=agent_type)
        self.llm = llm_provider.get_llm()  # OpenAI or Anthropic

    async def run(self, context):
        # 1. Set state to RUNNING
        # 2. Execute with timeout protection
        # 3. Return AgentResult (success/failure)
        # 4. Update state to COMPLETED/FAILED

    @abstractmethod
    async def execute(self, context):
        # Implement agent-specific logic
        pass

    @abstractmethod
    async def analyze(self, data):
        # Implement analysis logic
        pass
```

#### 2. **Member Engagement Agent**

```python
# app/agents/engagement/member_engagement_agent.py
class MemberEngagementAgent(BaseAgent):
    async def execute(self, context):
        # 1. Identify at-risk members (churn score >= 0.7)
        # 2. Generate retention strategies using LLM
        # 3. Calculate engagement metrics
        # 4. Return results

    async def predict_churn_risk(self, member):
        # Heuristic-based scoring (0.0 to 1.0):
        # - Days since last check-in (40% weight)
        # - Total check-in count (30% weight)
        # - Days until membership expiry (30% weight)
        # TODO: Replace with ML model

    async def generate_retention_strategies(self, at_risk_members):
        # Uses LLM to generate personalized messages:
        # - Analyzes member profile
        # - Creates custom outreach message
        # - Suggests specific incentive
        # - Recommends follow-up action
```

#### 3. **Operations Agent**

```python
# app/agents/operations/operations_agent.py
class OperationsAgent(BaseAgent):
    async def predict_maintenance_needs(self):
        # For each equipment:
        # - Check usage count vs threshold
        # - Check days since last maintenance
        # - Calculate priority score
        # - Estimate days until failure
        # TODO: Use IoT sensor data
        # TODO: Implement ML predictive model

    async def analyze_facility_capacity(self):
        # - Daily check-in trends (last 7 days)
        # - Peak hours by hour of day
        # - Current occupancy (active check-ins)
        # - Capacity utilization percentage
        # TODO: Add predictive capacity forecasting
```

#### 4. **Financial Agent**

```python
# app/agents/financial/financial_agent.py
class FinancialAgent(BaseAgent):
    async def forecast_revenue(self):
        # 1. Calculate current MRR from active memberships
        # 2. Apply growth rate (5% placeholder)
        # 3. Project 30/60/90 day revenue
        # TODO: Implement ML forecasting model
        # TODO: Add seasonality factors

    async def analyze_pricing_optimization(self):
        # Analyzes each membership plan:
        # - Current price vs market
        # - Demand elasticity
        # - Recommended price adjustments
        # TODO: Integrate competitor pricing data
        # TODO: A/B testing framework
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites

```bash
# Required
- Docker Desktop (with Docker Compose)
- Git

# Optional (for local development)
- Node.js 20+
- Python 3.11+
```

### 2. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd gym-ai

# Set up environment variables
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit backend/.env - IMPORTANT: Add your API keys!
# Required for AI agents:
# - OPENAI_API_KEY or ANTHROPIC_API_KEY
# - Set LLM_PROVIDER to "openai" or "anthropic"
```

### 3. Start All Services

```bash
# Start everything with Docker Compose
docker-compose up -d

# Services started:
# - PostgreSQL (5432)
# - Redis (6379)
# - ChromaDB (8001)
# - Backend API (8000)
# - Frontend (3000)
# - Celery Worker
# - Celery Beat

# Check status
docker-compose ps
```

### 4. Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Migrations applied:
# - 001: Users table
# - 002: Members, MembershipPlans, CheckIns tables
# - 003: Equipment table
```

### 5. Access the Application

```bash
# Frontend
http://localhost:3000

# Backend API Docs (Swagger)
http://localhost:8000/api/v1/docs

# Backend API Docs (ReDoc)
http://localhost:8000/api/v1/redoc

# ChromaDB (vector database)
http://localhost:8001
```

### 6. Create Your First User

```bash
# Via API (using curl)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@gym.com",
    "password": "SecurePass123!",
    "full_name": "Admin User",
    "role": "admin"
  }'

# Via Frontend
# Navigate to http://localhost:3000/auth/register
# Fill in the registration form
```

### 7. Test AI Agents

```bash
# Login first to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gym.com","password":"SecurePass123!"}' \
  | jq -r '.access_token'

# Use the token for agent endpoints
TOKEN="your-token-here"

# Get at-risk members
curl http://localhost:8000/api/v1/agents/engagement/at-risk-members \
  -H "Authorization: Bearer $TOKEN"

# Get maintenance predictions
curl http://localhost:8000/api/v1/agents/operations/maintenance-predictions \
  -H "Authorization: Bearer $TOKEN"

# Get revenue forecast
curl http://localhost:8000/api/v1/agents/financial/revenue-forecast \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📚 API Endpoints Reference

### Authentication Endpoints

```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login and get tokens
GET    /api/v1/auth/me                # Get current user info
POST   /api/v1/auth/refresh           # Refresh access token
```

### Member Management

```
POST   /api/v1/members/               # Create member (Staff+)
GET    /api/v1/members/               # List all members (Staff+)
GET    /api/v1/members/{id}           # Get member by ID
GET    /api/v1/members/user/{user_id} # Get member by user ID
PUT    /api/v1/members/{id}           # Update member
POST   /api/v1/members/check-in       # Check in member (Staff+)
PUT    /api/v1/members/check-out/{id} # Check out member (Staff+)
GET    /api/v1/members/dashboard/stats # Dashboard statistics (Staff+)
```

### Membership Plans

```
POST   /api/v1/membership-plans/      # Create plan (Admin+)
GET    /api/v1/membership-plans/      # List plans
GET    /api/v1/membership-plans/{id}  # Get plan by ID
PUT    /api/v1/membership-plans/{id}  # Update plan (Admin+)
DELETE /api/v1/membership-plans/{id}  # Delete plan (Admin+)
```

### AI Agent Endpoints

```
# Member Engagement Agent (Staff+)
POST   /api/v1/agents/engagement/execute
POST   /api/v1/agents/engagement/analyze
GET    /api/v1/agents/engagement/at-risk-members

# Operations Agent (Staff+)
POST   /api/v1/agents/operations/execute
POST   /api/v1/agents/operations/analyze
GET    /api/v1/agents/operations/maintenance-predictions
GET    /api/v1/agents/operations/capacity-analysis

# Financial Agent (Admin+)
POST   /api/v1/agents/financial/execute
POST   /api/v1/agents/financial/analyze
GET    /api/v1/agents/financial/revenue-forecast
GET    /api/v1/agents/financial/expiring-memberships
GET    /api/v1/agents/financial/pricing-recommendations

# General
GET    /api/v1/agents/status           # Get all agents status
```

---

## 🔨 Development Commands

### Using Makefile

```bash
make help          # Show all available commands
make dev           # Start development environment
make build         # Build Docker images
make up            # Start services (detached)
make down          # Stop all services
make logs          # Show logs from all services
make clean         # Remove containers, volumes, artifacts
make test          # Run all tests
make migrate       # Run database migrations
make db-shell      # Open PostgreSQL shell
make redis-cli     # Open Redis CLI
```

### Manual Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute commands in containers
docker-compose exec backend python
docker-compose exec backend alembic revision --autogenerate -m "message"

# Restart specific service
docker-compose restart backend

# Rebuild specific service
docker-compose up -d --build backend
```

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_auth.py

# Run with coverage
docker-compose exec backend pytest --cov=app tests/
```

### Frontend Tests

```bash
# TODO: Add frontend tests
cd frontend
npm run test
```

---

## 🔐 Security Implementation

### JWT Authentication

- **Access Token**: 30-minute expiry, for API requests
- **Refresh Token**: 7-day expiry, for getting new access tokens
- **Token Storage**: localStorage on client, verified on each request
- **Password Hashing**: bcrypt via passlib

### Role-Based Access Control (RBAC)

**Role Hierarchy**: Super Admin > Admin > Staff > Member

```python
# Permissions by role:
MEMBER:      # Can view/edit own profile only
STAFF:       # + manage members, check-ins, view all data
ADMIN:       # + manage plans, financial data, pricing
SUPER_ADMIN: # + full system access, user management
```

### API Security

- **CORS**: Configured origins in environment variables
- **Rate Limiting**: TODO - Add rate limiting middleware
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection**: Protected by SQLAlchemy ORM
- **XSS Protection**: React escapes output by default

---

## 📋 TODO Items & Roadmap

### 🔴 Critical Priority - AI/ML Production Readiness

#### Replace Heuristic Models with Machine Learning

**1. Churn Prediction ML Model** 🎯
- **Location**: `backend/app/agents/engagement/member_engagement_agent.py:146` (predict_churn_risk method)
- **Current State**: Heuristic scoring based on check-in frequency and membership status
- **Required**: Production-grade ML model trained on historical member data
- **Suggested Features**:
  - Check-in frequency and patterns
  - Class participation rates
  - Social engagement metrics (workout buddies, group classes)
  - Goal achievement progress
  - Payment history and delays
  - Seasonal attendance patterns
  - Demographics and member profile data
- **Suggested Models**: Random Forest, Gradient Boosting (XGBoost/LightGBM), or Neural Network
- **Success Metric**: Predict churn 2-3 weeks in advance with 75%+ accuracy

**2. Equipment Maintenance Prediction Model** 🔧
- **Location**: `backend/app/agents/operations/operations_agent.py:129` (_predict_equipment_maintenance method)
- **Current State**: Simple threshold-based logic (usage count > 1000 or 90 days since maintenance)
- **Required**: Predictive maintenance model using equipment usage patterns and sensor data
- **Suggested Features**:
  - Total usage count and hours
  - Days since last maintenance
  - Equipment age and manufacturer
  - Historical failure patterns
  - **IoT sensor data** (vibration, temperature, noise - when integrated)
  - Usage intensity patterns
- **Suggested Models**: Time series forecasting (LSTM), Survival Analysis, or Anomaly Detection
- **Success Metric**: Predict maintenance needs 1-2 weeks before failure with 80%+ accuracy

**3. Revenue Forecasting Model** 💰
- **Location**: `backend/app/agents/financial/financial_agent.py:206` (forecast_revenue method)
- **Current State**: Linear growth assumption (5% monthly growth rate)
- **Required**: Time series forecasting with seasonality and market factors
- **Suggested Features**:
  - Historical revenue (MRR)
  - Member growth and churn rates
  - Seasonal patterns (New Year's resolutions, summer slowdown)
  - Market trends and economic indicators
  - Marketing campaign effectiveness
  - Local competition changes
- **Suggested Models**: ARIMA, Prophet (Facebook), LSTM, or ensemble methods
- **Success Metric**: 30-day forecast within 10% of actual revenue

### 🟠 High Priority - Integrations & Infrastructure

#### Third-Party Integrations

**4. Stripe Payment Processing** 💳
- **Location**: Stripe package installed (`requirements.txt:36`), implementation needed
- **Files to Create**: `backend/app/models/payment.py`, `backend/app/services/payment_service.py`
- **Required Features**:
  - Create Stripe customer on member registration
  - Subscription creation and management
  - Webhook handlers for payment events (payment_succeeded, payment_failed, subscription_canceled)
  - Invoice generation and email delivery
  - Failed payment retry logic with intelligent timing
  - Payment history tracking
- **Related TODOs**:
  - `backend/app/agents/financial/financial_agent.py:108` - Check payment history for renewal offers
  - `backend/app/agents/financial/financial_agent.py:333` - Implement smart payment retry logic

**5. IoT Sensor Integration** 📡
- **Location**: `backend/app/models/equipment.py:62` - Fields ready (iot_device_id, iot_last_sync)
- **Files to Create**: `backend/app/core/integrations/iot.py`, `backend/app/services/iot_service.py`
- **Required Features**:
  - Research and select IoT platform (AWS IoT Core, Azure IoT Hub, or similar)
  - Device registration and authentication system
  - Real-time data ingestion pipeline
  - Sensor data processing (usage tracking, anomaly detection)
  - Automatic equipment usage metric updates
  - Alert system for equipment issues
- **Related TODOs**:
  - `backend/app/agents/operations/operations_agent.py:175` - Use IoT data in maintenance predictions
  - `backend/app/agents/operations/operations_agent.py:287` - Get actual facility capacity from sensors

**6. Terra API Integration (Wearables & Fitness Trackers)** ⌚
- **Location**: Need to create `backend/app/core/integrations/terra.py`
- **Current State**: Configured in environment variables, not implemented
- **Required Features**:
  - Terra API client implementation
  - OAuth flow for member device connection
  - Webhook handler for real-time wearable data
  - Data mapping (heart rate, steps, calories, sleep, workouts)
  - Member health metrics dashboard
  - Integration with Member Engagement Agent
- **Use Cases**:
  - Track workout intensity and recovery
  - Personalized workout recommendations
  - Overtraining detection and alerts
  - Goal progress tracking

**7. Communication Integrations** 📧📱
- **Location**: Twilio and SendGrid packages installed (`requirements.txt:37-38`)
- **Files to Create**: `backend/app/core/integrations/twilio.py`, `backend/app/core/integrations/sendgrid.py`
- **Required Features**:
  - **SendGrid**: Transactional emails (welcome, receipts, password reset, retention campaigns)
  - **Twilio**: SMS notifications (check-in confirmations, payment reminders, urgent alerts)
  - Email template system with dynamic content
  - SMS template system with personalization
  - Delivery tracking and analytics
  - Unsubscribe management

#### AI Infrastructure & Monitoring

**8. Complete LangSmith Integration** 📊
- **Location**: `backend/app/core/ai/monitoring.py` (multiple TODOs at lines 17, 40, 67, 90)
- **Current State**: Framework in place with TODO markers
- **Required Implementation**:
  - Initialize LangSmith client with API key (line 17)
  - Send agent execution start/end traces (line 40)
  - Log LLM API calls with prompts, completions, and token counts (line 67)
  - Track agent errors and failures (line 90)
  - Create custom LangSmith dashboards for agent performance
  - Set up alerts for agent failures or performance degradation
- **Success Metric**: Full visibility into all agent executions with cost tracking

**9. Production ChromaDB Configuration** 🗄️
- **Location**: `backend/app/core/ai/vector_store.py:13`
- **Current State**: In-memory ephemeral client (data lost on restart)
- **Required Changes**:
  - Switch from ephemeral to HTTP client (line 13)
  - Configure persistent storage volume
  - Add authentication for production security
  - Implement backup and restore strategy
  - Create collections for different agent knowledge bases
  - Add monitoring for vector store health
- **Critical**: Currently losing all vector data on container restart

**10. Structured Logging Infrastructure** 📝
- **Location**: `backend/app/core/ai/monitoring.py:97` (_log_locally method)
- **Current State**: Only prints to console
- **Required Implementation**:
  - Python logging module with proper configuration
  - Log rotation (daily or size-based)
  - JSON-structured logs for easy parsing
  - Different log levels by environment (DEBUG in dev, INFO in prod)
  - Centralized logging to file/database
  - Integration with log aggregation tools (ELK stack, CloudWatch, etc.)

### 🟡 Medium Priority - Feature Enhancements

#### Agent & Analytics Enhancements

**11. Advanced Engagement Analytics** 🎯
- **Locations**:
  - `backend/app/agents/engagement/member_engagement_agent.py:179` - Add sophisticated factors to churn prediction
  - Need new models for class tracking and social interactions
- **Required Features**:
  - **Class Participation Tracking**: Attendance by class type, favorite classes, instructor preferences
  - **Social Engagement Metrics**: Workout buddy pairings, group workout participation, challenges
  - **Goal Achievement System**: Goal setting, progress tracking, milestone celebrations
  - Integration into churn prediction model (increase accuracy)
- **Success Metric**: Reduce churn rate by 15-20% through better engagement insights

**12. Operations Automation** 🏢
- **Locations**:
  - `backend/app/agents/operations/operations_agent.py:263-265` - Capacity recommendations and HVAC
  - `backend/app/agents/operations/operations_agent.py:306` - AI-generated recommendations
- **Required Features**:
  - **HVAC & Climate Control**: Smart thermostat integration, occupancy-based optimization
  - **Automated Capacity Recommendations**: Staff scheduling suggestions, class size recommendations
  - **Peak Time Predictions**: ML-based forecasting for next 24-48 hours
  - **Inventory Management**: Automated supply reordering based on usage patterns
- **Success Metric**: 30% reduction in energy costs, 25% improvement in member satisfaction

**13. Financial Intelligence** 💼
- **Locations**:
  - `backend/app/agents/financial/financial_agent.py:253` - Advanced pricing analysis
  - `backend/app/agents/financial/financial_agent.py:288` - Competitor pricing data
  - `backend/app/agents/financial/financial_agent.py:313` - More financial metrics
- **Required Features**:
  - **Competitor Pricing Analysis**: Web scraping for local gym prices, market positioning
  - **Dynamic Pricing Engine**: Demand-based pricing, promotional campaign triggers
  - **Advanced Financial Metrics**: Customer Lifetime Value (CLV), Customer Acquisition Cost (CAC), payback period
  - **ROI Analysis**: Equipment purchase recommendations, class profitability analysis
- **Success Metric**: 10% increase in revenue through optimized pricing

**14. Facility Capacity Configuration** 🏋️
- **Location**: `backend/app/agents/operations/operations_agent.py:285-287`
- **Current State**: Hardcoded capacity of 100 members
- **Required Implementation**:
  - Create `backend/app/models/facility_config.py` for configurable settings
  - Database table for facility parameters (total capacity, equipment capacity by type)
  - Admin UI for capacity management
  - Time-based capacity (different limits for peak/off-peak hours)
  - Equipment-specific capacity constraints

#### Testing & Quality Assurance

**15. Comprehensive Test Suite** 🧪
- **Current State**: Testing infrastructure configured (`requirements.txt:47-51`), no tests written
- **Required Implementation**:

  **Backend Unit Tests**:
  - Create `backend/tests/test_agents/` directory
  - Test each agent's execute() and analyze() methods
  - Mock LLM responses for consistent testing
  - Test error handling and edge cases
  - Test service layer business logic
  - Database operation tests with test fixtures

  **Frontend Unit Tests**:
  - Setup Jest and React Testing Library
  - Component tests (Button, Input, StatCard, etc.)
  - Auth flow tests (login, register, protected routes)
  - API client error handling tests
  - State management tests (Zustand stores)

  **E2E Tests**:
  - Setup Playwright or Cypress
  - Complete user journey tests (registration → login → dashboard)
  - Member management workflows
  - Check-in/check-out flows
  - Agent execution validation

  **Load Tests**:
  - Setup Locust or k6
  - API endpoint performance benchmarks
  - Concurrent agent execution tests
  - Database query optimization validation

- **Success Metric**: 80% code coverage, all critical paths tested

**16. Frontend Feature Parity** 🎨
- **Location**: Frontend currently has minimal UI, backend has full API
- **Required Implementation**:
  - Member list view with search and filters
  - Member detail page with edit capabilities
  - Membership plan management UI
  - Equipment management dashboard
  - Check-in/check-out interface for staff
  - AI agent insights visualization
  - Financial dashboard with charts (revenue, MRR trends)
  - Operations dashboard (occupancy trends, maintenance schedule)
- **Nice to Have**: Framer Motion animations (configured but not used: `frontend/package.json:32`)

### 🟢 Lower Priority - Future Enhancements

#### Advanced Features

**17. Mobile Application** 📱 (Phase 6)
- React Native or Flutter implementation
- Member check-in via QR code scanning
- Workout logging and progress tracking
- Class booking and schedule
- Push notifications for reminders and alerts
- Offline-first architecture
- Biometric authentication

**18. A/B Testing Framework** 🧪
- For pricing optimization experiments
- Retention campaign effectiveness testing
- UI/UX experiments and conversion optimization
- Statistical significance calculations
- Automated experiment management

**19. Multi-language Support** 🌍
- i18n for frontend (react-i18next)
- Backend API response translation
- LLM prompt translation for non-English markets
- RTL support for Arabic/Hebrew
- Currency localization

**20. Multi-Gym / Multi-Tenant Support** 🏢
- Gym/organization model hierarchy
- Data isolation between tenants
- Cross-location reporting and analytics
- Centralized management dashboard
- Franchise/chain management features

#### DevOps & Infrastructure

**21. CI/CD Pipeline** 🚀
- GitHub Actions workflows
- Automated testing on pull requests
- Docker image building and pushing to registry
- Automated deployment to staging/production
- Database migration automation
- Semantic versioning and changelog generation

**22. Production Deployment** ☁️
- Kubernetes manifests (Deployments, Services, Ingress)
- Helm charts for easy installation
- Infrastructure as Code (Terraform or Pulumi)
- Auto-scaling configuration
- Load balancing setup
- SSL/TLS certificate management (Let's Encrypt)
- Monitoring setup (Prometheus, Grafana, Sentry)
- APM integration (New Relic, DataDog, etc.)

**23. Backup & Disaster Recovery** 💾
- Automated PostgreSQL backups (daily full, hourly incremental)
- Point-in-time recovery capabilities
- Multi-region replication for high availability
- Disaster recovery playbook and runbooks
- Regular restore testing
- Backup monitoring and alerting

**24. Advanced Security** 🔒
- Rate limiting middleware (prevent API abuse)
- API key management for third-party integrations
- Audit logging for sensitive operations
- Two-factor authentication (2FA)
- IP allowlisting for admin operations
- Penetration testing and security audits
- GDPR compliance features (data export, deletion)

### 📊 TODO Summary by Component

**Member Engagement Agent**: 5 TODOs
- ML churn prediction model
- Class participation tracking
- Social engagement metrics
- Goal achievement system
- Advanced engagement factors

**Operations Agent**: 6 TODOs
- ML maintenance prediction model
- IoT sensor integration
- HVAC integration
- Capacity recommendations
- Peak time predictions
- AI-generated recommendations

**Financial Agent**: 6 TODOs
- ML revenue forecasting model
- Payment history tracking
- Stripe integration
- Competitor pricing analysis
- Advanced financial metrics
- Smart payment retry logic

**Infrastructure**: 6 TODOs
- Production ChromaDB config
- LangSmith integration
- Structured logging
- Rate limiting
- CI/CD pipeline
- Production deployment

**Frontend**: 3 TODOs
- Feature parity with backend
- Unit tests
- E2E tests

**Third-Party Integrations**: 4 TODOs
- Stripe payments
- IoT sensors
- Terra API (wearables)
- Twilio & SendGrid

**Total Active TODOs**: 30+ items across all priorities

---

## 🐛 Known Issues & Limitations

### Current Limitations

1. **🤖 AI Agents Use Heuristics**:
   - Churn prediction uses basic scoring algorithm (not ML-based)
   - Equipment maintenance prediction uses simple thresholds
   - Revenue forecasting uses linear growth assumptions
   - **Impact**: Not production-ready for critical business decisions
   - **Fix**: See TODOs #1-3 for ML model implementation

2. **💳 No Payment Processing**:
   - Stripe package installed but not implemented
   - No payment history tracking
   - No automated billing or dunning
   - **Impact**: Manual payment management required
   - **Fix**: See TODO #4 for Stripe integration

3. **📧 No Communication Layer**:
   - Twilio/SendGrid packages installed but not integrated
   - Cannot send transactional emails or SMS
   - Retention campaigns cannot be executed automatically
   - **Impact**: Manual member communication required
   - **Fix**: See TODO #7 for communication integrations

4. **🗄️ In-Memory ChromaDB**:
   - Vector database loses all data on container restart
   - Using ephemeral client instead of persistent HTTP client
   - **Impact**: AI knowledge base is not persistent
   - **Fix**: See TODO #9 for production ChromaDB configuration

5. **🚫 No Rate Limiting**:
   - API endpoints have no rate limiting middleware
   - Vulnerable to abuse and DoS attacks
   - **Impact**: Not suitable for public-facing deployment
   - **Fix**: See TODO #24 for rate limiting implementation

6. **📊 Partial Monitoring**:
   - LangSmith framework in place but not fully implemented
   - Only console logging (no structured logging)
   - No cost tracking for LLM API calls
   - **Impact**: Limited visibility into agent performance and costs
   - **Fix**: See TODOs #8 and #10 for monitoring completion

7. **📡 No IoT Integration**:
   - Equipment has IoT fields but no actual device connectivity
   - Manual equipment usage entry required
   - No real-time sensor data
   - **Impact**: Cannot do real-time equipment monitoring
   - **Fix**: See TODO #5 for IoT sensor integration

8. **🎨 Minimal Frontend UI**:
   - Only login, register, and basic dashboard implemented
   - No member management UI
   - No equipment or financial dashboards
   - **Impact**: Limited usability for end users
   - **Fix**: See TODO #16 for frontend feature parity

9. **🧪 No Automated Tests**:
   - Testing infrastructure configured but no tests written
   - No CI/CD pipeline
   - **Impact**: Risk of regressions when making changes
   - **Fix**: See TODOs #15 and #21

10. **🌍 Single-Tenant Only**:
    - No multi-gym support
    - **Impact**: Cannot serve multiple locations
    - **Fix**: See TODO #20 for multi-tenant architecture

### Breaking Changes from Previous Commits

None currently. All commits are additive.

### Performance Considerations

- **Database**: PostgreSQL with async SQLAlchemy performs well for <10k members
- **LLM API Calls**: Agent execution can take 2-10 seconds depending on LLM provider
- **ChromaDB**: In-memory mode is fast but not scalable beyond development
- **Celery**: Background task processing not yet utilized (configured but no tasks defined)

---

## 🔄 Git Workflow

```bash
# Main development branch (merged)
# claude/implement-from-docs-01FUjHWWjJ4bM4S6humiQgz7

# Current documentation branch
git checkout claude/update-readme-features-011CCSqQkapUvDe6quHwcPTZ

# Recent commits:
# 1. afbfd80 - feat: Initial project setup with Next.js, FastAPI, and Docker
# 2. 3f6c473 - feat: Implement JWT authentication system with user management
# 3. 1df8abc - feat: Implement member management system with dashboard
# 4. 6797a64 - feat: Implement Phase 2 - AI Agent Infrastructure & Core Automation
# 5. 2716bb5 - docs: Add comprehensive README with code explanations and TODO items
# 6. 14b9831 - Merge pull request #1 from ninth-node/claude/implement-from-docs-01FUjHWWjJ4bM4S6humiQgz7
```

---

## 📞 Support & Contact

- **Documentation**: See `docs/` directory for detailed specs
- **Issues**: Report bugs via GitHub Issues (TODO: add repository link)
- **Email**: hello@aigymmanagement.com

---

## 📄 License

This project is proprietary software. All rights reserved.

---

## 🙏 Acknowledgments

Built with:
- FastAPI
- Next.js
- LangChain & LangGraph
- Shadcn UI
- ChromaDB
- PostgreSQL
- Redis

---

**Last Updated**: November 18, 2025
**Version**: Phase 2 Complete
**Branch**: `claude/update-readme-features-011CCSqQkapUvDe6quHwcPTZ`
**Status**: Development - Not Production Ready
