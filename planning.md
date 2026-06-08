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
400
**Overlap:**
75
**Reasoning:**

I will use fixed-size chunks of approximately 400 words with an overlap of 75 words.

Most official CSUF webpages are medium-length documents containing headings, short paragraphs, and bullet lists. A 400-word chunk is large enough to preserve context while remaining focused on a specific topic. The 75-word overlap helps ensure that important information located near chunk boundaries is not lost during retrieval.

For Reddit discussions, important information may be spread across multiple comments. The overlap allows related opinions and recommendations to remain connected even when split across chunks.

If chunks are too small, retrieval may return incomplete information and lose context. For example, a query about housing requirements might retrieve only part of the application instructions. If chunks are too large, retrieval may return irrelevant information and reduce embedding precision because multiple topics are mixed together.

The overlap improves retrieval quality by preserving continuity between adjacent chunks and reducing the risk of splitting key facts across boundaries.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

I will use the sentence-transformers all-MiniLM-L6-v2 embedding model because it is lightweight, free, and widely used for semantic search applications.

Embeddings will be stored in ChromaDB and queried using cosine similarity.

**Top-k:**

For each user query, I will retrieve the top 4 most relevant chunks (top-k = 4).

**Production tradeoff reflection:**

Retrieving too few chunks may omit important information needed to answer a question completely. Retrieving too many chunks may introduce irrelevant information, increasing the likelihood of inaccurate responses and making prompts unnecessarily large.

Semantic search works because embeddings capture the meaning of text rather than relying only on exact keyword matching. For example, a user asking about "career help" may retrieve content discussing "career guidance" even if those exact words do not appear in the query.

If cost and computational resources were not constraints, I would consider larger embedding models such as BGE-large or E5-large because they generally provide better semantic understanding, improved retrieval accuracy, and stronger performance on longer or more complex documents.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What services does the ECS Student Success Center provide?| Academic support, tutoring, career guidance, workshops, and student success resources.|
| 2 | How can students become involved in engineering clubs at CSUF?| Students can join organizations listed on the ECS Student Clubs page and participate in club meetings, projects, and networking events.|
| 3 | What scholarship opportunities are available for international students?| Scholarships listed through the International Students and Scholars Office, including eligibility requirements and application information.|
| 4 | How do students apply for on-campus housing?| Students must complete the housing application process described on the CSUF Housing Application page and meet the required deadlines.|
| 5 | What dining options are available on campus?|  Various dining locations and food service facilities listed on the CSUF Food Services page, along with operating hours.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.Mixed Document Types
The dataset contains both official university webpages and informal Reddit discussions. Student opinions may be subjective or inconsistent compared to official information.

2.Chunk Boundary Issues
Important information may be split across chunk boundaries, causing incomplete retrieval results. The overlap strategy is intended to reduce this risk.

3.Source Attribution
Responses should clearly identify whether information comes from official university resources or student discussions to improve trustworthiness.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Document Ingestion → Chunking → Embedding (all-MiniLM-L6-v2) → ChromaDB → Retrieval → Groq Llama 3.3 70B

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

1.Document Collection and Preprocessing

I will use Claude to help generate Python scripts for downloading, extracting, and cleaning text from webpages and Reddit discussions.

Input to Claude:

The list of source URLs from the Documents section.
Project requirements for storing documents as text files.

Expected Output:

Python code that extracts webpage content, removes unnecessary HTML elements, and saves clean text files for indexing.

Verification:

I will manually inspect several generated text files to ensure the extracted content matches the original webpages and does not contain excessive navigation menus or formatting artifacts.

2.Chunking Implementation

I will use Claude to implement the document chunking functionality.

Input to Claude:

The Chunking Strategy section of this planning document.
Requirements specifying 400-word chunks with a 75-word overlap.

Expected Output:

A Python function chunk_text() that splits documents into chunks according to the specified chunk size and overlap.

Verification:

I will test the function on sample documents and confirm that chunk lengths are approximately 400 words and that consecutive chunks share the required overlap.

3.Embedding Generation

I will use Claude to generate code for creating embeddings using the sentence-transformers library and the all-MiniLM-L6-v2 model.

Input to Claude:

The Retrieval Approach section.
The requirement to use all-MiniLM-L6-v2 for semantic search.

Expected Output:

Python code that loads the embedding model and converts document chunks into vector embeddings.

Verification:

I will verify that embeddings are generated successfully and that each chunk receives a corresponding vector representation.

4.ChromaDB Integration

I will use Claude to implement storage and retrieval using ChromaDB.

Input to Claude:

The Retrieval Approach section.
ChromaDB documentation and project requirements.

Expected Output:

Code that stores chunk embeddings in a ChromaDB collection and retrieves the most relevant chunks using similarity search.

Verification:

I will run test queries and confirm that retrieved chunks are relevant to the query and correspond to the correct source documents.

5.Retrieval-Augmented Generation Pipeline

I will use Claude to help integrate retrieval results with the Groq LLM.

Input to Claude:

The Retrieval Approach section.
Assignment requirements for RAG.
Sample retrieved chunks and user queries.

Expected Output:

Python code that retrieves top-k chunks, constructs a prompt, sends it to the Groq API, and generates a response based on retrieved context.

Verification:

I will compare generated responses against the retrieved chunks to ensure answers are grounded in the source material rather than fabricated information.

6.Evaluation and Testing

I will use Claude to generate additional test cases and evaluate retrieval performance.

Input to Claude:

The Evaluation Plan section.
Sample outputs from the retrieval system.

Expected Output:

Additional test questions and suggestions for measuring retrieval accuracy and response quality.

Verification:

I will manually compare generated answers against the expected answers listed in the Evaluation Plan and confirm whether the system retrieves the correct supporting information.

7.Documentation and README

I will use Claude to review project documentation and improve clarity.

Input to Claude:

The completed planning document.
Project implementation details and setup instructions.

Expected Output:

Suggestions for improving organization, readability, and completeness of the README and project documentation.

Verification:

I will ensure that all project requirements are documented and that another user could reproduce the project by following the provided instructions.


**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
