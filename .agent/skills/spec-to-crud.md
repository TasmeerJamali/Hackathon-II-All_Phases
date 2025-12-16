# Spec-to-CRUD Generator Skill

## Trigger Phrases
- "Generate CRUD from spec {feature_name}"
- "Create backend for {feature_name}"
- "Implement {feature_name} feature"

## Description
Generates complete backend CRUD implementation from a feature specification.

## Input
- Feature specification file path (e.g., specs/features/task-crud.md)

## Steps

### Step 1: Parse Specification
Read the spec file and extract:
- Entity name (e.g., Task)
- Fields with types and constraints
- Acceptance criteria
- API endpoints

### Step 2: Generate Model
Create SQLModel class in backend/src/models.py:
```python
class {Entity}(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # ... fields from spec
```

### Step 3: Generate CRUD Functions
Create functions in backend/src/crud.py:
```python
async def create_{entity}(session, data, user_id):
    ...
    
async def get_{entity}(session, id, user_id):
    ...
    
async def update_{entity}(session, id, data, user_id):
    ...
    
async def delete_{entity}(session, id, user_id):
    ...
    
async def list_{entities}(session, user_id, filters):
    ...
```

### Step 4: Generate API Routes
Create FastAPI router in backend/src/routes/{entity}.py:
```python
router = APIRouter(prefix="/api/{user_id}/{entities}")

@router.get("/")
async def list_{entities}(...):
    ...

@router.post("/", status_code=201)
async def create_{entity}(...):
    ...

@router.get("/{id}")
async def get_{entity}(...):
    ...

@router.put("/{id}")
async def update_{entity}(...):
    ...

@router.delete("/{id}", status_code=204)
async def delete_{entity}(...):
    ...
```

### Step 5: Generate Pydantic Schemas
Create request/response models:
```python
class {Entity}Create(BaseModel):
    # Required fields for creation
    
class {Entity}Update(BaseModel):
    # Optional fields for update
    
class {Entity}Response(BaseModel):
    # All fields for response
```

## Output
- Updated models.py
- Updated crud.py
- New routes/{entity}.py
- Updated main.py (router import)

## Example
```
User: Generate CRUD from spec task-crud
Agent: [Executes skill, generates all files]
```
