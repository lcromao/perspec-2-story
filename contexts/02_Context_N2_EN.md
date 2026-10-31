# Evaluation context for Pair N2

Pair ID: N2

Project ID: N

Project name: New York City Taxi Trip Duration Regression

Output language: English. Evaluate this pair only. The participant-facing content below reproduces the supplied form from Page 2 onward.

## Page 2 — Project summary and evaluation instructions

In the next seven pages, you will read the seven stories of two specifications written by different agile teams, Team X and Team Y, for the project summarized below. On each page, read both versions of the story and indicate, for each of four quality characteristics, which version you prefer.

Judge each characteristic on its own; the version you prefer in one characteristic may not be the one you prefer in another. The labels X and Y do not identify the authors or how the specifications were produced.

### Project summary — New York City Taxi Trip Duration Regression

User story [US01-N]: As a taxi dispatcher, I want to estimate a New York City ride's duration when the passenger's destination is known at pickup, so that I can communicate an expected arrival time and plan when the vehicle may be available again.

A New York City taxi service wants to estimate trip duration at pickup. The dispatcher supplies the pickup time, origin and passenger-stated destination; the system predicts seconds and displays minutes and expected arrival time. The estimate supports arrival and vehicle planning. This pilot does not choose routes, update estimates during rides or use live traffic.

The offline pilot uses historical Kaggle records of 2016 NYC taxi trips. Actual dropoff locations stand in for destinations stated at pickup; this assumption needs checking with the taxi service. Trip-end time and post-trip transmission fields cannot be used to make a pickup-time prediction. All targets and resource limits are proposed pilot decisions, not achieved results.

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

- Collect the Kaggle New York City Taxi Trip Duration dataset before development begins.
- Use completed historical trips for labeled data. Trip duration is known only after a ride ends; review newly completed trips before monthly updates.
- Record that the source contains 1,458,644 labeled training trips and 625,134 competition test trips without public duration labels. Report counts after cleaning and in every internal split.
- Check required pickup fields and known trip durations. During use, return unavailable when the destination is missing or invalid instead of inventing an arrival estimate.
- Report coverage and exclusions by time, area, airport, distance, and duration. Assess whether old trips and rarely used routes represent current demand.
- Follow competition usage rules, limit storage of precise trip locations, and report results in groups. Use trip IDs only for record and split traceability, never as model inputs or general logs.
- Explain estimate uncertainty and avoid claims about current traffic or full anonymity.
- Load dataset_B before development starts and record its download date, size and class balance.
- Keep varied HTTP and HTTPS URLs. Mark malformed URLs and URLs with unresolved labels so pre-processing can exclude them.
- Add reviewed application URLs and approved PhishTank/Tranco label confirmations once a day. Review user reports within 7 days.
- Keep only features that can be computed within the two-second check budget, including any online queries.

### Team Y — Data Collection Story

Data collection should

- Use the Kaggle New York City Taxi Trip Duration dataset, sampled from 2016 NYC Yellow Cab records originally published by NYC TLC. Retain its version and respect competition usage rules.
- Load historical data before development. Historical data do not describe current traffic.
- Ensure the dataset provides sufficient coverage across different trip times, areas, trip lengths, airports, and weekdays, and document potential gaps or biases
- Review new completed-trip records before using them for monthly offline model updates, since trip duration is only known after the ride is completed

Outcome / acceptance: The required historical dataset is collected and versioned, its source and usage rules are documented, and its coverage and potential biases are assessed. New completed-trip records are reviewed before being included in monthly offline model updates, with the resulting datasets traceable to their source and collection period.

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

- Define pickup_datetime (meter start), dropoff_datetime (trip end, for checking only), trip_duration (seconds), coordinates (latitude/longitude degrees) and passenger_count (driver entry); record the time zone.
- If used, reserve an expert-reviewed part of the final test set covering short/long trips, airports, rush hours and unusual routes. Use only for final checks; report full-test results too
- Order labeled trips by pickup time: first 70% for training, next 15% for choosing settings, last 15% for final testing. Keep duplicates together. Unlabeled Kaggle test.csv cannot measure prediction error.
- Check positive durations, coordinates, passenger counts and agreement between duration and start/end times. Separate doubtful records for review and report exclusions; do not silently shorten extreme trips.
- Use one time interpretation, coordinate order and duration unit. Learn durations in seconds and display minutes; never use trip-end time or post-trip transmission fields as prediction inputs.

### Team Y — Data Pre-processing Story

Data pre-processing should

- Keep completed NYC trips with a positive known duration and valid pickup/dropoff coordinates. Document duplicates, invalid times or locations and trips outside the service area.
- Define pickup_datetime (meter start), dropoff_datetime (trip end, for checking only), trip_duration (seconds), coordinates (latitude/longitude degrees) and passenger_count (driver entry); record the time zone.
- The source has 1,458,644 labeled training trips and 625,134 competition test trips without public duration labels. Report counts after cleaning and in each internal data split.
- Keep trip IDs only to trace records and data splits, not as model inputs or general logs. Limit precise-location storage and report grouped results; do not claim full anonymity.
- Check times and coordinates, remove duplicates, verify durations and record exclusions. Derive distance/time inputs; learn any data-dependent preparation settings from training data only.
- Order labeled trips by pickup time: first 70% for training, next 15% for choosing settings, last 15% for final testing. Keep duplicates together. Unlabeled Kaggle test.csv cannot measure prediction error.
- If used, reserve an expert-reviewed part of the final test set covering short/long trips, airports, rush hours and unusual routes. Use only for final checks; report full-test results too.

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

- Store source data, prepared data, test splits, field definitions, models and reports in controlled storage
- Build model inputs from the 87 features in the data dictionary. The output is the class, a phishing score from 0 to 1, the model version and up to three reasons.
- Encode and scale features as the candidate algorithms need. Fit any data-dependent settings on the training split only.
- Use the same versioned feature code for training and inside the serving container.
- Keep readable feature names so the top features can be shown as reasons, for example "contains an IP address".
- Keep TLD, language and domain age with each record so bias can be checked during evaluation.
- Store URLs and features in restricted file storage, user reports in a database, code in Git and approved models in a model registry.
- Version each dataset release together with its data dictionary, sources, label evidence and reviewer.
- Keep split IDs, feature code, settings, random seed and software and container versions for every run, so any result can be reproduced.
- If a golden dataset is used, keep 400 expert-reviewed URLs, versioned and excluded from tuning, for final checks only.
- Restrict access to full URLs and store only coded user and request identifiers.

### Team Y — Data Management Story

Data management should

- Store source data, cleaned datasets, feature preparation code, models and experiment results in controlled storage, with access restricted according to data sensitivity.
- Maintain the data version, filtering rules, time interpretation, data split, feature preparation code, random settings and software versions for each experiment so that approved results can be reproduced.
- Data Dictionary: Maintain the data dictionary together with each data version, including field definitions, units, coordinate conventions and the time zone used.
- Keep the source dataset version and its origin associated with each data release, including the Kaggle dataset and its NYC TLC origin.
- Restrict access to precise trip locations and avoid including trip IDs or precise locations in general logs.
- Follow competition usage rules and restrict precise trip locations, even without names. Explain estimate uncertainty and avoid claims about current traffic.

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

- Reserve an expert-reviewed part of the final test set covering short/long trips, airports, rush hours and unusual routes. Use only for final checks; report full-test results too.
- Order labeled trips by pickup time: first 70% for training, next 15% for choosing settings, last 15% for final testing. Keep duplicates together.
- Unlabeled Kaggle test.csv should not be used to measure prediction error and be removed from the dataset
- Keep trip IDs only to trace records and data splits, not as model inputs or general logs. Limit precise-location storage and report grouped results; do not claim full anonymity.
- Build inputs only from information known at pickup: pickup time, origin, intended destination and passenger count when known. Never use dropoff_datetime or fields sent after the trip.
- Derive distance between pickup and destination and time inputs (hour, weekday) from those fields. Learn any data-dependent settings on the training split only.
- The target is a positive duration in seconds. Convert to minutes only for display.
- Use the same versioned feature code in training and in the serving service.
- Keep readable input names (distance, pickup hour) so influential inputs can be shown for unusual estimates.
- Keep area, trip length, hour, weekday and airport flags with each record for group error checks.

### Team Y — Model Feature Preprocessing Story

Model feature preprocessing should

- Build the first model using selected available features from Kaggle datasets: pickup time, origin, intended destination and passenger count when known.
- Recover a positive numeric output referring to the expected duration in seconds of the trip, result status and model version.
- Retain selected selected feature values of the model to provide a transparent reasoning result
- Check that transformations preserve agreed features: time, area, airport, distance and duration.

Outcome / acceptance: The feature pipeline accepts the agreed inputs (pickup time, origin, dropoff locations and destination) and returns a positive duration in seconds with explainability feats (reasoning behind the duration, with selected labels)

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

- Check coverage and exclusions by time, area, airport, distance and duration. Old trips and rarely used routes may not represent the taxi service's current demand.
- Use one time interpretation, coordinate order and duration unit. Learn durations in seconds and display minutes; never use trip-end time or post-trip transmission fields as prediction inputs.
- Predict a positive trip duration in seconds from information known at pickup, and return whether an estimate is available.
- Compare linear regression, random forest and gradient boosting on the same inputs and time-ordered splits. Try at most 30 settings per algorithm on training and validation data, then fix settings before the final test.
- Compare against the reference estimate: the median training duration for each distance band (0–2, >2–5, >5–10, >10 km) and pickup-hour band (00–05, 06–11, 12–17, 18–23). Fall back to the overall median when a band has too few trips.
- Require at least 10% lower MAE in minutes than the reference on the final test trips, with no increase in large errors or in underestimates of more than 5 minutes.
- Also report RMSE, RMSLE, P90 error, average over- and underestimate, and the share of trips underestimated by more than 5 minutes.
- Review both error types. Estimates that are too short make passengers late and make taxis look free too soon. Estimates that are too long delay planning and reduce trust.
- Compare errors by area, trip length, hour, weekday and airport trips, and flag groups with few examples. Make no demographic fairness claim.
- Keep each candidate run within 2 hours on 4 CPU cores and 8 GB RAM, and record preparation time and training time separately.

### Team Y — Model Training & Evaluation Story

Model training & evaluation should

- Train and compare linear regression (a simple formula), random forest (combined decision trees) and gradient boosting (trees that improve earlier errors), using the same inputs and data splits.
- Try at most 30 settings per algorithm on training and validation data. Fix the chosen settings before examining the final test trips.
- Check positive durations, coordinates, passenger counts and agreement between duration and start/end times. Separate doubtful records for review and report exclusions; do not silently shorten extreme trips.
- Use the middle training-trip duration for each distance band (0–2, >2–5, >5–10, >10 km) and pickup-hour band (00–05, 06–11, 12–17, 18–23). With too few trips, use the overall training median; compare on the same test trips.
- Guarantee that the evaluation shows a clear and trustable/verifiable reasoning chain behind inference when an estimate shows an unusual result.
- Guarantee that inference time where at least 95% of model-service requests should finish within 500 ms on the reference computer; the full pickup-to-display path must stay within two seconds.

Outcome / acceptance: Documented comparison between chosen potential algorithms and guarantee that the resulting model fits the quality thresholds and explainability criteria.

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

- Ensure the cost does not exceed R$1,500/month for serving, storage and monitoring
- Ensure the retraining cost does not exceed R$500/month for retraining
- Cost is tracked per 1,000 estimates.
- Log request/model version, issue time, response time and status; add error summaries after completed trips. Keep precise locations and trip IDs out of general logs.
- Run the approved model as a service that returns seconds, status and version. If the model fails but the inputs are valid, return the labeled reference estimate.
- 95% of model-service requests should finish within 500 ms, and the full pickup-to-display path within 2 seconds.
- Identify each release by its model, data, input definitions, filters, splits, results and service code. Reject incompatible inputs and keep the last approved release for rollback.
- Review new completed trips weekly. Investigate if average error rises by more than 20% or the model loses its advantage over the reference.

### Team Y — Model Deployment Story

Model deployment should

- I2: Model Serving: Run the approved model as a service and return the predicted duration in seconds, result status and model version. Convert the result to minutes for display.
- M10: Versioning: Identify each deployed release by its model, data, input definitions, filters, splits, results and service code, and retain the last approved release for recovery.
- M7: Inference Time: Ensure at least 95% of model-service requests finish within 500 ms on the reference computer, while the full pickup-to-display path remains within two seconds.
- I5: Monitorability: Monitor missing destinations, invalid inputs, response times, failures and backup use, and review prediction errors after completed trips.
- M9: Performance Degradation: Review new completed trips weekly and investigate when average error increases by more than 20% or the model loses its advantage over the reference estimate.
- I4: Storage: Keep the deployed model and required preparation files in controlled storage and retain the previous approved model for recovery.
- I7: Reproducibility: Keep the data version, filtering rules, feature code, split IDs, random settings and software versions associated with each deployed release.
- I8: Maintainability: Keep input validation, feature preparation, prediction, backup and display components separate and test formats and units.
- M8: Model Size: Keep the model and preparation files below 100 MB and the serving process below 1 GB of memory.
- I6: Telemetry: Log the request/model version, issue time, response time and status, while keeping precise locations and trip IDs out of general logs.
- I11: Cost: Track serving, storage and monitoring costs against the proposed pilot limit of R1,500/month,plusR500/month for retraining.
- M12: Scalability: Test 20 requests per second for the pilot and growth toward 100 requests per second within the proposed budget.

Outcome / acceptance: The deployed model fits the 500ms time limite for 95% requests, guarantee an working monitor for monitoring input and output data and guarantee that model processing uses the memory cap (1GB)

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

- Track missing destinations, invalid inputs, response times, failures and backup use. After trips finish, review errors by time, distance and area.
- Not change the model during a request.
- Ensure retraining is offline monthly or after confirmed quality loss, using checked completed-trip records
- During use, have a missing or invalid destination return unavailable rather than an invented arrival estimate.
- Validate the assumption that the recorded dropoff location is the assumed destination known at pickup with the taxi service before deployment.
- Load historical data before development. Trip duration becomes known only after the ride ends; review new completed-trip records before monthly updates. Historical data do not describe current traffic.
- Connect pickup entry to prediction and display. A missing destination or invalid coordinates returns "unavailable", and a model failure with valid inputs returns the labeled backup estimate.
- Estimate once at pickup, when origin, destination and pickup time are known. Updates during the ride and destination changes are out of scope.
- Show minutes, expected arrival time, issue time and whether the result comes from the model or the backup. State that live traffic is not included.
- The estimate is advice. Dispatchers and drivers decide, and the system does not choose a route or guarantee an arrival time.
- Assign owners: dispatch owner for service decisions, data owner for records, ML owner for prediction quality, and platform owner for failures and recovery.
- Let dispatchers flag an implausible estimate. Check it against the actual completed-trip duration before using it for retraining.
- At least 8 of 10 dispatchers should correctly read the duration, the units, the backup estimate and the missing-destination message in a task-based review.
- Track the pilot goal: 20% fewer reported arrival-planning problems over three months.

Outcome / acceptance: dispatchers get an understandable estimate at pickup, can tell model, backup and unavailable results apart, and keep the final decision.

### Team Y — Model Integration Story

Model integration should

- I9: Integration: Connect the pickup entry to the prediction service and display. Missing destinations or invalid coordinates should return an unavailable result, while valid inputs should produce a model estimate or the labeled backup estimate.
- M3: Input & Output: Accept pickup time, origin, intended destination and passenger count when known, and return the predicted duration in seconds, result status and model version.
- U1: Value: Provide dispatchers with an expected arrival time and support vehicle availability planning.
- U2: Forcefulness: Present the prediction as advice. Dispatchers and drivers remain responsible for decisions, and the system does not select routes or guarantee arrival time
- s.U3: Frequency: Generate one estimate at pickup when the required information is available. Updates during the ride and destination changes are outside the pilot.
- U7: Accountability: Assign service decisions to the dispatch owner, prediction quality to the ML owner, data quality to the data owner and service failures and recovery to the platform owner.
- M14: Security & Privacy: Authenticate prediction requests, validate input formats, protect model files and restrict access to precise trip locations.

Outcome / acceptance: Drivers receive and understandable expected trip duration, that the system can flag and monitor for guaranteeing quality and track output quality and consistency.

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
