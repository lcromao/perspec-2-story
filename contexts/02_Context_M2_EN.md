# Evaluation context for Pair M2

Pair ID: M2

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

- Recover Mendeley datasets with balanced URLs
- Include and verify the provided 87 features
- Add URLs reviewed from the application and verify labels using PhishTank and Tranco
- Check coverage of phishing/non-phishing classes, languages, TLDs and domain ages

Outcome / acceptance: The full set of PhishTank and Tranco URLs with validated data

### Team Y — Data Collection Story

Data collection should

- Import Mendeley dataset_B version 3: 11,430 URLs, evenly split between phishing and legitimate, with 87 features collected in May 2020.
- Collect additional candidate URLs from PhishTank and Tranco, recording the source, collection date, and number obtained.
- Give every record an ID and label; record the label’s evidence, date, source, and reviewer. Treat reports and popularity lists as evidence requiring verification.
- Check and document coverage by class, source, URL form, language, TLD, domain age, and reachability, including missing groups and fields.
- Compare the 2020 data with recent application URLs before deployment, especially phishing prevalence and feature distributions.
- Use only sources whose terms permit this use. Protect private browsing data and never ask users to open suspicious URLs.
- Replace user and request identifiers with codes and remove secrets from URLs while retaining information needed for approved features.
- Standardize URLs, remove duplicates, compute and encode features, and record exclusions. Learn data-dependent preparation settings from training data only.
- Review features for clues that reveal a record’s source or labeling process instead of characteristics available when classifying a URL.
- Load dataset_B before development starts and record its download date, size and class balance.
- Keep varied HTTP and HTTPS URLs. Mark malformed URLs and URLs with unresolved labels so pre-processing can exclude them.
- Add reviewed application URLs and approved PhishTank/Tranco label confirmations once a day. Review user reports within 7 days.
- Keep only features that can be computed within the two-second check budget, including any online queries.

Outcome / acceptance: dataset_B is loaded with recorded counts, coverage and gaps. The daily update and the 7-day report review are defined.

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

- Setup-data-environment : Store source data, datasets, models, scripts
- Clear data and anonymize sensitive data
- Setup data dictionary with provided features
- Manually review 10% of records and check the feature extraction is correct
- Treat missing data by excluding empty results and results with empty target labels
- Guarantee a balanced proportion between labels (malicious/non-malicious)
- Split test and train data on 15 final testing, 70 training and 15 settings

Outcome / acceptance: Three datasets split in the 80/15/15 proportion, target labels dictionary, no data with missing target labels.

### Team Y — Data Pre-processing Story

Data pre-processing should

- Make sure ingested URLs are not malformed
- Make sure URLs with unresolved labels are not included
- Make sure features that cannot be computed at check time are not included
- Remove the URL index column
- Write a data dictionary for all 87 features: meaning, type, how it is computed, unit, missing-value code and whether it is available at check time. Label: 0 = non-phishing, 1 = phishing.
- Manually review 10% of records from both classes to check feature extraction and labels. Keep unresolved records separate and report exclusions.
- Use one versioned feature definition for training and use. Keep upper and lower case in URL paths unchanged.
- Split labeled URLs 70/15/15 into training, validation and test. Keep URLs from the same domain in the same part, and split by time when dates are reliable.
- Report record counts by class after cleaning and in each split.

Outcome / acceptance: the prepared dataset has a complete dictionary, documented exclusions, a domain-grouped 70/15/15 split and counts for each part.

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

- Store URLs, feature and related data in restricted storage, user reports, in database, code in Git and approved models in a model registry
- Track each database, including the data source, feature-extraction code, configuration and software environment.
- Preserve the data splits, features definitions , random seed and experiment setting so results can be reproduced.
- Maintain the expert-reviewed Golden Dataset separately and exclude it from model tuning, using it only for final checks,
- Review newly collected urls and confirmed labels before using them for offline model retraining
- Protect stored urls and user information, restrict access, and keep the feature extraction, prediction and warning components maintainable and properly documented.
- Test automatically before each release, first release a new model to a small share of users and retain the previous approved model for recovery.

### Team Y — Data Management Story

Data management should

- Retain the original dataset for auditing and tracing data transformation
- Describe each of the 87 features: meaning, type, how it is computed, unit, missing value code and whether it is available at check time. Label: 0 = non-phishing, 1 = phishing
- Store URLs and features in restricted file storage, user reports in a database, code in Git and approved models in a model registry.
- Version each dataset release together with its data dictionary, sources, label evidence and reviewer.
- Keep split IDs, feature code, settings, random seed and software and container versions for every run, so any result can be reproduced.
- if a golden dataset is used, keep 400 expert-reviewed URLs, versioned and excluded from tuning, for final checks only.
- Restrict access to full URLs and store only coded user and request identifiers.

Outcome / acceptance: every release and every run can be located and reproduced from stored data, splits, code and versions.

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

- Use the 87 url features, including url length, number of dots and presence of an ip address
- Standardize and encode the features consistently between training and model interference
- Learn any data dependent preprocessing setting only from the training data to avoid data leakage.
- Exclude malformed urls, unresolved labels and features that cannot be computed.
- Record the feature definitions, preprocessing steps and settings used for each model version
- Ensure the same feature extraction process is used during training and production inference

### Team Y — Model Feature Preprocessing Story

Model feature preprocessing should

- Split 70% of labeled URLs for training, 15% for choosing settings and 15% for final testing
- Use the 87 checked URL features, such as URL length, number of dots and presence of an IP address. Return class, phishing score, model version and explanation.
- Standardize URL formats, remove duplicates, compute and encode features and record exclusions. Learn any data-dependent preparation settings from training data only.
- Build model inputs from the 87 features in the data dictionary. The output is the class, a phishing score from 0 to 1, the model version and up to three reasons.
- Encode and scale features as the candidate algorithms need. Fit any data-dependent settings on the training split only.
- Use the same versioned feature code for training and inside the serving container.
- Keep readable feature names so the top features can be shown as reasons, for example "contains an IP address".
- Keep TLD, language and domain age with each record so bias can be checked during evaluation.

Outcome / acceptance: the feature pipeline gives the same inputs for training and serving, and those inputs can be explained.

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

- Train and compare logistic regression (a simple weighted formula), SVM (a boundary separating the two classes), decision tree (a sequence of yes/no questions) and random forest (combined decision trees), using the same inputs and data splits.
- Try at most 30 settings per algorithm, including class weights and the decision threshold, on training and validation data only. Fix the chosen settings before examining the final test URLs.
- Review newly confirmed URLs weekly. Investigate if recall falls below 95% or false positive rate exceeds 5% on at least 200 reviewed URLs, and report how uncertain these figures are; changed inputs alone do not prove poorer predictions.

### Team Y — Model Training & Evaluation Story

Model training & evaluation should

- Focus on phishing URL detection
- Determine a decision threshold (the score above which a URL counts as phishing) before testing.
- Ensure the model shows up to three reasons based on the features that most influenced the result, such as "contains an IP address

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

- Run feature extraction and the approved model as one package service that loads the model at startup and returns the class, risk score, reasons, status and the model version
- Connect the application or proxy to the service, authenticate requests, validate inputs.
- Track missing features, changes in input patterns (drift), share of URLs flagged, extraction errors, timeouts and response time. After review, compare results with confirmed labels.
- Test 20 requests per second for the pilot and growth to 100 by adding service copies within budget. Report whether feature extraction limits the speed.

### Team Y — Model Deployment Story

Model deployment should

- Make sure the model has serving process using less than 1 GB of memory, preferring the smaller model when quality is equivalent.
- Ensure feature extraction (computing the 87 URL features) and the approved model are one packaged service (container)
- Track missing features, changes in input patterns (drift), share of URLs flagged, extraction errors, timeouts and response time. After review, compare results with confirmed labels.
- Log request ID, model version, response time, score, warning shown, user override and feedback. Keep full URLs out of general logs, since they may reveal private browsing.
- 95% of model predictions should finish within 100 ms, not counting feature extraction. The full path from check to display should stay within 2 seconds.
- Fix the Python, library and container versions for each release. Test compatibility before updates and keep the last approved release for rollback.
- Review confirmed URLs weekly. Investigate if recall falls below 95% or the false positive rate goes above 5% on at least 200 reviewed URLs. Retrain offline monthly or after a confirmed quality loss.
- Authenticate requests and protect model files. Run feature extraction in isolation with restricted internet access, and test malformed URLs and URLs designed to trick the model.
- Run automated tests before each release, and release a new model to a small share of users first.
- Load-test at 20 requests per second and show growth to 100 by adding service copies. Keep serving, storage and monitoring within R$1,500/month.

Outcome / acceptance: the service meets the latency limits, can roll back to the previous release, detects quality loss and passes the security tests within budget.

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

- Create a front-facing artifact for URL submission and request Classifier API for labelling
- Create a request interceptor for the navigation and request classifier API for labelling
- In the labelling classifier API recover the query URL and run into the classification model
- Return the label to the user, IF the URL is labelled as phishing, request the user input choice for going forward into the Likely phishing URL
- Show up to three reasons based on the features that most influenced the result, such as "contains an IP address". These reasons are evidence, not proof that a URL is phishing.

Outcome / acceptance: Users receive the URL classification with the reasoning and let the user handle the URL access decision in the case of likely phishing URL

### Team Y — Model Integration Story

Model integration should

- Connect the application or proxy to the service, rules, feature extraction, model and warning. Authenticate requests, check input format and return "could not check" rather than silently letting the URL pass.
- Use the 87 checked URL features, such as URL length, number of dots and presence of an IP address. Return class, phishing score, model version and explanation.
- Give users timely warnings with understandable reasons, including for phishing URLs not yet on block lists; confirm usefulness with users.
- The warning is advice. The system recommends avoiding a phishing URL, but the user makes the final decision; the system does not block navigation.
- ML owner handles prediction quality; security lead handles warning policy and incidents; application owner handles how results are shown.
- Authenticate requests and protect model files. Run feature extraction isolated, with restricted internet access, and test malformed URLs and URLs crafted to trick the model.
- Check every URL the user submits or the proxy intercepts. Reuse a recent result only while the URL's features and the model version are unchanged.
- Show the URL, class, risk score, up to three reasons and the check time. Show "could not check" as clearly different from "non-phishing".
- Let users report a wrong result with the class they think is correct and a reason. A reviewer confirms the report before it is used for retraining.
- Combine the model with reviewed allow and block lists. Allow-list entries need approval, an expiry date and periodic rechecks.
- Provide short examples of what a warning means, and state that "non-phishing" does not guarantee a page is safe. At least 8 of 10 users should read the warning correctly in a task-based review.
- Track the pilot goal: 20% fewer confirmed phishing incidents per 1,000 checks over three months.

Outcome / acceptance: users get an understandable, non-blocking warning before navigation, can dispute it, and make the final decision.

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
