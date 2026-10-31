# Evaluation context for Pair N1

Pair ID: N1

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

- Use the Kaggle New York City Taxi Trip Duration dataset, sampled from 2016 NYC Yellow Cab records originally published by NYC TLC. Retain its version and respect competition usage rules.
- Only collect data for the last 2 years. If there isn't enough data, expand the time window by 2 years.
- Keep rows with a positive known duration and valid pickup/dropoff coordinates.
- Drop duplicates and rows with invalid times or locations and trips outside the service area.
- Document the number of remaining rows after the two previous steps.

### Team Y — Data Collection Story

Data collection should

- Use the Kaggle New York City Taxi Trip Duration dataset, sampled from 2016 NYC Yellow Cab records originally published by NYC TLC; retain its version and respect the competition usage rules.
- Load historical data before development; trip duration is known only after the ride ends, so review new completed-trip records before each monthly update; note that historical data do not describe current traffic.
- Keep completed NYC trips with a positive known duration and valid pickup/dropoff coordinates; document duplicates, invalid times or locations and trips outside the service area.
- Collect 1,458,644 labeled training trips and 625,134 competition test trips without public duration labels; report counts after cleaning and in each internal data split.
- Use real completed taxi trips, with the recorded dropoff location as the assumed destination known at pickup; validate this assumption with the taxi service before deployment.

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
- Check positive durations, coordinates, passenger counts and agreement between duration and start/end times. Separate doubtful records for review and report exclusions; do not silently shorten extreme trips.
- Check required pickup fields and known trip durations. During use, a missing or invalid destination must return unavailable rather than an invented arrival estimate.
- Use one time interpretation, coordinate order and duration unit. Learn durations in seconds and display minutes; never use trip-end time or post-trip transmission fields as prediction inputs.

### Team Y — Data Pre-processing Story

Data pre-processing should

- Define pickup_datetime (meter start), dropoff_datetime (trip end, for checking only), trip_duration (seconds), coordinates (latitude/longitude degrees) and passenger_count (driver entry); record the time zone.
- Check positive durations, coordinates, passenger counts and agreement between duration and start/end times; separate doubtful records for review and report exclusions, without silently shortening extreme trips.
- Check required pickup fields (pickup time, origin, destination) and known trip durations; document gaps, since in use a missing or invalid destination must return "unavailable" rather than an invented estimate.
- Use one time interpretation, coordinate order and duration unit; learn durations in seconds and display minutes; never use trip-end time or post-trip transmission fields as prediction inputs.
- Check times and coordinates, remove duplicates, verify durations and record exclusions; derive distance and time inputs; learn any data-dependent preparation settings from training data only.
- Order labeled trips by pickup time: first 70% for training, next 15% for choosing settings and last 15% for final testing; keep duplicates together; note that the unlabeled Kaggle test.csv cannot measure prediction error.
- Keep a record of the NYC TLC origin, Kaggle sampling and cleaning, and usage rules; note that the public files do not prove full record history.
- Golden dataset: If used, reserve an expert-reviewed part of the final test set covering short/long trips, airports, rush hours and unusual routes.

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

- Keep trip IDs only to trace records and data splits, not as model inputs or general logs. Limit precise-location storage and report grouped results; do not claim full anonymity.

### Team Y — Data Management Story

Data management should

- Define pickup_datetime (meter start), dropoff_datetime (trip end, for checking only), trip_duration (seconds), coordinates (latitude/longitude degrees) and passenger_count (driver entry); record the time zone.
- Check coverage and exclusions by time, area, airport, distance and duration. Old trips and rarely used routes may not represent the taxi service's current demand.
- Follow competition usage rules and restrict precise trip locations, even without names. Explain estimate uncertainty and avoid claims about current traffic.
- Keep trip IDs only to trace records and data splits, not as model inputs or general logs. Limit precise-location storage and report grouped results; do not claim full anonymity.
- Bias and fairness: Compare average error, large errors and over/underestimates by area, trip length, hour, weekday and airport trips. Flag groups with few examples; make no demographic fairness claim.
- Security and privacy: Check coordinates and input format, authenticate requests, protect model files and restrict precise locations. Reject malformed requests and keep diagnostic data only as needed.
- Golden dataset: If used, reserve an expert-reviewed part of the final test set covering short/long trips, airports, rush hours and unusual routes.

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

- Build model inputs only from information available when the trip-duration request is made at pickup.
- Use pickup time, origin, intended destination and passenger count when known.
- Use the recorded historical drop-off coordinates only as the offline proxy for the intended destination assumed to have been supplied at pickup.
- Derive distance-related features from pickup and destination coordinates.
- Derive time-related features from pickup time.
- Apply one consistent coordinate ordering and time interpretation during training and inference.
- Keep trip duration measured internally in seconds.

### Team Y — Model Feature Preprocessing Story

Model feature preprocessing should

- recover pickup_datetime (meter start), dropoff_datetime (trip end, for checking only), trip_duration (seconds), coordinates (latitude/longitude degrees) and passenger_count (driver entry); record the time zone.
- evaluate Use pickup time, origin, intended destination and passenger count when known. Return positive duration in seconds, result status and model version.
- Identify unusual estimates, show which inputs influenced the result, such as distance and pickup hour. These associations do not prove traffic conditions or causes.

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

- Train regression models that predict a positive trip duration in seconds.
- Compare linear regression, random forest and gradient boosting using the same input variables and data partitions.
- Use the first 70% of chronologically ordered labeled trips for model training.
- Use the next 15% for model and parameter selection.
- Keep the final 15% unchanged for final evaluation.
- Try at most 30 parameter settings per candidate algorithm using only training and validation data.
- Fix the selected algorithm and settings before examining the final test trips.
- Use Mean Absolute Error in minutes as the primary model-quality measure.

Outcome / acceptance: A reproducible comparison of linear regression, random forest and gradient boosting against the fixed distance-and-time reference estimate identifies a model that reduces final-test MAE by at least 10% without worsening important large-error or severe-underestimation measures and reports all required secondary metrics and subgroup analyses.

### Team Y — Model Training & Evaluation Story

Model training & evaluation should

- Use pickup time, origin, intended destination and passenger count when known. Return positive duration in seconds, result status and model version.
- Not change the model during a request; instead retrain offline monthly or after confirmed quality loss, using checked completed-trip records.
- Keep test splits and models in controlled storage; Keep the data version, filtering rules, time interpretation, split IDs, feature code, random settings, software versions and reference estimate for each run.
- Compare a baseline model (middle training-trip duration for each distance band and pickup-hour band), linear regression, random forest and gradient boosting, using the same inputs and data splits, trying at most 30 settings per algorithm on training and validation data.
- Use pickup time, origin, intended destination and passenger count when known. Return positive duration in seconds, result status and model version.
- Limit learning time to two hours per candidate run on four CPU cores and 8 GB RAM on the pilot.
- Limit model + preparation files to <100 MB in pilot.
- Record data preparation and training time separately.
- Measure performance on MAE and model size (bytes), report RMSE, RMSLE, P90, average over/underestimate and the share underestimated by over 5min.
- Require at least 95% of model-service requests finish within 500 ms on the reference computer; the full pickup-to-display path must stay within two seconds.
- Compare and balance average error, large errors and over/underestimates by area, trip length, hour, weekday and airport trips. Flag groups with few examples; make no demographic fairness claim. An improvement on short trips must not hide poorer results on important trip groups.
- For unusual estimates, show which inputs influenced the result, such as distance and pickup hour. These associations do not prove traffic conditions or causes.
- Derive distance/time inputs; learn any data-dependent preparation settings from training data only.
- Splits: Order labeled trips by pickup time: first 70% for training, next 15% for choosing settings, last 15% for final testing. Keep duplicates together. Unlabeled Kaggle test.csv cannot measure prediction error.
- Golden dataset: If used, reserve an expert-reviewed part of the final test set covering short/long trips, airports, rush hours and unusual routes. Use only for final checks; report full-test results too.

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

- Run the approved model as a service. Return seconds, status and version; convert to minutes for display. If the model fails but inputs are valid, use the simple reference estimate.

### Team Y — Model Deployment Story

Model deployment should

- Consider the best track from point A to B, check for traffic conditions or any eventual accidents on the path, calculate the time to do this track and the cost, check for security and privacy concerns, then, do the deployment, or apply the Algorithm and go from A to B by taxi.
- Identify each release by its model, data, input definitions, filters, splits, results and service code. Reject incompatible inputs and retain the last approved release.
- I2: Model serving: Run the approved model as a service. Return seconds, status and version; convert to minutes for display. If the model fails but inputs are valid, use the simple reference estimate

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

- Connect pickup entry to prediction and display. Missing destination or invalid coordinates returns unavailable; model failure with valid inputs uses the labeled backup estimate.

### Team Y — Model Integration Story

Model integration should

- Call the service once at pickup, when the dispatcher enters the pickup time, origin and passenger-stated destination; destination changes and updates during the ride are outside the pilot.
- Predict a positive trip duration in seconds from information known at pickup; return the estimate and whether it is available.
- Run the approved model as a service. Return seconds, status and version; convert to minutes for display. If the model fails but inputs are valid, use the simple reference estimate.
- Inference time: At least 95% of model-service requests should finish within 500 ms on the reference computer; the full pickup-to-display path must stay within two seconds.

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
