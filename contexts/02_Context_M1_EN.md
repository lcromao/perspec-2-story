# Evaluation context for Pair M1

Pair ID: M1

Project ID: M

Project name: Malicious URL Classification

Output language: English. Evaluate this pair only. The participant-facing content below reproduces the supplied form from Page 2 onward.

## Page 2 — Project summary and evaluation instructions

In the next seven pages, you will read the seven stories of two specifications written by different agile teams, Team X and Team Y, for the project summarized below. On each page, read both versions of the story and indicate, for each of four quality characteristics, which version you prefer.

Judge each characteristic on its own; the version you prefer in one characteristic may not be the one you prefer in another. The labels X and Y do not identify the authors or how the specifications were produced.

### Project summary — Malicious URL Classification

User story [US01-M]: As a security analyst, I want the browsing assistant to classify URLs as phishing or non-phishing before navigation, so that users receive a warning and can decide how to proceed.

A browsing assistant in an application or proxy checks each submitted or intercepted URL before navigation. It returns a phishing/non-phishing class, a risk score and supporting reasons. The application warns the user and recommends avoiding a phishing URL; the user makes the final choice. Reviewers verify reported classification errors before their labels are reused.

The offline pilot uses Mendeley dataset_B (v3): 11,430 balanced URLs with 87 features describing URL syntax, page content and external queries. Reviewed application URLs and verified PhishTank and Tranco labels support updates. The feature-extraction service is isolated and restricts external access; users are never asked to visit suspicious URLs. All targets and resource limits are proposed pilot decisions, not achieved results.

### Quality characteristics

For each story, you will compare the two versions on:

- Completeness (complete–incomplete): The story includes the information needed to carry out and accept the work, without relevant omissions.
- Clarity (clear–ambiguous): The story can be understood in only one way, without vague or ambiguous statements.
- Correctness (correct–incorrect): The statements in the story are true for the project and its domain; it states no incorrect facts.
- Consistency (consistent–inconsistent): The statements in the story do not contradict each other or the project context.

---

## Page 3 — Story 1 of 7 — Data Collection

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Data Collection Story

Data collection should

- Use Mendeley dataset_B (v3) as the historical base for the offline pilot. Add URLs reviewed from the application and confirm labels with PhishTank (reported phishing sites) and Tranco (popular sites).
- Collect the 11,430 URLs (50% phishing, 50% legitimate) with 87 features covering URL syntax, page content and external queries, gathered in May 2020. Remove the URL index column and report counts after cleaning and in each data split.
- Load historical data before development; keep online-query features within the two-second budget; add approved updates daily and review user reports within 7 days.
- Check coverage of both classes, URL forms, languages, domain ages and unreachable sites; require an ID and a label per record and document gaps.
- Use only sources whose terms allow this use; protect private browsing and never ask users to open suspicious URLs.
- Replace user and request identifiers with codes and remove passwords, tokens and other secrets from URLs, keeping what the features need.
- Use only sources whose terms allow this use; protect private browsing and never ask users to open suspicious URLs.

### Team Y — Data Collection Story

Data collection should

- Download Mendeley dataset_B (version 3).
- Add URLs reviewed from the application, and confirm labels with PhishTank (reported phishing sites) and Tranco (a list of popular sites).

Outcome / acceptance: The initial dataset_B release is available with its source, version, size and coverage recorded; procedures for collecting recent reviewed URLs and approved daily updates are defined, and potentially sensitive URLs are handled under the project’s security and privacy requirements.

**1.1.a — In terms of completeness (complete–incomplete), which version of the Data Collection story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**1.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**1.2.a — In terms of clarity (clear–ambiguous), which version of the Data Collection story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**1.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**1.3.a — In terms of correctness (correct–incorrect), which version of the Data Collection story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**1.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**1.4.a — In terms of consistency (consistent–inconsistent), which version of the Data Collection story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**1.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_

---

## Page 4 — Story 2 of 7 — Data Pre-processing

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Data Pre-processing Story

Data pre-processing should

- Describe each of the 87 features: meaning, type, how it is computed, unit, missing value code and whether it is available at check time; define the label as 0 = non-phishing, 1 = phishing.
- Check that features were extracted correctly and resolve conflicting labels; manually review 10% of records covering both classes, separate unresolved records and report exclusions.
- Use 70% of labeled URLs for training, 15% for choosing settings and 15% for final testing; keep URLs from the same domain in the same part and split by time when dates are reliable.
- Record source, date, evidence and reviewer for each label; treat popularity lists and user reports as evidence, not confirmed truth.
- Recheck coverage by source, language, TLD and domain age after cleaning; avoid features that reveal where a label came from rather than the URL itself.

### Team Y — Data Pre-processing Story

Data pre-processing should

- Keep varied HTTP and HTTPS URLs.
- Exclude malformed URLs, URLs with unresolved labels and features that cannot be computed at check time.

**2.1.a — In terms of completeness (complete–incomplete), which version of the Data Pre-processing story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**2.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**2.2.a — In terms of clarity (clear–ambiguous), which version of the Data Pre-processing story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**2.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**2.3.a — In terms of correctness (correct–incorrect), which version of the Data Pre-processing story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**2.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**2.4.a — In terms of consistency (consistent–inconsistent), which version of the Data Pre-processing story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**2.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_

---

## Page 5 — Story 3 of 7 — Data Management

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Data Management Story

Data management should

- I4: Storage: Keep URLs and features in restricted file storage, user reports in a database, code in Git and approved models in a model registry (a catalog of model versions). Restrict access to URLs.
- I7: Reproducibility: Keep the dataset version, split IDs, feature code, settings, random seed, exact software versions and container version for each run, so the same result can be produced again

D4: Data dictionary: Describe each of the 87 features: meaning, type, how it is computed, unit, missing value code and whether it is available at check time. Label: 0 = non-phishing, 1 = phishing.

D15: Data distribution: Use 70% of labeled URLs for training, 15% for choosing settings and 15% for final testing. Keep URLs from the same domain in the same part; split by time when dates are reliable

D16: Golden dataset: If used, reserve 400 expert-reviewed URLs covering both classes and difficult cases, versioned and excluded from tuning. Use only for final checks; report full-test results too.

### Team Y — Data Management Story

Data management should

- Load the historical dataset in batches for training.
- During use, receive one request per URL and answer immediately;
- add reviewed labels and approved source updates once a day.

**3.1.a — In terms of completeness (complete–incomplete), which version of the Data Management story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**3.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**3.2.a — In terms of clarity (clear–ambiguous), which version of the Data Management story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**3.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**3.3.a — In terms of correctness (correct–incorrect), which version of the Data Management story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**3.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**3.4.a — In terms of consistency (consistent–inconsistent), which version of the Data Management story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**3.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_

---

## Page 6 — Story 4 of 7 — Model Feature Preprocessing

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Model Feature Preprocessing Story

Model feature preprocessing should

- M3: Input and output: Use the 87 checked URL features, such as URL length, number of dots and presence of an IP address. Return class, phishing score, model version and explanation.

D14: Data operations and modeling: Standardize URL formats, remove duplicates, compute and encode features and record exclusions. Learn any data-dependent preparation settings from training data only

### Team Y — Model Feature Preprocessing Story

Model feature preprocessing should

- Compare different algorithms and models using the same inputs and data splits
- Build model inputs from the 87 checked URL features defined in the Project M data dictionary.
- Try at most 30 settings per algorithm, including class weights and the decision threshold, on training and validation data only.
- Fix the chosen settings before examining the final test URLs.

**4.1.a — In terms of completeness (complete–incomplete), which version of the Model Feature Preprocessing story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**4.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**4.2.a — In terms of clarity (clear–ambiguous), which version of the Model Feature Preprocessing story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**4.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**4.3.a — In terms of correctness (correct–incorrect), which version of the Model Feature Preprocessing story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**4.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**4.4.a — In terms of consistency (consistent–inconsistent), which version of the Model Feature Preprocessing story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**4.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_

---

## Page 7 — Story 5 of 7 — Model Training & Evaluation

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Model Training & Evaluation Story

Model training & evaluation should

- Compare performance of a baseline (fixed rule), logistic regression, SVM, decision tree and random forest using the same inputs and data splits; leave raw text NN for later, trying at most 30 settings per algorithm.
- Aim for >95% recall and <5% FP rate.
- Fix the decision threshold (the score above which a URL counts as phishing) before testing.
- Keep the dataset version, split IDs, feature code, settings, random seed, exact software versions and container version for each run.
- Classify each URL as “fishing” or “non-fishing”; return class, risk score in [0,1] and up to 3 reasons.
- Keep model unchanged after request; be retrained only monthly or after confirmed quality loss, using only reviewed labels.
- Report recall, FP rate, precision, F1, PR-AUC and the confusion matrix.
- Use the following split for training: 70% of labeled URLs for training, 15% for choosing settings and 15% for final testing. Keep URLs from the same domain in the same part; split by time when dates are reliable.
- Review both FP and FN.
- Limit pilot training time to 2 hours per candidate run on 4 CPU cores and 8 GB RAM and cost to R$1,500/month for serving, storage and monitoring, plus R$500,00/month for retraining; track cost per 1,000 checks.
- Golden dataset: If used, reserve 400 expert-reviewed URLs covering both classes and difficult cases, versioned and excluded from tuning. Use only for final checks; report full-test results too.

### Team Y — Model Training & Evaluation Story

Model training & evaluation should

- On the final test URLs, detect at least 95% of phishing URLs (recall) while wrongly flagging at most 5% of legitimate URLs (false positive rate).
- Fix the decision threshold (the score above which a URL counts as phishing) before testing.

**5.1.a — In terms of completeness (complete–incomplete), which version of the Model Training & Evaluation story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**5.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**5.2.a — In terms of clarity (clear–ambiguous), which version of the Model Training & Evaluation story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**5.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**5.3.a — In terms of correctness (correct–incorrect), which version of the Model Training & Evaluation story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**5.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**5.4.a — In terms of consistency (consistent–inconsistent), which version of the Model Training & Evaluation story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**5.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_

---

## Page 8 — Story 6 of 7 — Model Deployment

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Model Deployment Story

Model deployment should

- Consider the versioning of the artifacts, check for updates, analyse if it has changed or if it is a false positive, then, check for security or privacy issues, ensure that files have below 100mb, do tests for what is needed, and do the deployment

### Team Y — Model Deployment Story

Model deployment should

- Package feature extraction and the approved classification model as a service container that loads the approved model at startup.
- Return the phishing/non-phishing class, phishing risk score, up to three supporting reasons, request status and model version.
- Return at least 95% of complete check-to-display results within two seconds.
- Let users report a wrong result, suggesting the correct class with a short explanation. A reviewer confirms the report before it is used to retrain the model.
- Authenticate requests and validate URL input formats before processing

**6.1.a — In terms of completeness (complete–incomplete), which version of the Model Deployment story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**6.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**6.2.a — In terms of clarity (clear–ambiguous), which version of the Model Deployment story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**6.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**6.3.a — In terms of correctness (correct–incorrect), which version of the Model Deployment story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**6.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**6.4.a — In terms of consistency (consistent–inconsistent), which version of the Model Deployment story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**6.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_

---

## Page 9 — Story 7 of 7 — Model Integration

Read both versions of this story, then answer the questions at the bottom of the page.

### Team X — Model Integration Story

Model integration should

- input and output: Use the 87 checked URL features, such as URL length, number of dots and presence of an IP address. Return class, phishing score, model version and explanation
- Give users timely warnings with understandable reasons, including for phishing URLs not yet on block lists; confirm usefulness with users
- Check every URL the user submits or the proxy intercepts. Reuse a recent result for the same URL only while its features and the model version are unchanged.
- ML owner handles prediction quality; security lead handles warning policy and incidents; application owner handles how results are shown.
- Authenticate requests and protect model files. Run feature extraction isolated, with restricted internet access, and test malformed URLs and URLs crafted to trick the model.
- Combine the model with reviewed allow and block lists. A popular site is not automatically safe; allow list entries need approval, an expiry date and periodic rechecks.

### Team Y — Model Integration Story

Model integration should

- Connect the application or proxy to the service, rules, feature extraction, model and warning.
- Authenticate requests, check input format and return "could not check" rather than silently letting the URL pass.

**7.1.a — In terms of completeness (complete–incomplete), which version of the Model Integration story do you prefer?**

_The story includes the information needed to carry out and accept the work, without relevant omissions._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**7.1.b — Please explain or complement your answer about completeness.** _(Optional)_

> _Long-answer text_

**7.2.a — In terms of clarity (clear–ambiguous), which version of the Model Integration story do you prefer?**

_The story can be understood in only one way, without vague or ambiguous statements._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**7.2.b — Please explain or complement your answer about clarity.** _(Optional)_

> _Long-answer text_

**7.3.a — In terms of correctness (correct–incorrect), which version of the Model Integration story do you prefer?**

_The statements in the story are true for the project and its domain; it states no incorrect facts._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**7.3.b — Please explain or complement your answer about correctness.** _(Optional)_

> _Long-answer text_

**7.4.a — In terms of consistency (consistent–inconsistent), which version of the Model Integration story do you prefer?**

_The statements in the story do not contradict each other or the project context._

- ◯ Team X's version
- ◯ Team Y's version
- ◯ No preference (both are equivalent)

**7.4.b — Please explain or complement your answer about consistency.** _(Optional)_

> _Long-answer text_
