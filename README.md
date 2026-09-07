# RAG and Agentic AI — Capstone Project

An end-to-end food & restaurant recommendation system built lab by lab: from turning messy text and images into structured data, to a multimodal vector index with hybrid retrieval, to a multi-agent recommender exposed through a chatbot UI.

The labs run locally with **Ollama** (`llava`) for Modules 1, and open-source embedding models for Module 2. Module 3 uses the **OpenAI API**.

## Repository layout

```
M1L1_Extract Structured JSON from Restaurant Text Using LLMs.ipynb
M1L2-Process-Multimodal-Data-with-LLMs.ipynb
M1L3_Build-Command-Line-DataManagement-UI-for-Restaurant-Data.ipynb
restaurant_data_management.py        # CLI app + unit tests for M1L3
M2L1.ipynb                           # Build the multimodal vector index
M2L2_Lab.ipynb                       # Similarity retrieval + metadata filtering
M2L3_Lab.ipynb                       # Multimodal fusion & reranking
M3L1_Design_Specialized_Agents.ipynb
M3L2_Implement_Multi_Agent_Systems.ipynb
M3L3_Build_Chatbot_Interface.ipynb
data/                                # gitignored datasets (JSON + recipe images)
```

`data/` is excluded from version control (see `.gitignore`) and contains:
`California-Culinary-Map.txt`, `Recipes.json`, `Synthetic-User-Reviews.json`,
`structured_restaurant_data.json`, `augmented_food_recipe.json`,
`augmented_user_review.json`, and `synthetic_recipe_images/`.

## Module 1 — Data preparation with LLMs

### M1L1 — Structuring unstructured restaurant text
- Split a long culinary article into per-restaurant paragraphs.
- Wrap a local model with `ChatOllama` (`llava:latest`, `temperature=0`) behind an `llm_model(system_msg, prompt_txt)` interface.
- Prompt engineering for **schema-constrained extraction**: explicit JSON schema, no markdown fences, `null` for missing fields.
- Output validation with a **Pydantic** `Restaurant` model (`List[str]` fields for `signatures`, `shortcomings`, etc.).
- **Self-repair loop**: on `JSONDecodeError` / `ValidationError`, feed the bad output + error message back to the LLM (`JSON_auto_repair_prompts`) and re-parse.
- Retry/backoff wrapper (`safe_llm_call`) around flaky model calls.
- Result: `data/structured_restaurant_data.json`.

### M1L2 — Multimodal preprocessing
- Vision LLM calls with `ChatOllama` + **base64-encoded images** (`vision_llm(system_msg, prompt_txt, image_path)`).
- Caption ~110 synthetic recipe images with a food-name-conditioned prompt template, then augment `Recipes.json` → `augmented_food_recipe.json`.
- Caption review images pulled from remote URLs, using `tenacity` retry with exponential backoff for downloads, and `ast.literal_eval` to parse stringified lists.
- Result: `augmented_user_review.json`.

### M1L3 — Command-line data management UI
Implemented in <ref_file file="/home/zahra/RAG-and-Agentic-AI-Capstone-Project/restaurant_data_management.py" />:
- CRUD menu over the JSON store: browse, view record, add, edit, delete, exit.
- `new_data_entry_process(paragraph, itemId)` reuses the M1L1 extraction + JSON auto-repair pipeline so a free-text paragraph becomes a structured record.
- Write operations are gated behind a **security confirmation** prompt.
- `unittest` suite driving the UI with `unittest.mock.patch` on `builtins.input` and `sys.stdout`.

```bash
python3 restaurant_data_management.py       # runs the unit tests
# swap the last lines of the file to call manage_restaurants(FILEPATH, BACKUP_PATH) for the interactive UI
```

## Module 2 — Multimodal retrieval

Persistent store: **ChromaDB** at `~/chroma_multimodal`, two collections —
`restaurant_articles` (text) and `food_images` (images).

### M2L1 — Building the index
- Text embeddings: `sentence-transformers/all-MiniLM-L6-v2`.
- Image embeddings: **SigLIP** (`google/siglip-base-patch16-224`) via `transformers` `AutoModel`/`AutoProcessor`, batched, GPU-aware.
- Build LangChain `Document`s with metadata (`doc_id`, `cuisine`, `image_path`, …) so filters are possible later.
- Add texts/embeddings to Chroma with explicit `ids` and `metadatas`.

### M2L2 — Similarity retrieval + metadata filtering
- `retrieve_articles(query, k, where)` — text → article search.
- `retrieve_images_by_image(path, k, where)` — image → image search.
- Chroma `where` clauses for metadata filtering (e.g. cuisine), plus helpers to unwrap Chroma's list-of-lists responses and pretty-print hits.

### M2L3 — Fusion and reranking
- Text → image retrieval using SigLIP's **shared text/image embedding space** (`embed_text_siglip`).
- Convert distances to similarities, min-max normalize across modalities, then `fuse_rank(...)` combines text and image scores with tunable weights.
- Demos: unfiltered fusion, fusion with metadata filters, and weight-tuning to observe how ranking shifts.

## Module 3 — Agentic system

### M3L1 — Designing specialized agents
Six role/goal/backstory agents defined as config dicts and rendered into system prompts by `create_agent_prompt`:
1. User Profile Generator
2. RAG Retriever (queries the Module 2 vector DB)
3. Food Trend Analyst
4. Food Style Expert
5. Nutrition Expert
6. Recommendation Expert

Each agent has a matching task definition; individual agents are smoke-tested with `test_agent`.

### M3L2 — Multi-agent orchestration
- A shared `AgentState` (`TypedDict`) threaded through the workflow.
- One node function per agent (`node_generate_profile`, `node_retrieve_candidates`, `node_analyze_trends`, `node_analyze_styles`, `node_evaluate_nutrition`, `node_generate_recommendations`).
- Phased execution with **parallel fan-out** (trends / styles / nutrition run concurrently via `ThreadPoolExecutor`) before the final synthesis step.
- `run_workflow(user_input)` drives the graph; tested on a health-conscious user and an adventurous foodie, plus an `evaluate_recommendations` scoring pass.

### M3L3 — Chatbot interface
- **Gradio** `ChatInterface`, starting from an echo bot and built up incrementally.
- LLM-based **intent classification** (5 intents) and structured **preference extraction** from free-form messages.
- Hooks the extracted preferences into the multi-agent workflow and formats the results for chat display.
- Extra tabs for database management (`add_restaurant`, `add_recipe`).

## Setup

```bash
# Module 1 (local models)
ollama pull llava
pip install langchain-ollama pydantic tenacity pillow

# Module 2
pip install langchain==0.3.27 langchain-community==0.3.31 langchain-chroma==0.2.6 \
            sentence-transformers transformers torch

# Module 3
pip install openai==1.99.9 langchain langchain-openai langgraph gradio==4.29.0
export OPENAI_API_KEY=...   # required for M3L1–M3L3
```

## Skills covered

Prompt engineering for structured output · Pydantic schema validation · LLM self-repair loops · retry/backoff around model calls · vision-LLM image captioning · multimodal dataset augmentation · CLI app design with mocked-IO unit tests · sentence-transformer and SigLIP embeddings · ChromaDB vector stores and metadata filtering · cross-modal retrieval, score normalization and fusion reranking · agent role design · stateful multi-agent workflows with parallel execution · intent classification · Gradio chatbot deployment.
