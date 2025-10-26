# 🆔 User Identity Unification System

![Project Status](https://img.shields.io/badge/status-Completed-brightgreen?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Frontend](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Database](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![LLM](https://img.shields.io/badge/Ollama_Gemma_2B-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge) ---

## 📜 Introduction

The User Identity Unification System addresses the modern challenge of linking user identities scattered across multiple platforms (Email, WhatsApp, Dashboard, Instagram, etc.).It employs robust logic to resolve ambiguous or partial information, enabling precise identity unification.This is crucial for downstream analytics, personalization, and compliance in digital-first organizations.

---

## 🎯 Requirements

The system was built to meet the following key requirements:

🔗 **Link Disparate Identities:** Connect various identifiers (emails, names, phone numbers, handles) belonging to the same author across different platforms into a single internal profile.
🧠 **Phased Multi-Logic Matching:** Implement a sequential matching engine combining:
    ***Deterministic** (exact) matching.
    ***Fuzzy** (approximate) matching.
    ***LLM-based** (semantic/contextual) matching.
💯 **Confidence Scoring:** Assign a confidence score to each potential match.
❓ **Manual Review Threshold:** Implement a threshold-based system; matches below a certain confidence require manual verification.
💻 **User Interface:** Provide a flexible and easy-to-use system via a REST API and a React frontend.
📈 **Scalability & Maintainability:** Design for future data growth, extensibility to new platforms, and ease of maintenance.

---

## 🚦 Constraints and Conditions

The development adhered to specific constraints:

**Project Constraints:**

*Focus on matching logic; no user authentication required for the demo.
***Phase Isolation:** Higher-order matching (Fuzzy, LLM) only runs if the preceding phase fails to find a confident match.
***Unique Profile Linking:** Each platform identity must link to exactly one unified profile.
* **Confidence Handling:** Confidence scores must be numeric.Non-deterministic matches below a safe threshold require manual review.
***Single Phase Results:** Only one matching phase's results are returned per query.

**Technology Constraints:**

***Backend:** Python-based.
***Database:** Supabase (Managed PostgreSQL).
***LLM:** Local inference via Ollama (Gemma 2B specified) for privacy and cost control.
***Frontend:** React with Tailwind CSS.
***Deployment:** Docker-first approach for local execution via Docker Compose.

---

## 💡 Approach, Logic, and Justification

### Approach

***Layered Matching Strategy:** A three-tiered approach escalating in complexity: Deterministic -> Fuzzy -> LLM. This ensures efficiency and accuracy.
***API-Driven Design:** Business logic is exposed via REST endpoints, decoupling frontend and backend for modularity.
***Strict Phase Handling:** The backend logically proceeds to the next matching phase only if the current one yields no confident results, optimizing performance and ensuring predictable outcomes.

### Matching Logic Explained

1.  **Phase 1: Deterministic:**
    Normalizes identifiers (email, phone, username) to a standard format.
    Queries the database for an exact match on the normalized key.
    If found, assigns `confidence = 1.0` and `match_type = 'deterministic'`.
2.  **Phase 2: Fuzzy:**
    * *Runs only if Phase 1 fails.*
    * Compares input identifiers/names against existing records using:
        ***RapidFuzz:** Calculates similarity ratios (Levenshtein, token sort, partial) for typos/variations.
        ***Phonetics (Metaphone):** Matches similar-sounding names.
    * Calculates a weighted score.Matches above a threshold (e.g., 0.65) are returned with `match_type = 'fuzzy'`.
3.  **Phase 3: LLM (Semantic):**
    * *Runs only if Phase 1 & 2 fail or yield low confidence.*
    Sends pairs of identity records (source vs. candidate) to the local Gemma 2B LLM via Ollama.
    A carefully crafted prompt asks the LLM to determine if they represent the same person, providing its confidence and reasoning in JSON format.
    Matches confirmed by the LLM (`is_match: true`) above a threshold (e.g., 0.65) are returned with `match_type = 'llm'`.
***Result Encoding:** Each query returns results from *only one* phase, clearly tagged with `match_type` and `confidence`.

### Justification for the Approach

✅ **Robustness:** Prioritizing exact matches minimizes false positives with clean data.
🎯 **Coverage:** Fuzzy logic catches near-misses like typos and nicknames.
🤖 **Intelligence:** The LLM phase adds contextual reasoning for complex edge cases missed by string-based methods.
🔒 **Safety & Review:** The phased approach combined with confidence thresholds and manual review for uncertain matches minimizes the risk of incorrect merges.This is more controllable than simultaneously weighting all methods.

---

## 🛠️ Technology Stack & Rationale

| Category          | Technology                                                                                                | Rationale                                                                                                   |
| :---------------- | :-------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| **Frontend** | ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) + Vite + ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white) |Modern, component-driven UI with fast dev cycle.            |
| **Backend API** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) + Python          |Lightweight, modular, proven framework for REST APIs.                    |
| **String Matching** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) (RapidFuzz, Phonetics) |High-performance libraries for fuzzy/phonetic matching.                   |
| **LLM** | ![Ollama](https://img.shields.io/badge/Ollama-222222?style=flat&logo=ollama&logoColor=white) + ![Google Gemma](https://img.shields.io/badge/Gemma_2B-4285F4?style=flat&logo=google&logoColor=white) |Secure, scalable, local LLM execution. |
| **Database** | ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white) + ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) |Managed, scalable SQL DB with easy integration. |
| **Containerization**| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)             |Consistent development and deployment.                             |

*Rationale Summary:* The chosen technologies provide modularity, strong community support, and align with project scale, performance, and privacy requirements.

---

## 🎁 Deliverables

📄 **Supabase Database:** SQL schemas for all tables and sample seed data.
⚙️ **Backend:** Flask API with modular matchers (deterministic, fuzzy, LLM), data normalization utilities, API routes, and Dockerfile.
🎨 **Frontend:** React application with components for displaying profiles, adding identities, finding matches, showing color-coded results (Green/Yellow/Purple), displaying LLM reasoning, and basic stats.
🧪 **Testing:** Sample inputs and guidance for end-to-end verification.
📚 **Documentation:** Setup instructions, usage guide, and system flow explanation.

---

## ✨ Key Enhancements

**Backend:**

*Modular matcher classes organized by phase (Deterministic, Fuzzy, LLM).
*Single, atomic `/match` endpoint handling the phased logic.
*LLM integration specifically for ambiguous or unmatched cases.
*Strict type-checking in normalization and matching functions.

**Frontend:**

* Dynamic, color-coded display of match results:
    🟩 **Green:** Deterministic (Exact Match).
    🟨 **Yellow:** Fuzzy (Approximate Match).
    🟪 **Purple:** LLM (Semantic Match).
Live display of match type, confidence percentage, and expandable LLM reasoning.
Foundation for a manual review UI (pending candidates list).

---

## 🌊 System Flow Overview

1. **Input:** User enters identity information (platform identifiers, optional display name) into the React frontend and submits a match request.
2. **API Request:** Frontend sends data to the Flask backend's `/api/v1/match` endpoint.
3.  **Backend Processing:**
    * Runs **Deterministic** matching.If a confident (1.0) match is found, returns result.
    * If no deterministic match, runs **Fuzzy** matching.If confident matches (>=0.65) are found, returns results.
    * If still no confident match, runs **LLM Semantic** matching.Returns matches confirmed by the LLM (>=0.65).
4. **API Response:** Backend returns results from *only one* phase (the first successful one), including `match_type` and `confidence`.
5. **Frontend Display:** React UI renders the matches, color-coded by `match_type`, showing confidence and LLM reasoning where applicable.
6. **Review (Future):** Low-confidence matches (below threshold) would ideally be flagged in a separate list for admin review.

---

## 🔮 Future Improvements

***Scalability:** Explore distributed LLM inference or cloud options; consider database sharding for very large datasets.
***UX:** Develop a full admin dashboard for managing the pending review queue, viewing match history, and configuring thresholds.
***Security:** Implement fine-grained Role-Based Access Control (RBAC), enhance audit trails, and ensure PII protection.
***ML Feedback Loop:** Use admin decisions (approvals/rejections) on pending matches to potentially fine-tune matching weights or LLM prompts over time.
***Integrations:** Add support for more identity platforms (e.g., Twitter, LinkedIn); implement webhooks for real-time identity updates.
***Performance:** Introduce caching for LLM responses; consider async task queues for intensive matching operations.

---

## ✅ Conclusion

This project successfully delivers a robust and modular User Identity Unification System, meeting all core requirements. By employing a phased architecture combining exact, fuzzy, and sophisticated LLM-based semantic matching, it ensures flexibility, maintainability, and extensibility.The clear visual and technical separation provides a solid foundation for future enhancements and scaling in real-world applications.

---

*Add links to your repository, live demo (if applicable), or contact info below.*

[![View Repository](https://img.shields.io/badge/View_Repository-GitHub-blue?style=for-the-badge&logo=github)](https://github.com/your-username/your-repo-name) ```