# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Students at California State University, Fullerton rely on information from many different sources to learn about academic support, student organizations, housing, dining, scholarships, and campus opportunities. This information is scattered across university websites and student discussions, making it difficult to find relevant answers quickly. This RAG system will consolidate official resources and student experiences into a searchable knowledge base to help students navigate campus life more effectively.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | ECS Student Success Center| Details about Career guidance and oncampus help available | https://www.fullerton.edu/ecs/resources/StudentSuccessCenter.php|
| 2 | ECS Student Clubs Page| List of clubs for stidents to get into as per their interests| https://www.fullerton.edu/ECS/students/clubs.html|
| 3 | Reddit: Engineering Clubs| Club details shared by students| https://www.reddit.com/r/csuf/comments/10k0755|
| 4 | Reddit: Computer Engineering Advising| Advusors of department support to students| https://www.reddit.com/r/csuf/comments/fua9p1|
| 5 | CSUF Scholarships| Details of scholarships for international students| https://international.fullerton.edu/international-students-and-scholars/scholarships/index.html|
| 6 | Reddit: Engineering Clubs recommendations| Engineering club recommendations thread| https://www.reddit.com/r/csuf/comments/1m3lax3|
| 7 | Graduate degree options| Details for graduate options for international stidents| https://international.fullerton.edu/prospective-students/degrees/graduate-degrees.html|
| 8 | CSUF housing| Details to apply for on campus housing| https://www.fullerton.edu/housing/apply/26-27/application-overview.html|
| 9 | Food outlets| Options for food oncampus| https://www.fullerton.edu/food/hours/|
| 10 | CSUF ASI team| ASi upcoming event details| https://asi.fullerton.edu/programming/#Upcoming%20Events|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
