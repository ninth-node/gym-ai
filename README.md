# AI-First Gym Management SaaS

> The First AI-Powered Gym Management Platform That Thinks Before You Do

Transform your gym from reactive to predictive. Our AI agents work 24/7 to prevent problems, retain members, and optimize operations—so you can focus on what matters: your members' success.

## 📊 Current Implementation Status

✅ **Phase 1 Complete**: Foundation & Core Infrastructure
✅ **Phase 2 Complete**: AI Agent Infrastructure & Core Automation
🚧 **Phase 3-7**: Advanced features (see roadmap)

---

## 🚀 Key Features Implemented

- **JWT Authentication System** with role-based access control (4 tiers)
- **Member Management** with profiles, memberships, and check-ins
- **AI Agent Framework** with 3 operational agents
- **Real-time Dashboard** with live metrics
- **Equipment Tracking** with maintenance prediction
- **Revenue Forecasting** with AI-powered insights

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

## 📋 TODO Items for Team

### 🔴 High Priority

#### AI/ML Models (Replace Heuristics)

- [ ] **Churn Prediction ML Model**
  - Location: `backend/app/agents/engagement/member_engagement_agent.py:predict_churn_risk()`
  - Current: Heuristic scoring based on check-ins, attendance
  - Needed: Train ML model on historical member data
  - Features to include: class participation, social engagement, goal progress
  - Suggested models: Random Forest, Gradient Boosting, Neural Network

- [ ] **Equipment Maintenance Prediction Model**
  - Location: `backend/app/agents/operations/operations_agent.py:_predict_equipment_maintenance()`
  - Current: Simple threshold-based logic
  - Needed: Predictive model using equipment usage patterns
  - Features: usage count, hours, last maintenance, equipment age, manufacturer data
  - Suggested: Time series forecasting (LSTM) or survival analysis

- [ ] **Revenue Forecasting Model**
  - Location: `backend/app/agents/financial/financial_agent.py:forecast_revenue()`
  - Current: Linear growth assumption (5%)
  - Needed: Time series forecasting with seasonality
  - Features: historical revenue, member growth, seasonal patterns, market trends
  - Suggested: ARIMA, Prophet, or LSTM

#### Integrations

- [ ] **IoT Sensor Integration**
  - Location: `backend/app/models/equipment.py` (iot_device_id, iot_last_sync fields ready)
  - Needed: Actual IoT device connectivity
  - Tasks:
    - Research IoT platforms (AWS IoT, Azure IoT Hub, etc.)
    - Implement device registration and authentication
    - Create data ingestion pipeline
    - Real-time sensor data processing
    - Update equipment usage metrics from sensor data

- [ ] **Payment History Tracking**
  - Location: Need new model `backend/app/models/payment.py`
  - Current: No payment tracking implemented
  - Needed:
    - Payment model with Stripe integration
    - Payment history table
    - Failed payment retry logic
    - Subscription lifecycle management
  - Related: `backend/app/agents/financial/financial_agent.py:generate_payment_retry_strategy()`

- [ ] **Terra API Integration (Wearables)**
  - Location: Environment variables configured, implementation needed
  - Tasks:
    - Implement Terra API client (`backend/app/core/integrations/terra.py`)
    - Webhook handler for wearable data
    - Map Terra data to member health metrics
    - Use in Health & Wellness Agent (Phase 3)

- [ ] **Stripe Payment Processing**
  - Location: API keys configured, implementation needed
  - Tasks:
    - Create Stripe customer on member registration
    - Subscription creation and management
    - Webhook handlers for payment events
    - Invoice generation
    - Failed payment handling

#### Monitoring & Logging

- [ ] **Complete LangSmith Integration**
  - Location: `backend/app/core/ai/monitoring.py`
  - Current: Framework in place, TODO markers for implementation
  - Tasks:
    - Initialize LangSmith client properly
    - Send agent execution traces
    - Log LLM API calls with token counts
    - Track agent performance metrics
    - Set up dashboards in LangSmith

- [ ] **Local Logging Infrastructure**
  - Location: `backend/app/core/ai/monitoring.py:_log_locally()`
  - Current: Just prints to console
  - Needed: Proper logging to file/database
  - Suggested: Use Python logging module with rotation

- [ ] **Production ChromaDB Configuration**
  - Location: `backend/app/core/ai/vector_store.py`
  - Current: In-memory client
  - Needed: HTTP client for production deployment
  - Tasks:
    - Update ChromaDB client to use HTTP
    - Configure persistent storage
    - Add authentication
    - Implement backup strategy

### 🟡 Medium Priority

#### Agent Enhancements

- [ ] **Class Participation Analysis**
  - Location: `backend/app/agents/engagement/member_engagement_agent.py`
  - Add class/group fitness tracking
  - Include in churn prediction model
  - Analyze attendance patterns by class type

- [ ] **Social Engagement Metrics**
  - Location: Need new model for social interactions
  - Track workout buddy pairings
  - Measure social engagement (group workouts, challenges)
  - Include in member engagement scoring

- [ ] **Goal Achievement Tracking**
  - Location: `backend/app/models/member.py` has fitness_goals field
  - Implement goal setting and tracking system
  - Progress monitoring
  - Include in churn prediction and engagement

- [ ] **HVAC & Climate Control Integration**
  - Location: `backend/app/agents/operations/operations_agent.py`
  - Mentioned in capacity analysis
  - Integrate with smart thermostat APIs
  - Optimize based on occupancy predictions

- [ ] **Competitor Pricing Analysis**
  - Location: `backend/app/agents/financial/financial_agent.py:analyze_pricing_optimization()`
  - Web scraping for local gym prices
  - Market analysis dashboard
  - Dynamic pricing recommendations

#### Testing & Quality

- [ ] **Unit Tests for Agents**
  - Create `backend/tests/test_agents/`
  - Test each agent's execute() and analyze() methods
  - Mock LLM responses for consistent testing
  - Test error handling and edge cases

- [ ] **Frontend Unit Tests**
  - Setup Jest and React Testing Library
  - Test components: Button, Input, StatCard, etc.
  - Test auth flows
  - Test API client error handling

- [ ] **E2E Tests**
  - Setup Playwright
  - Test complete user journeys
  - Auth flow tests
  - Member management workflows

- [ ] **Load Testing**
  - Setup Artillery or Locust
  - Test API endpoint performance
  - Agent execution under load
  - Database query optimization

### 🟢 Low Priority / Future Enhancements

#### Features

- [ ] **Mobile App** (Phase 6)
  - React Native implementation
  - Offline-first architecture
  - Biometric authentication
  - Push notifications

- [ ] **A/B Testing Framework**
  - For pricing optimization
  - Retention campaign testing
  - UI/UX experiments

- [ ] **Multi-language Support**
  - i18n for frontend
  - Backend API response translation
  - LLM prompt translation for non-English markets

- [ ] **Multi-gym Support**
  - Gym/organization model
  - Multi-tenancy architecture
  - Cross-gym reporting

#### DevOps

- [ ] **CI/CD Pipeline**
  - GitHub Actions workflows
  - Automated testing
  - Docker image building
  - Deployment automation

- [ ] **Production Deployment**
  - Kubernetes manifests
  - Helm charts
  - Infrastructure as Code (Terraform)
  - Monitoring setup (Prometheus, Grafana)

- [ ] **Backup & Disaster Recovery**
  - Automated PostgreSQL backups
  - Point-in-time recovery
  - Multi-region replication
  - Disaster recovery playbook

---

## 🐛 Known Issues & Limitations

### Current Limitations

1. **AI Agents Use Heuristics**: Not production-ready without ML models
2. **No Payment Processing**: Stripe integration not implemented
3. **No Email/SMS Sending**: Twilio/SendGrid not integrated
4. **In-Memory ChromaDB**: Will lose data on container restart
5. **No Rate Limiting**: API vulnerable to abuse
6. **No Monitoring**: LangSmith partially implemented
7. **No IoT Integration**: Equipment data is manual entry only

### Breaking Changes from Previous Commits

None currently. All commits are additive.

---

## 🔄 Git Workflow

```bash
# Current branch
git checkout claude/implement-from-docs-01FUjHWWjJ4bM4S6humiQgz7

# Latest commits:
# 1. feat: Initial project setup with Next.js, FastAPI, and Docker
# 2. feat: Implement JWT authentication system with user management
# 3. feat: Implement member management system with dashboard
# 4. feat: Implement Phase 2 - AI Agent Infrastructure & Core Automation
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

**Last Updated**: November 18, 2024
**Version**: Phase 2 Complete
**Branch**: `claude/implement-from-docs-01FUjHWWjJ4bM4S6humiQgz7`
