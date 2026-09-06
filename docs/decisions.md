# Decision log

The reasoning behind the project. Written for a reader who has to trust the
output without reading the code. Every entry states what was decided, why, and
what it would take to change the decision.

## 1. The decision problem

*Stated without the word "model", so that a reader who does not build models
can still check whether the framing is right.*

**Decision variable.**
For each client i, a binary choice: contact, or do not contact.

**Objective function.**

**Constraints.**

**Value assumptions.**

| Assumption | Value | Why it is defensible |
| --- | --- | --- |
| Value of one conversion | | |
| Cost of one contact | | |
| Contact capacity | | |

**Who decides this today, and how.**

**Cost of being wrong.**

## 2. Data decisions

**Leakage.** `duration` is excluded from the feature set. It is the call length
in seconds, so it only exists after the call has happened and cannot inform the
decision of who to call. It is listed in `config/params.yaml` under
`data.leakage_columns`.

**Missing values.**

**`pdays = 999`.**

## 3. Modelling decisions

*Pending.*

## 4. Optimisation decisions

*Pending.*

## 5. Limitations

**Causality.** The campaign was not randomised, so the model estimates
propensity and not the incremental effect of the contact. Uplift modelling on a
randomised holdout is the stated next step.

