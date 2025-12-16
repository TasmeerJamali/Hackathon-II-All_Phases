# Architecture Diagrams

> Phase V: Complete system architecture documentation for Evolution of Todo

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          EVOLUTION OF TODO                               │
│                     Cloud-Native Event-Driven System                     │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────┐     HTTPS      ┌─────────────┐     HTTPS      ┌─────────────┐
│   Browser   │ ──────────────▶│   Vercel    │ ──────────────▶│  Azure AKS  │
│   Client    │                │  Frontend   │                │   Backend   │
└─────────────┘                └─────────────┘                └─────────────┘
                                                                     │
                                                                     ▼
                                                              ┌─────────────┐
                                                              │   Neon DB   │
                                                              │ PostgreSQL  │
                                                              └─────────────┘
```

---

## 2. Kubernetes Architecture (AKS)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        AZURE KUBERNETES SERVICE                          │
│                         todo-evolution-aks                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        default namespace                          │    │
│  │                                                                   │    │
│  │  ┌─────────────────────┐      ┌─────────────────────┐           │    │
│  │  │   backend           │      │   Dapr Sidecar      │           │    │
│  │  │   Deployment        │◀────▶│   :3500             │           │    │
│  │  │   :8000             │      │                     │           │    │
│  │  │                     │      │   • Pub/Sub         │           │    │
│  │  │   FastAPI           │      │   • State           │           │    │
│  │  │   + OpenAI          │      │   • Secrets         │           │    │
│  │  │   + SQLModel        │      │   • Service Invoke  │           │    │
│  │  └─────────────────────┘      └─────────────────────┘           │    │
│  │            │                                                      │    │
│  │            ▼                                                      │    │
│  │  ┌─────────────────────┐                                         │    │
│  │  │   backend-svc       │                                         │    │
│  │  │   LoadBalancer      │◀─── External IP: 135.235.248.0          │    │
│  │  │   Port: 80 → 8000   │                                         │    │
│  │  └─────────────────────┘                                         │    │
│  │                                                                   │    │
│  │  ┌─────────────────────┐                                         │    │
│  │  │   todo-secrets      │                                         │    │
│  │  │   Secret            │                                         │    │
│  │  │                     │                                         │    │
│  │  │   • DATABASE_URL    │                                         │    │
│  │  │   • BETTER_AUTH_SECRET                                        │    │
│  │  │   • OPENAI_API_KEY  │                                         │    │
│  │  └─────────────────────┘                                         │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        dapr-system namespace                      │    │
│  │                                                                   │    │
│  │  • dapr-operator                                                  │    │
│  │  • dapr-sidecar-injector                                          │    │
│  │  • dapr-placement                                                 │    │
│  │  • dapr-sentry (mTLS)                                             │    │
│  │                                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                          ┌─────────────────────────┐
                          │   Azure Container       │
                          │   Registry (ACR)        │
                          │   todoevolutionacr      │
                          │                         │
                          │   • backend:v1          │
                          │   • frontend:v1         │
                          └─────────────────────────┘
```

---

## 3. Event-Driven Architecture (Dapr)

```
                                    PHASE V: EVENT-DRIVEN FLOW
                                    
┌──────────────────────────────────────────────────────────────────────────┐
│                              PRODUCER (Backend)                           │
│                                                                           │
│  ┌─────────────┐    HTTP POST     ┌─────────────┐    Produce    ┌──────┐│
│  │   FastAPI   │ ────────────────▶│   Dapr      │ ─────────────▶│Kafka ││
│  │   Routes    │  /v1.0/publish   │   Sidecar   │               │Topic ││
│  │             │  /kafka-pubsub   │   :3500     │               │      ││
│  │  • tasks.py │  /task-events    │             │               │      ││
│  └─────────────┘                  └─────────────┘               └──────┘│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                         │
                                         │ task-events
                                         │ reminders
                                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                              MESSAGE BROKER                               │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                         REDPANDA (Kafka)                            │  │
│  │                                                                     │  │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │  │
│  │  │  task-events    │    │   reminders     │    │  task-updates   │ │  │
│  │  │                 │    │                 │    │                 │ │  │
│  │  │  • TaskCreated  │    │  • ReminderDue  │    │  • TaskUpdated  │ │  │
│  │  │  • TaskUpdated  │    │                 │    │                 │ │  │
│  │  │  • TaskDeleted  │    │                 │    │                 │ │  │
│  │  │  • TaskCompleted│    │                 │    │                 │ │  │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘ │  │
│  │                                                                     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
                                         │
                                         │ Subscribe
                                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                              CONSUMERS (Backend)                          │
│                                                                           │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐         │
│  │   Audit     │         │  Recurring  │         │ Notification│         │
│  │   Service   │         │    Task     │         │   Service   │         │
│  │             │         │   Service   │         │             │         │
│  │  Logs all   │         │  Creates    │         │  Sends      │         │
│  │  events     │         │  next task  │         │  reminders  │         │
│  └─────────────┘         └─────────────┘         └─────────────┘         │
│        │                       │                       │                  │
│        └───────────────────────┴───────────────────────┘                  │
│                                │                                          │
│                    POST /events/task-events                               │
│                    POST /events/reminders                                 │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Dapr Building Blocks (5/5)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DAPR BUILDING BLOCKS                              │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │ 1. PUB/SUB       │  │ 2. STATE STORE   │  │ 3. BINDINGS      │       │
│  │                  │  │                  │  │                  │       │
│  │ kafka-pubsub     │  │ statestore       │  │ reminder-cron    │       │
│  │                  │  │                  │  │                  │       │
│  │ Type:            │  │ Type:            │  │ Type:            │       │
│  │ pubsub.kafka     │  │ state.postgresql │  │ bindings.cron    │       │
│  │                  │  │                  │  │                  │       │
│  │ Topics:          │  │ Backend:         │  │ Schedule:        │       │
│  │ • task-events    │  │ Neon PostgreSQL  │  │ */5 * * * *      │       │
│  │ • reminders      │  │                  │  │ (every 5 min)    │       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐                             │
│  │ 4. SERVICE       │  │ 5. SECRETS       │                             │
│  │    INVOCATION    │  │    MANAGEMENT    │                             │
│  │                  │  │                  │                             │
│  │ /v1.0/invoke/    │  │ kubernetes-      │                             │
│  │ {app-id}/        │  │ secrets          │                             │
│  │ method/{method}  │  │                  │                             │
│  │                  │  │ Type:            │                             │
│  │ Features:        │  │ secretstores.    │                             │
│  │ • mTLS           │  │ kubernetes       │                             │
│  │ • Retry          │  │                  │                             │
│  │ • Load Balance   │  │ Secrets:         │                             │
│  │                  │  │ • DATABASE_URL   │                             │
│  └──────────────────┘  │ • OPENAI_API_KEY │                             │
│                        └──────────────────┘                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. CI/CD Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GITHUB ACTIONS WORKFLOW                           │
│                        .github/workflows/deploy.yml                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────┐     ┌──────────────────────────────────────────────────────┐
│   GitHub    │     │                    JOBS                               │
│   Push to   │────▶│                                                       │
│   main      │     │  ┌────────────┐  ┌────────────┐  ┌────────────┐      │
└─────────────┘     │  │  Backend   │  │  Frontend  │  │            │      │
                    │  │  Job       │  │  Job       │  │            │      │
                    │  │            │  │            │  │            │      │
                    │  │ • checkout │  │ • checkout │  │            │      │
                    │  │ • python   │  │ • node     │  │            │      │
                    │  │ • uv sync  │  │ • npm ci   │  │            │      │
                    │  │ • ruff     │  │ • lint     │  │            │      │
                    │  │ • pytest   │  │ • build    │  │            │      │
                    │  └─────┬──────┘  └─────┬──────┘  │            │      │
                    │        │               │         │            │      │
                    │        └───────┬───────┘         │            │      │
                    │                ▼                 │            │      │
                    │  ┌─────────────────────────────┐ │            │      │
                    │  │      Docker Job             │ │            │      │
                    │  │                             │ │            │      │
                    │  │  • login to GHCR            │ │            │      │
                    │  │  • build backend image      │ │            │      │
                    │  │  • build frontend image     │ │            │      │
                    │  │  • push to registry         │ │            │      │
                    │  └──────────────┬──────────────┘ │            │      │
                    │                 ▼                │            │      │
                    │  ┌─────────────────────────────┐ │            │      │
                    │  │      Deploy Job             │◀┼── Manual   │      │
                    │  │                             │ │   Approval │      │
                    │  │  • setup helm               │ │            │      │
                    │  │  • setup kubectl            │ │            │      │
                    │  │  • helm upgrade --install   │ │            │      │
                    │  └─────────────────────────────┘ │            │      │
                    │                                  │            │      │
                    └──────────────────────────────────┴────────────┘      │
                                                                           │
                                       ▼                                   │
                              ┌─────────────────┐                          │
                              │   Azure AKS     │                          │
                              │   Cluster       │                          │
                              └─────────────────┘                          │
```

---

## 6. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW                                      │
└─────────────────────────────────────────────────────────────────────────┘

  USER                    FRONTEND                  BACKEND                 
   │                         │                         │                    
   │  1. Create Task         │                         │                    
   │ ────────────────────▶   │                         │                    
   │                         │  2. POST /api/{id}/tasks│                    
   │                         │ ────────────────────▶   │                    
   │                         │                         │  3. Insert to DB   
   │                         │                         │ ──────────────────▶
   │                         │                         │                    
   │                         │                         │  4. Publish Event  
   │                         │                         │ ──────────────────▶
   │                         │                         │    (Dapr → Kafka)  
   │                         │  5. Return Task         │                    
   │                         │ ◀────────────────────   │                    
   │  6. Show Task           │                         │                    
   │ ◀────────────────────   │                         │                    
   │                         │                         │                    

                                          ┌─────────────────────────────┐
                                          │  EVENT CONSUMERS           │
                                          │                            │
                                          │  7. Consume TaskCreated    │
                                          │  8. Audit Log              │
                                          │  9. If Recurring → Create  │
                                          │     Next Instance          │
                                          └─────────────────────────────┘


  USER                    FRONTEND                  BACKEND                 
   │                         │                         │                    
   │  1. "Add task to buy milk"                        │                    
   │ ────────────────────▶   │                         │                    
   │                         │  2. POST /api/{id}/chat │                    
   │                         │ ────────────────────▶   │                    
   │                         │                         │  3. Load History   
   │                         │                         │ ──────────────────▶
   │                         │                         │                    
   │                         │                         │  4. Call OpenAI    
   │                         │                         │ ──────────────────▶
   │                         │                         │                    
   │                         │                         │  5. Execute Tool   
   │                         │                         │    (add_task)      
   │                         │                         │ ──────────────────▶
   │                         │                         │                    
   │                         │  6. Return Response     │                    
   │                         │ ◀────────────────────   │                    
   │  7. "Created task #5"   │                         │                    
   │ ◀────────────────────   │                         │                    
```

---

## 7. Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────┐
│            TRANSPORT SECURITY             │
│                                           │
│  • HTTPS (TLS 1.3) - Frontend            │
│  • mTLS via Dapr Sentry - Pod-to-Pod     │
│  • Encrypted DB connection (SSL)          │
└───────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────┐
│          AUTHENTICATION                   │
│                                           │
│  • Better Auth (Frontend)                 │
│  • JWT Tokens (HS256)                     │
│  • Token expiry: 7 days                   │
└───────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────┐
│          AUTHORIZATION                    │
│                                           │
│  • User ID from JWT payload              │
│  • URL user_id must match token          │
│  • All queries filter by user_id         │
└───────────────────────────────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────┐
│          SECRETS MANAGEMENT               │
│                                           │
│  • Kubernetes Secrets                     │
│  • Dapr Secrets API                       │
│  • No hardcoded credentials              │
└───────────────────────────────────────────┘
```

---

## 8. Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY STACK                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  FRONTEND                      BACKEND                                   │
│  ───────────────────          ───────────────────                        │
│  • Next.js 15                 • Python 3.13                              │
│  • TypeScript                 • FastAPI                                  │
│  • Tailwind CSS               • SQLModel                                 │
│  • Lucide Icons               • Pydantic                                 │
│  • Better Auth                • PyJWT                                    │
│                               • OpenAI SDK                               │
│                               • httpx                                    │
│                                                                          │
│  DATABASE                      INFRASTRUCTURE                            │
│  ───────────────────          ───────────────────                        │
│  • Neon PostgreSQL            • Azure AKS                                │
│  • SQLModel ORM               • Azure ACR                                │
│                               • Docker                                   │
│                               • Helm 3                                   │
│                               • Dapr                                     │
│                                                                          │
│  MESSAGING                     CI/CD                                     │
│  ───────────────────          ───────────────────                        │
│  • Redpanda (Kafka)           • GitHub Actions                           │
│  • Dapr Pub/Sub               • GHCR                                     │
│                               • Helm Upgrade                             │
│                                                                          │
│  AI/ML                         HOSTING                                   │
│  ───────────────────          ───────────────────                        │
│  • OpenAI GPT-4o-mini         • Frontend: Vercel                         │
│  • Function Calling           • Backend: Azure AKS                       │
│  • MCP Tools                  • DB: Neon Serverless                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*Evolution of Todo - Phase V Architecture Documentation*
