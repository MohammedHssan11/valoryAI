# Diagram 1: Full System Architecture

### Purpose
To explain the entire ValorAI platform in a single, visual diagram, illustrating how the system separates presentation, application routing, core mathematical engines, spatial persistence layers, and the restricted LLM communication gate.

```mermaid
flowchart TD
    User[User]
    
    subgraph Presentation["1. Presentation Layer"]
        Mobile["Flutter Mobile Application"]
    end
    
    subgraph Application["2. Application Layer"]
        Backend["FastAPI Backend APIs"]
    end
    
    subgraph Agentic["3. Agentic Layer"]
        Orch["Agentic Orchestrator"]
    end
    
    subgraph Business["4. Business Intelligence Layer"]
        Tools["Business Tools 1 to 8"]
    end
    
    subgraph Valuation["5. Valuation Layer"]
        Router["Goldilocks Router"]
        CMT["CMT Engine"]
        ML["ML Engine"]
    end
    
    subgraph Trust["6. Trust Layer"]
        Explain["Explainability Engine"]
        Confidence["Confidence Calculator"]
        Evidence["Evidence Generator"]
    end
    
    subgraph Data["7. Data Layer"]
        DB_Prop["Property Database"]
        DB_Space["Spatial Intelligence Data"]
        DB_Work["Workspace and Copilot Data"]
    end
    
    subgraph Communication["8. Communication Layer"]
        LLM["LLM Narration Layer"]
        Gate{"Grounding and Admission Gate"}
    end

    User --> Mobile
    Mobile --> Backend
    Backend --> Orch
    Orch --> Tools
    Tools --> Router
    
    Router --> CMT
    Router --> ML
    
    CMT --> DB_Prop
    CMT --> DB_Space
    ML --> DB_Space
    
    CMT --> Explain
    CMT --> Confidence
    CMT --> Evidence
    ML --> Explain
    ML --> Confidence
    
    Tools --> DB_Work
    
    Explain --> LLM
    Confidence --> LLM
    Evidence --> LLM
    DB_Work --> LLM
    
    LLM --> Gate
    Gate -->|Pass: Grounded Response| Backend
    Gate -->|Fail: Deterministic Fallback| Backend
```

### Short Explanation
ValorAI is structured across eight distinct conceptual layers. The core execution is driven by the backend databases, valuation models, explainability engines, and agentic orchestration plane. The Large Language Model (LLM) is not the core reasoning system; instead, it is isolated to the communication layer, generating natural language narration for pre-calculated facts under the strict governance of a grounding admission gate.

---

# Diagram 2: Data to Intelligence Journey

### Purpose
To show the complete systems engineering evolution of ValorAI, tracing the progression from raw unstructured listings to clean, geofenced, and agent-orchestrated real estate intelligence.

```mermaid
flowchart TD
    Raw["Raw Real Estate Data\n- Ingestion and Crawling"] --> Clean["Cleaning and Validation\n- Pruning and Sanitization"]
    Clean --> DB["Database Evolution\n- Hierarchical Trees"]
    DB --> Spatial["Spatial Intelligence\n- PostGIS Geofencing"]
    Spatial --> Valuation["Valuation Engines\n- CMT and ML Routing"]
    Valuation --> Explain["Explainability\n- SHAP and Confidence Metrics"]
    Explain --> Tools["Business Tools\n- Isolated API Services"]
    Tools --> Agentic["Agentic Intelligence\n- Intent and Orchestration"]
```

### Short Explanation
The systems engineering journey follows a linear logical sequence. Raw scraped listing points are sanitized in memory, structured into recursive parent-child tree geometries in PostGIS, processed by tiered geofencing engines, enriched via mathematical explainability, modularized into business services, and exposed through a secure agentic control plane.

---

# Diagram 3: Agentic Orchestration Architecture

### Purpose
To explain the agentic control plane and the sequence of steps that transform unstructured user messages into grounded conversational actions.

```mermaid
flowchart TD
    UserQuery[User Query] --> Intent["Intent Analysis\n- Taxonomy matching"]
    Intent --> Plan["Planning\n- Construct ExecutionPlan"]
    Plan --> Tools["Tool Selection\n- Maps plan to tools"]
    Tools --> Exec["Tool Execution\n- Thread-isolated run"]
    Exec --> Ground["Grounding\n- Database validation"]
    Ground --> Composer["Response Composition\n- Normalization and Python math"]
    Composer --> Resp[Final Response]
```

### Short Explanation
The orchestrator converts conversational inputs into intent profiles, schedules tools to execute securely inside isolated database sessions, resolves pricing queries through the Goldilocks Router, executes comparison math in Python, and validates citations to deliver mathematically verified responses.

---

# Diagram 4: End-to-End System Sequence Diagram

### Purpose
To map the request and response sequence of a real real estate query across the user interface, backend services, mathematical engines, databases, and LLM providers.

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Backend
    participant Orchestrator
    participant Tools
    participant Valuation
    participant Database
    participant LLM

    User->>Frontend: Inputs conversational query
    Frontend->>Backend: API Request
    Backend->>Orchestrator: Initiates orchestration
    Orchestrator->>Orchestrator: Intent Classification and Planning
    Orchestrator->>Tools: Invokes matched tools
    Tools->>Valuation: Dynamic pricing request
    Valuation->>Database: Geofenced spatial query
    Database-->>Valuation: Returns listing data
    Valuation->>Valuation: Calculates prices and confidence
    Valuation-->>Tools: Structured price outputs
    Tools-->>Orchestrator: Tool results
    Orchestrator->>Orchestrator: Response Composer normalizes facts
    Orchestrator->>LLM: Requests narration with facts
    LLM-->>Orchestrator: Returns natural language text draft
    Note over Orchestrator: Enforces grounding check on citations
    Orchestrator-->>Backend: Grounded natural response
    Backend-->>Frontend: JSON payload
    Frontend-->>User: Renders text and visual cards
```

### Short Explanation
When a query is received, the orchestrator classifies intents and calls tools in parallel. The tools request spatial valuations from the CMT or ML models, which pull data from the PostGIS database. The outputs are composed and formatted by the LLM narration provider. The response is validated by the orchestrator and returned as natural language text accompanied by interactive cards.

---

# Diagram 5: Why ValorAI Is Not an LLM Wrapper

### Purpose
To demonstrate the fundamental architectural difference between a traditional, unchecked LLM wrapper and ValorAI's database-grounded system.

```mermaid
flowchart TD
    subgraph Traditional["Traditional Student AI Project"]
        T_User[User] --> T_LLM["Unchecked LLM"]
        T_LLM -->|Hallucinates Math and Facts| T_Answer[Answer]
    end
    
    subgraph ValorAI["ValorAI Platform"]
        V_User[User] --> V_Orch["Agentic Orchestrator\n- Intent and Plan"]
        V_Orch --> V_Tools["Business Tools\n- Isolated APIs"]
        V_Tools --> V_Engines["Valuation Engines\n- CMT and ML Models"]
        V_Engines --> V_Truth["Truth Layer\n- Spatial PostGIS Database"]
        V_Truth -->|Deterministic Facts| V_LLM["LLM Narration\n- Restricted to presentation"]
        V_LLM --> V_Resp[Grounded Response]
    end
```

### Short Explanation
A typical wrapper application delegates database logic, mathematics, and context processing directly to the language model, leading to logical and numerical hallucinations. ValorAI offloads all reasoning, spatial geofencing, mathematical modeling, and state tracking to deterministic backend engines, restricting the LLM to drafting natural language narration of these verified facts.
