# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project focuses on helping California State University, Fullerton (CSUF) students find information about academic support services, student organizations, scholarships, housing, dining options, graduate programs, and campus events.

This knowledge is valuable because students often need to search across multiple university websites, resource pages, and student discussion forums to find answers. Official information is scattered across different departments, while student experiences and recommendations are often only available through Reddit discussions. This RAG system combines both official resources and student perspectives into a single searchable knowledge base that provides quick, grounded answers with source attribution.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | ECS Student Success Center| Website| ECS Student Success Center| Details about Career guidance and oncampus help available | https://www.fullerton.edu/ecs/students/international-support.html|
| 2 | ECS Student Clubs Page| Website|ECS Student Clubs Page| List of clubs for stidents to get into as per their interests| https://www.fullerton.edu/ECS/students/clubs.html|
| 3 | Engineering Clubs Discussion| Reddit|Reddit: Engineering Clubs| Club details shared by students| https://www.reddit.com/r/csuf/comments/10k0755|
| 4 | Computer Engineering Advising Discussion| Reddit: Computer Engineering Advising| Advusors of department support to students| https://www.reddit.com/r/csuf/comments/fua9p1|
| 5 | CSUF Scholarships| Website| CSUF Scholarships| Details of scholarships for international students| https://international.fullerton.edu/international-students-and-scholars/scholarships/index.html|
| 6 | Engineering Club Recommendations| Reddit | Reddit: Engineering Clubs recommendations| Engineering club recommendations thread| https://www.reddit.com/r/csuf/comments/1m3lax3|
| 7 | Graduate Degree Programs| Website| Graduate degree options| Details for graduate options for international stidents| https://international.fullerton.edu/prospective-students/degrees/graduate-degrees.html|
| 8 | CSUF Housing portal| Website| CSUF housing| Details to apply for on campus housing| https://www.fullerton.edu/housing/apply/26-27/application-overview.html|
| 9 | CSUF Food services| Website| Food outlets| Options for food oncampus| https://www.fullerton.edu/food/hours/|
| 10 | CSUF ASI portal| Website| CSUF ASI team| ASi upcoming event details| https://asi.fullerton.edu/programming/#Upcoming%20Events|
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
250

**Overlap:**
50

**Why these choices fit your documents:**
Before chunking, HTML content, navigation menus, and unnecessary formatting were removed from the collected webpages and Reddit discussions. The cleaned text was then split into chunks of approximately 250 words with a 50-word overlap.

The documents primarily consist of FAQs, event descriptions, club information, and university resources. A chunk size of 250 words provides enough context to preserve complete ideas while remaining specific enough for accurate retrieval. The 50-word overlap helps prevent important information from being lost when content spans chunk boundaries.

During testing, larger chunks resulted in weaker retrieval performance because multiple topics were combined into a single embedding. Reducing the chunk size improved retrieval quality and lowered similarity distances.

**Final chunk count:**
34 chunks across 10 documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

Sentence Transformers: all-MiniLM-L6-v2

Embeddings were generated locally using the Sentence Transformers library and stored in ChromaDB for semantic retrieval.

**Production tradeoff reflection:**

The all-MiniLM-L6-v2 model was selected because it is lightweight, free, and performs well for semantic search tasks. It can be run locally without requiring API calls or usage fees.

If this system were deployed in production without cost constraints, I would evaluate larger embedding models such as BGE-Large or E5-Large. These models generally provide stronger semantic understanding, better retrieval accuracy, and improved handling of complex queries. However, larger models require more computational resources, have higher latency, and increase storage requirements. I would balance retrieval accuracy against response speed and operational cost.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt explicitly instructs the LLM to answer only using information contained within the retrieved context.

Example prompt:

"Answer the user's question using only the provided context. Do not use outside knowledge. If the retrieved documents do not contain enough information to answer the question, respond with: 'I don't have enough information in the provided documents to answer that question.'"

The retrieved chunks are inserted into the prompt before the user question, ensuring that the model has access only to the relevant document context.


**How source attribution is surfaced in the response:**

Source attribution is handled programmatically rather than relying entirely on the LLM. Each retrieved chunk includes metadata containing the source document name. After generation, the system appends a list of the retrieved source documents to the response.

Example:

Sources:

Student clubs.txt
Scholarships.txt

This guarantees that every response includes traceable source information.



---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What services does the ECS Student Success Center provide?| Academic support, tutoring, career guidance, workshops, and international student resources.| Retrieved I don't have enough information on that.| Relavant | Accurate |

| 2 | How can students become involved in engineering clubs at CSUF?| Students can join clubs such as ACM, IEEE, DSML, and participate in events and projects.| Retrieved Students can become involved in engineering clubs at CSUF by looking at Titanlink for a list of clubs, attending Discoverfest (a campus-wide tabling event), and checking out the college's website for engineering clubs. They can also attend tabling events such as Welcome to ECS Day, where clubs invite students to meet their officers. Additionally, students can log into the school's Discord with their school email to see all clubs offered at CSUF.| Relavant| Accurate|

| 3 | What scholarship opportunities are available for international students?| Abroova & Prabakar Scholarship and ISS scholarship opportunities.| Retrieved There are two scholarship opportunities mentioned: 

1.Abroova & Prabakar Scholarship: This scholarship is open to students without immigration status and to international students who demonstrate motivation for education and a significant financial need.

2.Minh Tâm Nguyen Scholarship for International Undergraduate Students: This scholarship was established to support international undergraduate students in achieving their educational goals.| Partially Relavant| Partially Accurate|

| 4 | How do students apply for on-campus housing?| Complete the housing application through the CSUF Housing portal and meet deadlines.| Retrieved Students apply for on-campus housing through the Housing Portal. They must complete the online application and submit it with a $50 non-refundable application fee, which must be paid using a debit or credit card.| Relevant| Accurate| 

| 5 | What dining options are available on campus?| Multiple dining locations including Baja Fresh, Starbucks, Juice It Up, Panda Express, and Pieology.| Retrieved The available dining options on campus include:

1.Carl's Jr. (Near Gordon Hall) - offers breakfast, burgers, chicken, salads, sides, and desserts
2.Baja Fresh Express (Titan Student Union) - offers burritos, tacos, quesadillas, nachos, tostadas, salads, and sides
3.Avanti Markets at Nutwood Café (Nutwood Café) - offers grab and go snacks, refreshments, and quick lunch
4.Hibachi-San (Titan Student Union) - offers traditional Japanese inspired cuisine (will be back in Fall 2026)
5.Juice It Up! (Titan Student Union) - offers blended-to-order fresh fruit smoothies, fresh-squeezed juices, and other beverages (will be back in Fall 2026)
6.Fresh Kitchen (Titan Student Union) - (will be back in Fall 2026)
7.On-Campus Food Trucks (Humanities Plaza) - will return in the Fall 2026.| Relevant| Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

"What scholarship opportunities are available for international students?"

**What the system returned:**
 
The system retrieved both scholarship information and general international student support information. Although the scholarship document appeared in the results, the top-ranked result came from the Student Success Center document rather than the dedicated scholarship source.

**Root cause (tied to a specific pipeline stage):**

The failure originated during the retrieval stage. The query contained the phrase "international students," which appears frequently in the Student Success Center document. The embedding model therefore considered that document semantically similar and ranked it slightly higher than the scholarship-specific document.

This caused retrieval noise and reduced answer precision.

**What you would change to fix it:**

I would improve retrieval by:

Using metadata filtering to prioritize scholarship documents for scholarship-related queries.
Increasing the number of scholarship-related source documents.
Using a stronger embedding model such as BGE-Large.
Implementing reranking after retrieval to prioritize chunks containing scholarship-specific terminology.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning document provided a clear roadmap for developing the RAG pipeline. Defining the chunking strategy, retrieval approach, and evaluation questions before implementation made it easier to verify whether each stage of the system was working correctly. The evaluation plan also provided objective criteria for measuring retrieval and generation performance.

**One way your implementation diverged from the spec, and why:**

The original planning document proposed using approximately 400-word chunks with a 75-word overlap. During retrieval testing, similarity distances were consistently above 0.7 and retrieval quality was poor. After experimenting with smaller chunks, I changed the implementation to 250-word chunks with a 50-word overlap. This reduced retrieval distances to approximately 0.38–0.54 for relevant results and significantly improved retrieval quality.


---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
The Chunking Strategy section from planning.md.
Requirements for fixed-size chunking with overlap.

- *What it produced:*
A Python chunk_text() implementation that split documents into overlapping chunks and generated metadata.

- *What I changed or overrode:*
The AI initially implemented larger chunk sizes similar to the original specification. After testing retrieval quality, I reduced the chunk size to 250 words and overlap to 50 words to improve semantic retrieval performance.

**Instance 2**

- *What I gave the AI:*
The Retrieval Approach section from planning.md.
Requirements for using all-MiniLM-L6-v2 and ChromaDB.

- *What it produced:*
Python code for embedding chunks, storing vectors in ChromaDB, and retrieving the top-k most relevant chunks.

- *What I changed or overrode:*
I modified the retrieval logic to include source metadata and distance-score reporting. I also tested different chunking configurations after noticing that initial retrieval scores were too high and often returned partially relevant documents.


**Sample Chunks**

================================================================================
Chunk #11 

Source: ASI events.txt 

--------------------------------------------------------------------------------
some of the stress that comes along with being in school, or just something to do while taking a break between classes. Events range from things like karaoke and open mic to film screenings and concerts and include special events around midterms and finals and even the biggest event of the year, Spring Concert. Association for InterCultural Awareness The Association for Inter-Cultural Awareness (AICA) is the part of Programming that plans events to highlight, celebrate, and educate students about culture and diversity. Performances, showcases, festivals, and experiences bring out a variety of culture-based student organizations and campus departments for activities that all students are welcome to attend., AICA gives students and the campus community the chance to come together to learn, g

================================================================================
Chunk #8 

Source: food_services.txt 

--------------------------------------------------------------------------------
Hall Convenience Store at Langsdorf Hall View Hours at TitanShops.com The Express at Titan Shops Convenience Store at Titan Shops View Hours at TitanShops.com The Yum at the TSU Convenience Store at the TSU View Hours at TitanShops.com TOGO'S Titan Student Union Monday - Friday: 10:00 AM - 2:00 PM Group order options are available at OC Choice Express

================================================================================
Chunk #9 

Source: ASI events.txt 

--------------------------------------------------------------------------------
Event Date Time Location Registration Poolside Cinema: The Wild Robot April 22 6 PM-9 PM SRC Pool Barbershop Talks April 28 noon-2 PM TSU Pub Destress at CBE April 30 3:30 PM SGMH3230 Spring Concert May 2 3 PM-9:30 PM Intramural Fields Spring Into Finals Picnic May 4 11 AM-1 PM Central Quad End of Year Pool Bash May 5 11 AM-2 PM SRC Pool ASI Pantry: Finals To-Go May 6 11 AM-1 PM Pantry Patio Glow Late Night Study May 7 6 PM-9 PM TSU Lower Level National Speech, Language and Hearing Month May 7 noon-2 PM Main Quad Brolates May 7 TBD SRC Pool Deck & Dance Studio Rec'd All Night Aug. 21 8:30 PM-11:30 PM SRC Beyond the Conversation ASI, in collaboration with the Division of Student Affairs and Strategic Enrollment Management, has joined forces to create a special series of events, headlined by

================================================================================
Chunk #33 

Source: Student clubs.txt 

--------------------------------------------------------------------------------
businesses led by our professionals daily, the impact of our organization is unmistakable. As trailblazers in shaping the future of Black Engineers and Blacks in STEM, NSBE stands at the forefront of positive change. OFFENSIVE SECURITY SOCIETY (OSS) @osscsuf | oss@osscsuf.org Jason Iwama, Faculty Advisor Offensive Security Society (OSS) is a student-led cybersecurity club dedicated to professionalism, hands-on learning, and excellence in the field of information security. We provide students with opportunities to develop technical skills through workshops, competitions, and industry-driven projects. This club also focuses on fostering collaboration and leadership. Our mission is to prepare members for success in both academic and professional environments by combining cybersecurity studies

================================================================================
Chunk #42 

Source: CSUF_housing.txt 

--------------------------------------------------------------------------------
Applying Housing offers are sent on a rolling basis Students must check their CSUF email daily Missing an email is not an acceptable reason for missed deadlines Offers are only emailed to students No parents, supporters, or guarantors receive housing emails Carefully review each section of the housing application before submitting. By completing and submitting your application, you agree to the terms and conditions outlined in the License Agreement, which constitutes a legally binding agreement between you and Housing and Residential Engagement. All official communication from Housing and Residential Engagement will be sent to your Cal State Fullerton student email address. Please check your CSUF email regularly, as many messages contain important and time-sensitive information that may re

 * Empty Chunks: 0 

**Retrieval Testing Results**

Query 1

Question:

What engineering clubs are available for students interested in machine learning?

Top Results

Rank	Source	Distance
1	Student clubs.txt	0.3814
2	engineering clubs recommendation.txt	0.4427
3	Student clubs.txt	0.5301
4	Enginerring clubs.txt	0.5364

Why the retrieval is relevant:

The top result contains information about the Data Science and Machine Learning Club (DSML), which directly answers the user's question.

Query 2

Question:

What scholarships are available for international students?

Top Results

Rank	Source	Distance
1	Student_sucess_center.txt	0.5248
2	Scholarships.txt	0.5385
3	graduate_Program.txt	0.5549
4	Student_sucess_center.txt	0.6060

Why the retrieval is partially relevant:

The Scholarships.txt chunk contains the correct answer. However, the Student Success Center chunk ranked higher because it contains several references to international students.

Query 3

Question:

How can students get involved in campus events?

Top Results

Rank	Source	Distance
1	ASI events.txt	0.4150
2	ASI events.txt	0.4323
3	Enginerring clubs.txt	0.4566
4	ASI events.txt	0.4759

Why the retrieval is relevant:

The highest-ranked chunks come from ASI events and describe student programs, the Street Team, and campus activities. These directly answer how students can participate in events.


**Example Responses**

The rubric explicitly requires source attribution visible.

Example Response 1

Question

What scholarships are available for international students?

Response

The Abroova & Prabakar Scholarship is available to international students who demonstrate financial need and motivation for education.

Sources:
- Scholarships.txt
- Student_sucess_center.txt
Example Response 2

Question

How can students get involved in engineering clubs?

Response

Students can join clubs such as DSML, IEEE, ACM, and Engineering Design Club. Students can also attend DiscoverFest and ECS tabling events.

Sources:
- Student clubs.txt
- Enginerring clubs.txt


**Out-of-Scope Example**

Required by the assignment.

Out-of-Scope Query Example

Question

Who won the 2026 NBA Finals?

Response

I don't have enough information in the provided documents to answer that question.

Sources:
None

** Query Interface Section**

Query Interface

The system uses a Gradio web interface.

Input Field

User Question textbox

Output Fields

Generated Answer
Retrieved Source Documents

Users enter a question about CSUF resources and the system retrieves relevant chunks from ChromaDB before generating a grounded response using Groq Llama 3.3 70B.


**Sample Interaction**

User Input

What dining options are available on campus?

System Response

The available dining options on campus include:

1. Carl's Jr. (Near Gordon Hall) - offers breakfast, burgers, chicken, salads, sides, and desserts
2. Baja Fresh Express (Titan Student Union) - offers burritos, tacos, quesadillas, nachos, tostadas, salads, and sides
3. Avanti Markets at Nutwood Café (Nutwood Café) - offers grab and go snacks, refreshments, and quick lunch
4. Hibachi-San (Titan Student Union) - offers traditional Japanese inspired cuisine (will be back in Fall 2026)
5. Juice It Up! (Titan Student Union) - offers blended-to-order fresh fruit smoothies, fresh-squeezed juices, and other beverages (will be back in Fall 2026)
6. Fresh Kitchen (Titan Student Union) - (will be back in Fall 2026)
7. On-Campus Food Trucks (Humanities Plaza) - (will return in Fall 2026)

Sources:
• ASI events.txt
• food_services.txt