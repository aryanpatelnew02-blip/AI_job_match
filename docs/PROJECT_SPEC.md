# Master Prompt: Build a Complete AI Job Matching & Search Agent from Scratch

Act as a senior AI engineer, backend architect, full-stack developer, and technical mentor. Help me design and implement a complete, functional, portfolio-quality project called **AI Job Matching & Search Agent**.

I want to build a real application that I can demonstrate to recruiters for software engineering, backend engineering, AI engineering, LLM engineering, and AI agent internship roles.

Do not merely explain the architecture or give me isolated code snippets. Guide me through the entire development process, provide complete working code for every required file, explain how the components work together, help me run the project locally, debug errors, test it, and deploy it.

Assume I am a student building this project independently. Give clear explanations without unnecessarily oversimplifying the technical concepts. Do not skip steps or assume that I have already configured something unless we have explicitly completed it.

---

# 1. PROJECT OVERVIEW

## Project name
AI Job Matching & Search Agent

## Project objective

Build an AI-powered job discovery and recommendation platform that accepts a candidate's resume or skills profile, searches a collection of job listings using semantic similarity, ranks jobs according to skill compatibility, experience requirements, and user preferences, generates explanations using an LLM, and provides a conversational agent that can search, filter, and remember user preferences across sessions.

The application should demonstrate:

- Semantic search and retrieval.
- Embeddings and vector databases.
- Hybrid retrieval using semantic and keyword search.
- Personalized recommendation and ranking algorithms.
- LLM integration and structured output generation.
- Agentic tool calling.
- Persistent user preferences and conversational context.
- REST API development.
- Relational database design.
- Automated testing and measurable evaluation.
- Docker-based development and deployment.

The objective is to build a genuine AI-powered backend application, not merely a chatbot that sends prompts to an LLM.

## Core user journey

A user should be able to:

1. Upload a resume PDF, paste resume text, or manually enter skills and projects.
2. Have the system extract and normalize their skills, projects, experience level, and interests.
3. Select preferred roles, locations, work arrangements, and employment types.
4. Search for relevant jobs using natural-language queries.
5. Receive ranked job recommendations.
6. See a match score, matching skills, missing requirements, and an explanation for each recommendation.
7. Ask follow-up questions through a conversational interface.
8. Change filters naturally, such as "Only show remote internships."
9. Have explicitly saved preferences persist across sessions.
10. Save interesting jobs and provide relevance feedback.
11. Open the original application URL for each listing.
12. Receive sensible results even if the LLM API is unavailable.

The system must not claim that a candidate will be hired or shortlisted based on a match score.

---

# 2. REQUIRED TECHNOLOGY STACK

Use the following stack unless a technical limitation justifies a change. Explain any proposed change before introducing a new dependency.

## Backend
- Python 3.12 or another currently supported, compatible Python version.
- FastAPI for REST APIs.
- Uvicorn for local development.
- Pydantic for request, response, and LLM output validation.
- SQLAlchemy 2.x for database access.
- Alembic for database migrations.
- HTTPX for testing and external HTTP requests.
- pytest for automated testing.

## Database and search
- PostgreSQL.
- pgvector extension for storing and searching embeddings.
- PostgreSQL full-text search for keyword retrieval.
- SQLAlchemy for relational data access.
- Parameterized database queries and appropriate indexes.

Use PostgreSQL and pgvector together instead of introducing a separate vector database in the initial version.

## Embeddings and semantic search
- Sentence Transformers.
- Start with `sentence-transformers/all-MiniLM-L6-v2`, subject to compatibility and suitability.
- Generate embeddings for job descriptions during ingestion.
- Generate candidate/query embeddings when needed.
- Store vectors in PostgreSQL using the correct embedding dimensions.
- Use cosine similarity or another justified distance metric consistently.

Make the embedding model configurable. Explain how model changes affect stored vectors and why embeddings from incompatible models cannot be mixed.

## LLM integration
- Use a hosted LLM API for conversational interaction, tool selection, profile extraction where appropriate, and job-match explanations.
- Keep the provider configurable through environment variables and a small provider-independent service interface.
- Select a provider/model whose API and structured-output capabilities are currently available.
- Do not hardcode API keys.
- Do not require a paid service without identifying the cost implications.
- If possible, provide a low-cost development option.
- If using a provider-specific SDK, pin a compatible dependency version and explain the configuration.

The LLM must not calculate the authoritative ranking score. The backend ranking engine must calculate it deterministically.

## Resume processing
- PyMuPDF for PDF text extraction.
- Support pasted resume text as an alternative.
- Use Pydantic schemas to validate extracted candidate data.
- Treat resume content as untrusted input.

## Frontend
- React.
- TypeScript.
- Vite.
- Tailwind CSS.
- A suitable icon library.
- Fetch or Axios for API communication.

Use a clean, responsive, modern SaaS dashboard design.

## Development and deployment
- Git and GitHub.
- Docker.
- Docker Compose for local services.
- GitHub Actions for automated testing.
- A suitable frontend hosting provider.
- A suitable Python backend hosting provider.
- Managed PostgreSQL with pgvector support for production, or another verified compatible hosting arrangement.

Check the current compatibility of the chosen versions and services when necessary. Do not invent provider features or deployment instructions.

---

# 3. SYSTEM ARCHITECTURE

Implement a modular monolith initially. Do not split the project into microservices unless a concrete requirement justifies it.

The high-level architecture should be:

Candidate
    |
    v
React + TypeScript Frontend
    |
    v
FastAPI REST API
    |
    +---- Candidate Profile Service
    |
    +---- Resume Parsing Service
    |
    +---- Job Ingestion Service
    |
    +---- Embedding Service
    |
    +---- Hybrid Retrieval Service
    |
    +---- Ranking Engine
    |
    +---- LLM Service
    |
    +---- Agent Tool Execution Service
    |
    +---- Persistent Preference/Memory Service
    |
    +---- Evaluation Service
    |
    v
PostgreSQL + pgvector
    |
    +---- Candidate Profiles
    +---- Job Listings
    +---- Embeddings
    +---- User Preferences
    +---- Conversations
    +---- Saved Jobs
    +---- Feedback
    +---- Evaluation Data

Explain the responsibilities and data flow of each module before implementing it.

There must be two distinct workflows.

## A. Job indexing workflow

1. Obtain job records from a curated CSV dataset or permitted external data source.
2. Validate and normalize the records.
3. Remove duplicates.
4. Validate required fields and application URLs.
5. Normalize skills and employment types.
6. Generate embeddings for valid job descriptions.
7. Save the job records and embeddings to PostgreSQL.
8. Record the source and ingestion timestamp.
9. Track last verification time and listing status when available.
10. Update existing records safely when the source listing changes.
11. Avoid regenerating embeddings unnecessarily.
12. Provide ingestion statistics and error reports.

## B. Candidate search workflow

1. Receive a search request or conversational message.
2. Load the candidate profile and relevant saved preferences.
3. Interpret the search intent.
4. Extract structured query constraints.
5. Apply hard filters where appropriate.
6. Perform semantic retrieval and keyword retrieval.
7. Merge and deduplicate the candidate results.
8. Rank the results using deterministic scoring.
9. Optionally rerank a small candidate set with a cross-encoder in a later phase.
10. Generate explanations for the top results using the LLM.
11. Validate the LLM output.
12. Return the ranked results and component scores.
13. Record relevant feedback for later evaluation.

Clearly distinguish hard constraints from soft preferences. For example, an explicitly excluded employment type should not be reintroduced merely because its semantic similarity is high.

---

# 4. CANDIDATE PROFILE MANAGEMENT

Support these profile inputs:

- Resume PDF.
- Pasted resume text.
- Manually entered skills and projects.
- Experience level.
- Preferred job titles.
- Preferred locations.
- Remote, hybrid, or onsite preference.
- Employment type.
- Salary preferences when available.
- Technologies of interest.
- Maximum acceptable experience requirements.

Extract structured fields such as:

- Skills.
- Projects.
- Education.
- Professional experience, if specified.
- Internship experience, if specified.
- Target roles.
- Location preferences.
- Employment preferences.

Use a Pydantic schema.

Example:

{
  "skills": [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "React"
  ],
  "projects": [
    "Semantic search engine",
    "REST API with authentication"
  ],
  "experience_level": "fresher",
  "preferred_roles": [
    "Backend Engineer Intern",
    "AI Engineer Intern"
  ],
  "preferred_locations": [
    "Bengaluru",
    "Remote"
  ],
  "employment_types": [
    "internship",
    "entry-level"
  ]
}

This is an illustrative profile, not a fixed profile for every user.

Do not infer professional experience from personal projects. Preserve uncertainty when the resume does not specify a fact. Allow the user to review and edit extracted information before saving it.

Implement reasonable upload-size restrictions, PDF validation, safe temporary-file handling, and clear error messages.

---

# 5. JOB DATA AND INGESTION

Begin with a curated CSV dataset of approximately 500–2,000 listings if a suitable legitimate dataset is available. This is a target for development, not a requirement to fabricate data.

Create a sample CSV schema containing fields such as:

- id or source_job_id.
- title.
- company.
- description.
- required_skills.
- preferred_skills.
- experience_min.
- experience_max.
- experience_level.
- location.
- remote_policy.
- employment_type.
- salary_min, if known.
- salary_max, if known.
- currency, if known.
- application_url.
- source.
- posted_at, if known.
- last_verified_at.
- status, if known.

Requirements:

1. Clearly distinguish sample records from real opportunities.
2. Do not invent real employers, live listings, salary figures, or application URLs.
3. Do not scrape sources that prohibit automated collection.
4. Prefer legitimate APIs, permitted datasets, or manually curated records.
5. Deduplicate jobs using source IDs and a justified fallback matching strategy.
6. Normalize skills and metadata consistently.
7. Support missing fields without crashing.
8. Provide a reproducible ingestion script.
9. Report how many records were inserted, updated, skipped, and rejected.
10. Track listing freshness and avoid implying that an unverified listing is currently active.

Provide a sample CSV file with a small, clearly labeled set of synthetic development records if real data is not immediately available. Do not represent those records as actual vacancies.

Later, explain how to replace the sample dataset with a legitimate job API or other permitted source.

---

# 6. EMBEDDINGS AND HYBRID RETRIEVAL

Implement semantic retrieval using Sentence Transformers and pgvector.

For every job:

1. Construct a clean text representation using the job title, description, required skills, and other relevant text.
2. Generate an embedding.
3. Save the embedding with the job record or in a related table.
4. Regenerate it only when the relevant source text changes or the embedding model changes.

For each search:

1. Build a search representation from the user's query, relevant skills, target roles, and selected context.
2. Generate the query embedding.
3. Retrieve the most similar jobs using pgvector.
4. Perform keyword retrieval using PostgreSQL full-text search.
5. Merge and deduplicate the candidate results.
6. Apply metadata filters.
7. Pass the candidate pool to the ranking engine.

Implement and compare:

- Keyword-only retrieval.
- Vector-only retrieval.
- Hybrid retrieval.

Use a sensible configurable retrieval limit, such as retrieving up to 50 candidates before ranking, while allowing the system to handle smaller datasets.

Explain vector dimensions, cosine similarity, database indexing, and how to configure pgvector correctly.

Start with exact vector search for simplicity if necessary. Add HNSW or another approximate index only when it is justified, and compare the performance/recall trade-off.

Never use a fabricated similarity value as though it were a measured score.

---

# 7. PERSONALIZED RANKING ENGINE

Build a deterministic ranking engine in a dedicated Python module.

Use an initial configurable formula:

Final Score =
    0.35 × Semantic Similarity Score
  + 0.30 × Required Skill Match Score
  + 0.20 × Experience Compatibility Score
  + 0.15 × Preference Compatibility Score

All component scores must be placed on a consistent 0–100 scale before combination.

These weights are initial design choices, not proven optimal values. Make them configurable and evaluate them experimentally.

## Semantic similarity score

Use the retrieval model's similarity measure with a consistent normalization strategy. Do not automatically interpret raw cosine similarity as a probability or a percentage chance of being hired.

If using transformed scores, document the transformation and evaluate its behavior.

## Required skill match

Calculate a transparent score based on candidate skills and job-required skills.

A simple baseline is:

Skill Match =
100 × (Number of matching required skills /
       Number of required skills)

Handle empty required-skill lists explicitly.

Normalize aliases where justified, such as related representations of the same technology, without incorrectly treating distinct technologies as identical.

Do not count every preferred skill as a mandatory requirement.

## Experience compatibility

Design a rule-based score that handles:

- Fresher candidates.
- Internship roles.
- Entry-level roles.
- Roles with no explicit experience requirements.
- Jobs with minimum and maximum experience requirements.
- Candidates whose experience is unknown.
- Jobs whose experience information is missing.

Document the rules. Do not automatically give a perfect score to unknown experience information.

## Preference compatibility

Consider:

- Target role.
- Location.
- Remote/hybrid/onsite preference.
- Employment type.
- Salary preference, if reliable data is available.

Distinguish soft preferences from hard constraints.

Return both the final score and individual component scores so that the ranking can be inspected and debugged.

Provide unit tests for edge cases and test that the final score remains in its expected range.

Later, compare the baseline with a cross-encoder reranker or alternative weights using a held-out evaluation set.

Do not claim that the ranking weights are optimal without evidence.

---

# 8. LLM-GENERATED MATCH EXPLANATIONS

Use an LLM to generate a structured explanation for each top-ranked job.

Example response:

{
  "job_id": "job_1042",
  "match_summary": "Relevant Python backend experience",
  "matching_skills": [
    "Python",
    "PostgreSQL"
  ],
  "missing_skills": [
    "Redis"
  ],
  "experience_fit": "suitable",
  "reasons": [
    "The candidate's backend project is relevant to API development.",
    "The job requires technologies represented in the candidate profile."
  ]
}

This example is illustrative only.

The LLM must receive actual candidate and job information. It must not invent requirements, skills, companies, or facts about the candidate.

Implement:

- A provider-independent LLM service interface.
- Structured output using supported provider features where available.
- Pydantic validation.
- Timeout handling.
- Rate-limit and API-error handling.
- A limited retry strategy.
- A deterministic fallback explanation if generation fails.
- Logging that avoids exposing sensitive resume content or API keys.

The backend calculates the scores. The LLM explains the scores and supporting evidence.

Validate that the returned job ID corresponds to the requested job, and that explanations do not contradict the source description.

If the model produces invalid JSON, handle the failure safely instead of crashing the application.

---

# 9. CONVERSATIONAL AGENT AND TOOL CALLING

Implement a conversational agent that can invoke explicitly defined backend tools.

The agent should not simply return generated text. It must actually execute tools and use their results.

Create tools such as:

1. search_jobs(query, filters, top_k).
2. filter_jobs(filters).
3. get_job_details(job_id).
4. get_candidate_profile(user_id).
5. update_preferences(user_id, preferences).
6. save_job(user_id, job_id).
7. record_feedback(user_id, job_id, feedback).

Define strict input schemas for every tool.

The LLM may choose a tool and construct its arguments. The backend must validate the arguments, enforce authorization, execute the function, and return the actual results to the model.

Example conversation:

User:
"Find AI and backend internships in Bengaluru or remote. Prefer Python and FastAPI, and exclude jobs requiring more than one year of experience."

Agent:
1. Interprets the intent.
2. Extracts roles, location, skills, and experience constraints.
3. Calls the search tool.
4. Retrieves actual job results.
5. Ranks the jobs.
6. Explains the recommendations.

Follow-up:

User:
"Only show remote jobs."

The system must update the relevant filter while preserving other active search constraints.

Implement clear tool execution boundaries. Never give the model unrestricted database access, arbitrary code execution, or unrestricted SQL execution.

For the first version, implement the agent using a straightforward provider-supported tool-calling loop or explicit Python orchestration. Do not add a complex agent framework unless needed.

---

# 10. PERSISTENT MEMORY AND USER PREFERENCES

Implement persistent preference storage in PostgreSQL.

Separate:

## Long-term preferences

- Preferred job titles.
- Preferred technologies.
- Preferred locations.
- Employment types.
- Work arrangements.
- Maximum experience requirements.
- Other explicitly selected search preferences.

## Conversation/session context

- Current query.
- Active filters.
- Recent result IDs.
- Recent job references.
- Relevant messages from the current conversation.

Store only useful information, avoid unnecessarily storing sensitive content, and provide a way to view, edit, and reset saved preferences.

Use explicit user IDs and conversation IDs when implementing multiple users.

Do not rely on a global in-memory Python dictionary for persistent memory.

Ensure that one user's profile, saved jobs, preferences, and conversations cannot be accessed by another user.

The application should support follow-ups such as:

- "Show only remote roles."
- "Exclude jobs requiring Java."
- "Find similar positions."
- "What are the skill gaps for the second job?"
- "Remember that I prefer backend internships."
- "Reset my search preferences."

Explain how persistent preferences differ from the LLM's temporary conversation context.

---

# 11. DATABASE DESIGN

Use SQLAlchemy 2.x models and Alembic migrations.

Create a normalized schema appropriate for the application.

Suggested tables:

## users
- id.
- email.
- password_hash, if authentication is implemented.
- created_at.

## candidate_profiles
- id.
- user_id.
- resume_text or a secure resume reference.
- skills.
- projects.
- education.
- experience_level.
- created_at.
- updated_at.

## jobs
- id.
- source_job_id.
- title.
- company.
- description.
- required_skills.
- preferred_skills.
- experience_min.
- experience_max.
- location.
- remote_policy.
- employment_type.
- salary information, if available.
- application_url.
- source.
- embedding.
- posted_at.
- last_verified_at.
- status.
- created_at.
- updated_at.

## user_preferences
- id.
- user_id.
- preferred_roles.
- preferred_skills.
- preferred_locations.
- employment_types.
- work_arrangement.
- max_experience_years.
- updated_at.

## conversations
- id.
- user_id.
- created_at.
- updated_at.

## messages
- id.
- conversation_id.
- role.
- message.
- created_at.

## saved_jobs
- id.
- user_id.
- job_id.
- created_at.

## feedback
- id.
- user_id or evaluation profile ID.
- job_id.
- relevance rating.
- optional feedback reason.
- created_at.

Adjust the schema when necessary. Explain which fields should be JSON, arrays, normalized relations, or separate tables and why.

Add:

- Foreign keys.
- Unique constraints.
- Appropriate indexes.
- Referential integrity.
- Migration scripts.
- Safe database session management.

Use PostgreSQL-compatible data types and a supported pgvector integration. Do not assume that generic JSON or array fields automatically support all desired query operations.

For the first MVP, authentication can be deferred if that keeps the implementation manageable. If multiple users are supported, implement secure authentication and authorization before production deployment.

---

# 12. REQUIRED FASTAPI ENDPOINTS

Implement versioned API routes, using `/api/v1` as the prefix.

Suggested endpoints:

POST /api/v1/profile
POST /api/v1/profile/resume
GET /api/v1/profile
PATCH /api/v1/profile

POST /api/v1/jobs/search
GET /api/v1/jobs
GET /api/v1/jobs/{job_id}
POST /api/v1/jobs/{job_id}/save
DELETE /api/v1/jobs/{job_id}/save

POST /api/v1/chat

GET /api/v1/preferences
PATCH /api/v1/preferences
DELETE /api/v1/preferences

POST /api/v1/feedback

POST /api/v1/admin/jobs/ingest
GET /api/v1/health

Adjust the endpoints if there is a better REST design. Explain any significant differences.

Requirements:

- Use Pydantic request and response schemas.
- Return appropriate HTTP status codes.
- Handle invalid input and missing resources.
- Add pagination where appropriate.
- Avoid exposing stack traces to end users.
- Keep database and business logic out of route handlers.
- Protect administrative ingestion endpoints.
- Do not expose unrestricted administrative functionality publicly.

Provide example request and response payloads for every important endpoint.

---

# 13. FRONTEND REQUIREMENTS

Build a complete, responsive React + TypeScript interface using Vite and Tailwind CSS.

Create these views:

## A. Landing page
- Project name and short description.
- Call to action to upload a resume or start searching.
- Explanation of how job matching works.

## B. Candidate profile page
- Resume upload.
- Manual profile entry.
- Editable skills and projects.
- Experience-level selection.
- Target-role selection.
- Location and employment preferences.
- Save and update actions.

## C. Job search dashboard
- Search input.
- Filters for role, location, work arrangement, employment type, and experience.
- Ranked job cards.
- Match score and component-score breakdown.
- Matching skills.
- Missing requirements.
- Short explanation.
- Company and job details.
- Application link.
- Save-job button.

## D. Job details page or panel
- Full description.
- Required and preferred skills.
- Experience requirements.
- Work arrangement.
- Match explanation.
- Application link.

## E. Conversational agent
- Chat interface.
- Conversation history.
- Clear loading states.
- Tool execution reflected in actual results.
- Suggested follow-up queries.
- Updated results when filters change.
- Clear error states.

## F. Preferences
- View saved preferences.
- Edit preferences.
- Reset preferences.
- Persist changes through the backend.

## G. Evaluation page
For a development/admin-only view, display actual evaluation results such as:

- Precision@K.
- Recall@K.
- NDCG@K.
- Structured-output validity.
- Search latency.
- Comparison between retrieval strategies.

Do not show invented metrics as though they were actual experiment results.

Design requirements:

- Professional, minimal, recruiter-friendly UI.
- Responsive desktop and mobile layouts.
- Accessible labels and keyboard navigation.
- Proper empty, loading, and error states.
- Consistent spacing and typography.
- No dead buttons.
- No fabricated live job data.
- No placeholder UI presented as finished functionality.

---

# 14. EVALUATION AND EXPERIMENTS

The project must include a reproducible evaluation pipeline.

Create a labeled evaluation dataset containing candidate profiles, job listings, search queries, and human-assigned relevance labels.

For example:

- 2 = highly relevant.
- 1 = partially relevant.
- 0 = irrelevant.

Treat these as label definitions, not fabricated experiment results.

Create a script that evaluates retrieval and ranking for each test query.

Implement:

## Precision@K

Precision@K =
Number of relevant jobs among top K / K

## Recall@K

Recall@K =
Number of relevant jobs among top K /
Total known relevant jobs for that query

## NDCG@K

Implement normalized discounted cumulative gain using graded relevance labels. Document the gain and discount functions used.

## Structured-output validity

Measure the percentage of LLM responses that pass JSON/Pydantic validation.

Also test:

- Correct job IDs.
- Required response fields.
- Hallucinated skills.
- Unsupported explanations.
- Contradictions between the job description and explanation.
- Tool-call argument validation.
- Behavior when the LLM is unavailable.

Compare the following configurations:

A. Keyword-only search.
B. Semantic-only search.
C. Hybrid keyword and semantic retrieval.
D. Hybrid retrieval plus personalized ranking.
E. Hybrid retrieval, personalized ranking, and optional reranking.

Use the same held-out test queries for fair comparison. Do not tune weights on the test set.

Record real results and generate a comparison table. Explain any observed differences without assuming one method must outperform the others.

Add latency and cost measurements where practical.

Never invent experimental results, benchmark claims, or model performance statistics.

---

# 15. TESTING REQUIREMENTS

Use pytest and appropriate test utilities.

Implement unit tests for:

- Skill normalization.
- Profile validation.
- Resume extraction error handling.
- Ranking formula.
- Experience compatibility.
- Preference filtering.
- Empty search results.
- Missing job metadata.
- Malformed LLM responses.
- Unknown job IDs.
- Duplicate ingestion.
- Preference updates.
- Feedback recording.

Implement integration tests for:

- Database operations.
- Job ingestion.
- Search API.
- Profile APIs.
- Saved-job APIs.
- Preference APIs.
- Agent tool execution.
- Authentication and authorization if implemented.

Use mocked LLM calls for deterministic automated tests and avoid requiring a paid API key for every test.

Provide a separate optional integration test that uses a real LLM API.

Run the test suite and help me resolve failures before calling the relevant phase complete.

Do not claim that tests pass unless they have actually been executed successfully.

---

# 16. SECURITY AND RELIABILITY

Include these safeguards:

1. Keep API keys and database credentials in environment variables.
2. Provide a `.env.example` file without real secrets.
3. Never commit `.env` or credentials to Git.
4. Validate resume upload size and type.
5. Restrict access to uploaded resumes and avoid unnecessary permanent storage.
6. Treat resumes, job descriptions, and external content as untrusted data.
7. Defend against prompt injection in retrieved content.
8. Validate LLM-generated tool arguments.
9. Never execute arbitrary SQL generated by the model.
10. Use safe ORM operations and parameterized queries.
11. Implement appropriate timeouts and limited retries.
12. Add rate limiting where appropriate.
13. Avoid logging sensitive resume text or API keys.
14. Implement authorization for user-owned profiles and saved jobs.
15. Restrict administrative endpoints.
16. Handle invalid, missing, stale, or duplicate job listings.
17. Implement safe fallback explanations if the LLM fails.
18. Make search results available even if explanation generation fails.
19. Use reasonable pagination and resource limits.
20. Document known limitations.

If authentication is included, use an established, secure approach rather than storing plaintext passwords or inventing cryptographic mechanisms.

---

# 17. DOCKER AND DEPLOYMENT

Create a reproducible local development environment.

Include:

- Backend Dockerfile.
- Frontend Dockerfile if useful for the chosen deployment.
- Docker Compose configuration.
- PostgreSQL with pgvector support.
- Persistent database volume.
- Correct service networking.
- Environment-variable configuration.
- Database migration instructions.
- Health checks where appropriate.
- `.dockerignore`.
- `.gitignore`.

Provide exact commands for:

1. Creating the project directories.
2. Creating and activating a Python virtual environment.
3. Installing dependencies.
4. Configuring environment variables.
5. Starting PostgreSQL.
6. Enabling pgvector.
7. Running Alembic migrations.
8. Ingesting the sample dataset.
9. Starting FastAPI.
10. Starting the frontend.
11. Running tests.
12. Building and running with Docker Compose.

Clearly distinguish local development commands from production deployment commands.

For deployment, explain how to configure:

- Frontend hosting.
- Backend hosting.
- Managed PostgreSQL with pgvector.
- CORS.
- Production environment variables.
- Database migrations.
- HTTPS.
- Health checks.
- Logging and error reporting.

Verify provider compatibility before recommending a specific hosting configuration. Do not assume that every managed PostgreSQL provider supports pgvector.

---

# 18. REQUIRED PROJECT STRUCTURE

Use a modular directory structure similar to this:

ai-job-matching-agent/
    backend/
        app/
            main.py
            core/
                config.py
                security.py
            api/
                routes/
                    profile.py
                    jobs.py
                    chat.py
                    preferences.py
                    feedback.py
            models/
                user.py
                candidate.py
                job.py
                preference.py
                conversation.py
            schemas/
                profile.py
                job.py
                agent.py
                preferences.py
            services/
                resume_parser.py
                embeddings.py
                retrieval.py
                ranking.py
                llm_service.py
                agent.py
                memory.py
                ingestion.py
            db/
                database.py
                repositories.py
            evaluation/
                ranking_metrics.py
                llm_validation.py
        tests/
        requirements.txt
        Dockerfile
        alembic.ini
    frontend/
        src/
            components/
            pages/
            services/
            hooks/
            types/
        package.json
        Dockerfile
    data/
        sample_jobs.csv
        evaluation/
    scripts/
        ingest_jobs.py
        evaluate_ranking.py
    docker-compose.yml
    .env.example
    .gitignore
    README.md

Modify this structure if necessary, but preserve clear separation between routes, services, database access, schemas, and evaluation.

Do not create unnecessary files just to make the architecture look complicated.

---

# 19. README AND PORTFOLIO DOCUMENTATION

Create a professional README that includes:

- Project title.
- Problem statement.
- Objectives.
- Features.
- Architecture diagram.
- Tech stack.
- Data flow.
- Database schema overview.
- Retrieval and ranking algorithm.
- LLM and agent workflow.
- Setup instructions.
- Environment-variable reference.
- API endpoints.
- Testing instructions.
- Evaluation methodology and actual results when available.
- Screenshots.
- Deployment information.
- Limitations.
- Future improvements.

Explain the major engineering decisions so that I can discuss them confidently in interviews.

Potential future improvements include:

- Better reranking.
- Learning ranking weights from feedback.
- Scheduled job ingestion.
- Duplicate detection.
- Job freshness checks.
- Asynchronous ingestion tasks.
- Search caching.
- Observability.
- More sophisticated agent workflows.

Do not add technologies just for resume keyword stuffing. Only include technologies that the implementation actually uses.

---

# 20. DEVELOPMENT METHOD — FOLLOW THIS STRICTLY

This is one of the most important requirements.

Do not generate the entire project as a massive, untested code dump.

Implement the application incrementally in working phases.

## Phase 1: Environment and foundation

- Confirm the selected stack and prerequisites.
- Give the exact directory-creation commands.
- Create the backend.
- Configure dependencies.
- Set up PostgreSQL and pgvector.
- Configure SQLAlchemy.
- Create initial database models and migrations.
- Implement the health endpoint.
- Run the backend and verify that it starts.

## Phase 2: Job ingestion and basic search

- Create the CSV schema.
- Provide a small sample dataset clearly labeled as synthetic if necessary.
- Implement ingestion and deduplication.
- Implement job listing and keyword search.
- Add metadata filters.
- Test the endpoints.

## Phase 3: Semantic and hybrid retrieval

- Implement embedding generation.
- Add vector storage.
- Implement vector similarity search.
- Add keyword/vector result merging.
- Test retrieval with representative queries.
- Compare the retrieval strategies.

## Phase 4: Candidate profile and ranking

- Implement resume parsing.
- Add candidate profile CRUD operations.
- Implement the deterministic ranking engine.
- Return component scores and missing requirements.
- Add ranking unit tests.

## Phase 5: LLM explanations and conversational agent

- Configure the LLM provider.
- Implement structured explanations.
- Add tool schemas and safe tool execution.
- Implement preference persistence.
- Implement conversation context.
- Add error handling and mocked tests.

## Phase 6: Frontend

- Set up React, TypeScript, Vite and Tailwind CSS.
- Build profile management.
- Build the search dashboard.
- Build job detail views.
- Build the conversational interface.
- Connect every interactive element to the backend.
- Test loading, empty, error and success states.

## Phase 7: Evaluation and quality improvements

- Create a labeled test set.
- Implement Precision@K, Recall@K and NDCG@K.
- Implement structured-output validity tests.
- Compare retrieval and ranking configurations.
- Record actual experimental results.
- Fix failures and document limitations.

## Phase 8: Docker, CI and deployment

- Add Dockerfiles and Docker Compose.
- Run the application in containers.
- Add GitHub Actions tests.
- Configure deployment.
- Verify the deployed application.
- Finish the README and portfolio documentation.

After every phase:

1. Explain what has been implemented.
2. Provide the complete code for all new or modified files.
3. Specify each file's exact path.
4. Give the exact commands to run.
5. Explain what successful output should look like.
6. Provide the relevant tests.
7. Help debug errors before proceeding.
8. Summarize what is complete and what remains.
9. Keep the implementation consistent with earlier files and dependencies.

Never silently replace previously established architecture or rewrite working modules without explaining why.

If you modify an existing file, provide its complete revised contents rather than an ambiguous patch, unless I explicitly ask for a diff.

Do not use ellipses such as `...` to omit essential implementation code.

Do not claim that a command, test, deployment, or API call succeeded unless the result has actually been verified.

If you cannot run code in your environment, say so and provide instructions for me to execute it locally.

When an error occurs, diagnose the actual error, identify the relevant file, provide the correction, and explain why it works.

If you need information that materially affects implementation, ask a concise clarifying question. Otherwise, use reasonable defaults and continue rather than repeatedly asking for confirmation.

Do not overload me with all phases at once. Work sequentially while keeping the complete architecture in mind.

---

# 21. CODING QUALITY REQUIREMENTS

- Use type hints.
- Follow consistent Python naming conventions.
- Use clear module boundaries.
- Keep functions focused.
- Use async functions where appropriate and beneficial.
- Avoid unnecessary global state.
- Use configuration rather than hardcoded settings.
- Handle errors explicitly.
- Use database transactions appropriately.
- Keep business logic out of FastAPI route handlers.
- Avoid circular imports.
- Avoid duplicate implementations of the same logic.
- Avoid unnecessary dependencies.
- Add useful comments without commenting on every line.
- Keep secrets out of source code.
- Use deterministic tests where practical.
- Pin compatible dependency versions when appropriate.
- Explain any important trade-offs.
- Ensure the frontend request and response types match the backend schemas.
- Ensure the code is internally consistent across files.

The final result should be a coherent application that can actually be installed, started, tested, and demonstrated.

---

# 22. SUCCESS CRITERIA

The project should not be considered complete until the following are verified:

1. The backend starts successfully.
2. PostgreSQL and pgvector are configured correctly.
3. Job records can be ingested and stored.
4. Embeddings can be generated and retrieved.
5. Keyword and semantic search both work.
6. Hybrid retrieval works.
7. Candidate profiles can be created and edited.
8. Jobs are ranked using deterministic, explainable scores.
9. LLM explanations are generated and schema-validated.
10. The conversational agent executes actual tools.
11. Preferences persist across sessions.
12. The frontend communicates with the backend.
13. Users can inspect and save job listings.
14. Automated tests cover core business logic and API behavior.
15. Ranking metrics can be computed from a labeled evaluation set.
16. LLM failure does not completely break job search.
17. Secrets and user data are handled safely.
18. Docker-based local setup works.
19. The README contains reproducible setup instructions.
20. The application is demonstrable to a recruiter.

Do not fabricate evaluation results, production usage, job coverage, or performance improvements to satisfy these criteria.

---

# 23. YOUR FIRST RESPONSE

Begin by doing the following:

1. Briefly restate the project objective and intended user experience.
2. Present the final recommended architecture and explain the main technology choices.
3. List the prerequisites I need to install or configure on a Windows development machine.
4. Identify the minimum services and API keys required, including which components can run locally without paid APIs.
5. Present the development phases and what each phase will deliver.
6. Start Phase 1 immediately by providing the exact commands, initial folder structure, dependency configuration, environment setup, PostgreSQL/pgvector setup, initial database configuration, and health endpoint implementation.
7. Give complete code for every file needed in Phase 1.
8. Explain how to run the application and verify that it works.

Use Windows PowerShell for commands unless I ask for a different environment.

For database setup, provide a practical Docker-based option and explain any native alternative only if necessary.

Do not stop after presenting a plan. Start implementing the first working phase in the same response.

The overall goal is a fully functional, well-tested, properly documented AI Job Matching & Search Agent that I can build step by step, publish on GitHub, deploy, demonstrate, and discuss confidently in software engineering and AI-related interviews.
