# Execution prompt

Act as the Requirements Engineering specialist defined in the system prompt. Complete the expert-evaluation questionnaire in the attached pair context.

Read the shared context and the project summary, then compare Team X and Team Y for all seven stories. Judge Completeness, Clarity, Correctness, and Consistency independently, using the exact definitions and the three answer options in the form.

Answer all 28 preference questions when the evidence supports a comparison, and give a concise evidence-based explanation for each. Errors, duplicated, misplaced, or truncated text inside a story belong to that team's specification: judge them under the four characteristics rather than reporting them as input issues. Leave an answer empty only when the supplied material itself is missing or unreadable, and list that question under `input_issues`. Do not use No preference as a substitute for missing information.

Return only the JSON object defined in the system prompt. Do not guess which team should win, evaluate another form, rewrite the stories, invent facts, produce absolute quality labels or scores, or submit the questionnaire. Write the entire response in English.
