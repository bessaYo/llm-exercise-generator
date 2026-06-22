Dear Mart,

We thank you and the three reviewers for the opportunity to improve our paper and the instructive comments that greatly supported the revision process.

We have updated our submission on EasyChair and addressed the provided feedback as follows:

**1. The overlapping of Bloom categories**

We acknowledge that the keyword-matching approach can be weakened by overlapping words in the learning objectives, which may match several Bloom categories. We kept the current approach (selecting the first detected level) and strengthened the future-work discussion in Section 7, noting that more robust alternatives, such as LLM-based classification or optional instructor confirmation of the level, should be evaluated.

**2. A discussion of potential failure points: propagated summary distortions or incomplete slides**

These are valid points. Lecture slides can be incomplete and the LLM summarisation step can lose or distort information before it reaches the generator. We now name both explicitly as limitations in Section 6. First, the generation step relies on LLM-generated slide summaries, which we use deliberately to extract the exercise-relevant content and keep the prompt within the context window, but summarisation errors can then propagate into the exercise unchecked; as future work, the summaries could be validated against the source slides to catch such distortions. Second, the pipeline relies only on the lecture slides, so material taught only in lectures or textbooks cannot be covered; we accept this as a limitation of a slides-based approach, and a natural extension would be to incorporate additional sources such as textbooks or instructor notes.

**3. Domain expert evaluation of generated exercises**

This is a fair point. The exercises were not validated by instructors. We state this as a limitation in Section 6 and name, as future work in Section 7, an expert review of a sample (rating objective alignment, difficulty, and classroom readiness) to confirm pedagogical quality.

More details on how we addressed each reviewer's suggestions can be found in the attached PDF file (indicated by indented bullet points, as above).

Best regards

---

# Reviewer 1
---
### Point 1
*Reviewer Comment:* "We target programming exercises in the domain of functional programming using Haskell, a language commonly taught in university-level programming courses." Provide examples of what you mean. Taught where? At what levels of the curriculum?

**Response:** In Section 1 (Introduction) we now name the university and course level and give concrete examples.

### Point 2

*Reviewer Comment:* "Our framework combines two sources of guidance: Learning Objectives (LOs) categorized by Bloom’s taxonomy
and lecture slides that contain the actual teaching material of a course." As I advanced through the manuscript, I kept asking myself: what if the lecture slides are incomplete? Rarely, if ever, does an instructor include everything that is taught or needs to be taught on the slides. After all, this is why we have lectures and textbooks to deliver important material to students. Your design seems to assume that lecture slides are complete. Much to my surprise this concern is not mentioned in the limitations section nor as part of your future work. This is an important (design) issue that needs to be addressed. It ought to be feasible to include the textbook of instruction and/or instructor written guidance as elements that are used to generate programming problems. I understand that in this first version of the tool, this concern has not been addressed. However, you can discuss this limitation and outline in your future work how this is to be addressed.

**Response:** The concern is valid. We now state it explicitly in Section 6 (Limitations) and note that the tool could be improved by adding further material such as textbooks or instructor notes.

### Point 3

*Reviewer Comment:* "In our approach, we embed learning objectives and lecture slides to compute semantic similarity and
identify the slides that are most semantically relevant for each objective." For readers not familiar with cosine similarity, it would be opportune to highlight that you are looking at the angles between the vectors as the measure for similarity.

**Response:** We added a parenthetical remark in Section 2.2, where the metric is introduced, noting that cosine similarity measures the angle between the vectors.

### Point 4

*Reviewer Comment:* "The goal was to evaluate the exercises generated with minimal manual effort."
It is unclear what is meant by minimal manual effort. Furthermore, discuss why this is a good or reasonable goal. Once again, I am thinking about the slides being incomplete.

**Response:** The term was underspecified. We rephrased the opening of Section 5.3 to state the goal directly: the evaluation pipeline is automated and aimed at assessing the generated exercises at scale, so that an instructor does not need to hand-check every exercise. This clarifies what we meant by minimal manual effort and, at the same time, explains why a low-supervision evaluation is a reasonable goal, since it is what lets an individual instructor apply the approach at scale. (The overall evaluation is still described as semi-automated in the Section 5 introduction, as interpreting the aggregated results involves inspecting a few representative exercises.)

### Point 5

*Reviewer Comment:* "Of the 17 exercises containing Haskell code, 12 passed the compilation check, resulting in an overall
success rate of about 71%. Some failures occurred because the generated code was incomplete, even
though the provided fragments were syntactically valid." I appears that you are selling the performance short. Yes, of course, incomplete code will fail to compile. What is the success rate for complete code? This metric ought to be reported and is likely the more important metric.	In addition, mention all the reasons for failure as done for the use of filter being applied to a programmer-defined datatype.

**Response:** We agree the complete-code success rate is the more meaningful indicator. The pipeline separates failures caused by truncated, incomplete fragments (e.g. a type signature without a body) from genuine type or semantic errors, so that truncation artifacts do not deflate the rate.

In the revised evaluation, 14 Haskell snippets were generated, of which 13 compiled. All 14 were complete code, so the complete-code rate equals the overall rate, 13/14 (92.9%). In Section 5.4 we report this rate and list the single failure cause: a genuine type error in an Evaluate-level exercise comparing two factorial implementations, where the memoized variant uses the result of `lookup` (of type `Maybe Integer`) directly as an `Integer`, which GHC rejects with "Couldn't match expected type 'Integer'".

### Point 6

*Reviewer Comment:* "One possible explanation is that Gemma 3 is a general purpose model, whereas Qwen2.5-Coder is specifically optimized for programming-related tasks" Why use or report the results using Gemma 3? What is the point if it is not optimized for programming-related tasks?

**Response:** The reviewer is right that specialized models are better options. Yet, they are not always (easily) available, so a comparison can be instructive. We therefore decided to keep the Gemma 3 experiments.

### Point 7

*Reviewer Comment:* "Despite growing interest in LLM-based question generation, most existing research in education has focused primarily on MCQs." Yes, indeed, a great deal of work has focused on MCQs. However, related work ought to also cover efforts beyond generation of MCQs. Here are a few pointers that may guide bolstering your related work section (...)

**Response:** Thank you for the pointers! We added all four suggested references to the related-work discussion in Section 3.


### Style

*Reviewer Comment:* The sentence after RQ3 is simply repeating the contents of RQ3. This is unnecessary. Please remove it

**Response:** Done. We removed the sentence after RQ3 that repeated its content (Section 5).

*Reviewer Comment:* The elements of Bloom's taxonomy are outlined twice: Section 2.3 and Section 4.1. This is unnecessary. The important outline is the one in Section 4.1. I strongly suggest omitting or summarizing in prose the description in Section 2.3
:

**Response:** Done. We have removed the redundant bulleted list from Section 2.3 and summarized the background of Bloom's taxonomy in a concise prose paragraph.

### Typos
We fixed all typos and grammatical problems listed.


# Reviewer 2

---

### Point 1
*Reviewer Comment:* To verify grammar, it seems preferable to remove embedded code snippets prior to the analysis instead of weakening the grammar checker by excluding rules. Since the paper already implements code extraction for the compilation phase, a similar mechanism could likely have been reused for grammar evaluation as well.

**Response:** We reimplemented the grammar stage (Section 5.3) along these lines. Instead of disabling LanguageTool rules that misfire on embedded code, we remove the code before checking: fenced code blocks are dropped, and inline code spans are replaced with a neutral placeholder so the surrounding sentence stays grammatical (deleting them outright would create artifacts such as doubled commas where a code item sat in a list). All grammatical rules then stay active; the only rule we still disable is the spell-checker, because the prose legitimately contains Haskell identifiers and keywords (e.g. `newtype`, `Int`) that are domain vocabulary, not misspellings. On the same set of exercises, this drops the total flagged issues from 23 to 6: the removed flags were code-induced false positives (on Evaluate-level exercises, 12 spurious flags fell to 0), and the 6 that remain are genuine prose issues the previous blacklist had masked.

### Point 2

*Reviewer Comment:* Table 4 suggests that 18 code snippets were generated, but the text later states "Of the 17 exercises containing Haskell code". Is this because some exercises contain more than one code snippet?

**Response:** Correct, some exercises embed more than one code block (for example, Evaluate-level exercises that present two implementations to compare), so snippets can outnumber exercises. In the revised paper we report the snippet count consistently in the running text and in the caption of Table 4 (labelled "fenced Haskell code snippets"), so the two figures no longer disagree.

### Point 3

*Reviewer Comment:* It is not entirely clear to me whether the missing implementation in Listing 1 is actually an error, or whether the intention of the exercise was only to provide the type signature, which would make this a false positive.

**Response:** In the revised evaluation the exercises were regenerated, so the original Listing 1 no longer appears. The underlying concern is now handled structurally: the pipeline classifies a missing-definition or truncated fragment as an *incomplete* failure, distinct from a *genuine* type error, and reports the complete-code success rate separately (see our response to Reviewer 1, Point 5). In the revised run there were no incomplete failures; the only compilation failure is a genuine type error (now shown in Listing 1).

# Reviewer 3

---

### Point 1
*Reviewer Comment:* The grammar evaluation manually excludes rules that fire on embedded code.
  Was it considered to strip all code blocks before running LanguageTool?
  If the output is JSON with Markdown code blocks, filtering on
  backticks or the code field seems straightforward and would avoid
  the residual false positives entirely.

**Response:** We adopted exactly this approach: the grammar stage now strips the code before running LanguageTool (Section 5.3). See our response to Reviewer 2, Point 1 for details and the before/after numbers.

### Point 2

*Reviewer Comment:* For the Understand-level exercise in Figure 6,
  the task asks students to identify ill-typed expressions.
  Given that LLMs are predominantly trained on well-typed code,
  are they reliably able to construct intentionally ill-typed examples?
  And is the ill-typedness verified anywhere in the pipeline?

**Response:** This is an important point, and it led us to add expression-level type-checking to the pipeline (Section 5.3). Beyond compiling the fenced code blocks, we now type-check every inline Haskell expression by compiling it individually with GHC and classifying it as well-typed or ill-typed. Applied to the Understand-level exercises that ask students to identify ill-typed expressions, this shows the model does construct genuinely ill-typed examples: in the revised evaluation (Section 5.4), of the 85 inline expressions, 81 are well-typed and 4 ill-typed. The 4 ill-typed ones all occur in the Understand-level exercises and are exactly the expressions the exercise presents as not well-typed (e.g. `let f x = x + 1 in f True`, which GHC rejects with "No instance for Num Bool"). So, to the two questions: (i) the model can produce intentionally ill-typed expressions, and (ii) the ill-typedness is now verified rather than assumed. Being deliberately ill-typed, these expressions are pedagogical content, not generation errors, and are reported separately from the compilation success rate.

### Point 3

*Reviewer Comment:* For the compilation failure in Listing 1:
  was the missing implementation intentional (a fill-in-the-blank exercise),
  or a genuine generation error?

**Response:** This is the same concern as Reviewer 2, Point 3; please see our response there. In short, the revised evaluation regenerated the exercises, so the original Listing 1 no longer appears, and the pipeline now classifies any missing-definition or truncated fragment as an *incomplete* failure, distinct from a genuine type error. In the revised run there were no incomplete failures.

### Point 4

*Reviewer Comment:* Table 1: the benchmark numbers are for the 32B model,
  while the 7B variant is used for generation.
  This is mentioned in a footnote;
  flagging it in the table caption too would avoid a misleading impression

**Response:** We updated the caption of Table 1 to state that the benchmark scores refer to the 32B variant, while our local deployment used the smaller 7B variant on consumer hardware.


### Point 5

*Reviewer Comment:* §4.2: the choice $k = 3$ for retrieved slides is presented as a practical decision but is not ablated.
  A sentence acknowledging this was not tuned would be useful.

**Response:** We added a sentence to Section 5.2 stating that $k=3$ was a heuristic choice to keep the prompt compact and was not systematically tuned.