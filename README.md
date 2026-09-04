# RAG-and-Agentic-AI-Capstone-Project
Combine Agents into a Multi-Agent System
# Multimodal Multi-Agent Restaurant Recommendation System

A portfolio-ready **Generative AI application** that combines structured data generation, multimodal retrieval, multi-agent orchestration, and the **Model Context Protocol (MCP)** to build an intelligent restaurant recommendation system.

The project demonstrates an end-to-end AI workflow — from unstructured restaurant data and food images to retrieval, agent collaboration, tool execution, and an interactive chatbot.

---

## Project Overview

The system transforms heterogeneous restaurant information such as:

* Restaurant descriptions
* Customer reviews
* Food images
* Metadata

into a structured and searchable knowledge base.

It then combines **text and image embeddings**, **multimodal retrieval**, and **specialized AI agents** to generate personalized restaurant recommendations.

The final system is exposed through an interactive **Gradio chatbot** and uses **MCP** to connect agents with retrieval systems and external tools.

---

## Architecture

```text
                    ┌─────────────────────────┐
                    │   Restaurant Data       │
                    │                         │
                    │ • Descriptions          │
                    │ • Reviews               │
                    │ • Food Images           │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────┐
              │   Structured Generative AI       │
              │                                  │
              │ LLM + Multimodal LLM             │
              │ Prompt Engineering                │
              │ JSON Validation                  │
              └────────────────┬─────────────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │ Structured Restaurant Knowledge  │
              │ Base                             │
              └────────────────┬─────────────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
          Text Embeddings             Image Embeddings
                  │                         │
                  └────────────┬────────────┘
                               ▼
              ┌──────────────────────────────────┐
              │   Multimodal Vector Database     │
              │                                  │
              │ Similarity Search                │
              │ Metadata Filtering               │
              │ Late-Fusion Ranking              │
              └────────────────┬─────────────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │      Multi-Agent System          │
              │                                  │
              │ • Restaurant Research Agent      │
              │ • Retrieval Agent                │
              │ • Recommendation Agent           │
              │ • Preference/Ranking Agent       │
              └────────────────┬─────────────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │       MCP Integration            │
              │                                  │
              │ MCP Host                         │
              │ MCP Client                       │
              │ MCP Servers                      │
              │ Tools & Resources                │
              └────────────────┬─────────────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │       Gradio Chatbot             │
              │                                  │
              │ Personalized Recommendations     │
              └──────────────────────────────────┘
```

---

# 1. Structured Generative AI Application

The first stage converts unstructured restaurant information into a consistent structured representation.

### Input

The application processes:

* Restaurant descriptions
* Customer reviews
* Food images
* Restaurant metadata

### Generative AI Pipeline

Large Language Models (LLMs) and multimodal LLMs are used to extract structured information.

Example:

```json
{
  "restaurant_name": "La Bella",
  "cuisine": ["Italian"],
  "price_level": 2,
  "rating": 4.5,
  "dishes": [
    {
      "name": "Margherita Pizza",
      "category": "pizza"
    }
  ],
  "ambiance": ["casual", "family-friendly"],
  "dietary_options": ["vegetarian"],
  "customer_sentiment": "positive"
}
```

### Key Components

* Prompt engineering
* LLM-based information extraction
* Multimodal understanding
* Structured JSON generation
* Output validation
* Error handling
* Knowledge-base updates

A command-line interface (CLI) is used to manage the structured restaurant knowledge base safely.

---

# 2. Multimodal Retrieval System

The second stage enables the system to search restaurants using both **textual and visual information**.

## Text Embeddings

Restaurant descriptions, reviews, and structured information are converted into vector representations.

```text
Restaurant Text
      │
      ▼
Embedding Model
      │
      ▼
Text Vector
      │
      ▼
Vector Database
```

## Image Embeddings

Food images are also converted into vector representations.

```text
Food Image
    │
    ▼
Vision / Multimodal Embedding Model
    │
    ▼
Image Vector
    │
    ▼
Vector Database
```

## Similarity Search

The system retrieves restaurants based on semantic similarity.

For example:

```text
"Find a cozy Italian restaurant with vegetarian pizza"
```

can retrieve restaurants whose descriptions, reviews, and dishes are semantically related to the query.

---

## Metadata Filtering

Vector similarity is combined with structured metadata filtering.

Example:

```text
Cuisine = Italian
Price Level <= 2
Rating >= 4.0
Vegetarian = True
```

This allows the system to combine:

**Semantic Search + Structured Filtering**

---

## Weighted Late Fusion

Text and image retrieval results are combined using a weighted late-fusion strategy.

A simplified scoring function is:

```text
Final Score =
    α × Text Similarity
  + β × Image Similarity
```

where:

* `α` = text retrieval weight
* `β` = image retrieval weight

The weights can be adjusted depending on the query.

For example:

```text
Text-focused query:

α = 0.7
β = 0.3
```

Visual-focused query:

```text
α = 0.3
β = 0.7
```

This improves cross-modal retrieval by allowing evidence from multiple modalities to contribute to the final ranking.

---

# 3. Multi-Agent Recommendation System

The retrieval system is combined with multiple specialized AI agents.

Instead of using one agent for every task, responsibilities are divided between specialized agents.

## Example Agent Roles

### Restaurant Research Agent

**Goal:** Understand restaurant information and identify relevant candidates.

### Retrieval Agent

**Goal:** Search the multimodal vector database and retrieve relevant restaurants.

### Recommendation Agent

**Goal:** Generate personalized recommendations based on retrieved information.

### Ranking / Preference Agent

**Goal:** Compare candidates and rank them according to user preferences.

---

## Agent Collaboration

```text
User Query
    │
    ▼
Recommendation Agent
    │
    ▼
Retrieval Agent
    │
    ├── Text Search
    │
    ├── Image Search
    │
    └── Metadata Filtering
    │
    ▼
Candidate Restaurants
    │
    ▼
Ranking Agent
    │
    ▼
Personalized Recommendation
```

The agents collaborate to transform a natural-language request into a personalized recommendation.

---

# 4. Interactive Gradio Chatbot

The recommendation system is exposed through an interactive **Gradio** interface.

Example interaction:

```text
User:
I want a romantic Italian restaurant with vegetarian
options and a moderate price.

Assistant:
Here are the best matching restaurants based on your
preferences...

1. Restaurant A
   Italian • Romantic • Vegetarian
   Rating: 4.6

2. Restaurant B
   Italian • Cozy • Vegetarian
   Rating: 4.4
```

The chatbot provides a simple interface for interacting with the underlying multi-agent and retrieval architecture.

---

# 5. Model Context Protocol (MCP) Integration

The project integrates **Model Context Protocol (MCP)** to connect the AI system with tools and external capabilities in a structured way.

## MCP Architecture

```text
                   ┌───────────────┐
                   │   LLM Host    │
                   └───────┬───────┘
                           │
                           ▼
                   ┌───────────────┐
                   │  MCP Client   │
                   └───────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        MCP Server     MCP Server    MCP Server
              │            │            │
              ▼            ▼            ▼
          Retrieval      Database      Tools
```

MCP provides a standardized mechanism for agents and LLMs to interact with tools and resources.

### MCP Components

* MCP Host
* MCP Client
* MCP Servers
* Tools
* Resources
* Structured tool inputs and outputs

---

## Tool Execution

The system validates end-to-end tool execution:

```text
User Request
     │
     ▼
LLM / Agent
     │
     ▼
MCP Client
     │
     ▼
MCP Server
     │
     ▼
Tool Execution
     │
     ▼
Structured Result
     │
     ▼
Agent
     │
     ▼
Final Response
```

Security and structured communication are considered when exposing tools to AI agents.

---

# 6. Guided Labs and Final Project

The project is developed incrementally through guided laboratory tasks.

Each lab contributes to the final system, covering different parts of the AI architecture:

```text
Lab 1
  │
  ▼
Structured Data Generation
  │
  ▼
Lab 2
  │
  ▼
Multimodal Retrieval
  │
  ▼
Lab 3
  │
  ▼
Multi-Agent System
  │
  ▼
Lab 4
  │
  ▼
MCP Integration
  │
  ▼
Final Project
```

The final result is a portfolio-ready application demonstrating the ability to design and coordinate complex AI systems from **data ingestion to deployment**.

---

# Technologies

| Area              | Technologies                     |
| ----------------- | -------------------------------- |
| Programming       | Python                           |
| Generative AI     | LLMs, Multimodal LLMs            |
| Prompting         | Prompt Engineering               |
| Structured Output | JSON, Schema Validation          |
| Retrieval         | Vector Search, Similarity Search |
| Embeddings        | Text & Image Embeddings          |
| Vector Database   | Multimodal Vector Store          |
| Ranking           | Weighted Late Fusion             |
| Agents            | Multi-Agent Architecture         |
| Interface         | Gradio                           |
| Protocol          | Model Context Protocol (MCP)     |
| Application       | CLI + Chatbot                    |
| Architecture      | RAG + Agents + Tools             |

---

# Key Learning Outcomes

By completing this project, the following capabilities are demonstrated:

* Build structured data pipelines using LLMs.
* Extract information from text and images.
* Design reliable prompt-based workflows.
* Validate and manage LLM-generated JSON.
* Build multimodal vector databases.
* Generate and use text and image embeddings.
* Implement semantic similarity search.
* Combine vector retrieval with metadata filtering.
* Implement weighted late-fusion ranking.
* Design specialized AI agents.
* Coordinate multi-agent workflows.
* Build interactive AI applications with Gradio.
* Integrate agents and tools using MCP.
* Validate structured tool execution.
* Design portfolio-ready Generative AI systems.

---

# End-to-End AI Stack

```text
                    GENERATIVE AI
                         │
          ┌──────────────┴──────────────┐
          │                             │
       LLMs                     Multimodal LLMs
          │                             │
          └──────────────┬──────────────┘
                         │
                  Structured Data
                         │
                         ▼
                Multimodal Retrieval
                         │
              ┌──────────┴──────────┐
              │                     │
        Text Embeddings       Image Embeddings
              │                     │
              └──────────┬──────────┘
                         │
                  Vector Database
                         │
                         ▼
                  Multi-Agent AI
                         │
                         ▼
                       MCP
                         │
                         ▼
                    AI Tools
                         │
                         ▼
                 Gradio Chatbot
```

---

# Project Goal

The goal of this project is to demonstrate how modern AI components can be combined into a single production-oriented architecture:

**LLMs + Multimodal AI + RAG + Vector Search + Multi-Agent Systems + MCP + Interactive Applications**

The project focuses not only on individual models, but on the **engineering and orchestration required to build a complete Generative AI system**.
