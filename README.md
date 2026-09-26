# Contact Allocation Under Capacity Constraint

> **Status: in progress.** The data layer, the framing and the exploratory analysis are done. The propensity model and the allocation policy are not. Numbers go in the Answer section once there are numbers.

Choosing which clients a phone campaign should call when there is not enough capacity to call everyone.

## Context

A retail bank sells term deposits over the phone. The base in this dataset is 45,211 clients, and 11.7% of them subscribed.

The team making the calls gets through a few thousand clients per campaign, not 45,211. So someone has to pick the list. Today that pick comes from ranking clients on whatever score is available, and nobody can say what a bad pick costs, or which clients never make the list at all.

## Business question

> Given a fixed number of calls, who should be on the list, and what does the campaign earn?

Underneath that:

- Is the highest-probability list also the highest-value list?
- What happens to expected value if capacity moves up or down by half?
- Which client groups does the policy never reach?
- Can the model's probabilities be read as probabilities, or only as a ranking?
- How much of the list would have subscribed without the call?

## Answer

Not yet. The headline number, the comparison against the current approach, and the chart go here.

## How

Four layers, each feeding the next. What comes out at the end is a call list, and the model is one input to it.

| Layer | Job | Tools |
| --- | --- | --- |
| Data | Prepare and explore the campaign base | DuckDB, pandas |
| Predictive | A calibrated conversion probability per client | scikit-learn, MLflow |
| Expected value | Probability into currency, using conversion value and call cost | pandas |
| Prescriptive | Pick the list under capacity and coverage constraints | PuLP |

The probability has to be calibrated and not merely well ranked, because the optimisation multiplies it by money. If the model says 0.4 for a group that converts at 0.1, the budget goes to the wrong people even though the ranking was fine. That is why the evaluation uses PR-AUC and Brier Score instead of accuracy and ROC-AUC.

Taking the top k scores is already optimal when every call costs the same and nothing else constrains the list. Once there is a minimum number of calls per segment, the best affordable list stops being the top of the ranking, and choosing it becomes an integer programming problem.

### Structure

```
├── config/params.yaml      # conversion value, call cost, capacity, coverage floors
├── data/raw/               # bank-full.csv
├── docs/decisions.md       # what was decided and why
├── notebooks/              # exploration and modelling
├── src/bank_marketing/     # the pipeline as importable functions
├── tests/                  # pytest
└── outputs/figures/        # charts used above
```

### Running it

```bash
uv sync --extra dev
uv run jupyter lab
uv run pytest
```

### Still to do

- [x] Repository, environment, dataset
- [x] Exploratory analysis, and the decision problem written into `docs/decisions.md`
- [ ] Calibrated propensity model
- [ ] Allocation policy in PuLP, against top-k and random baselines, with a capacity sensitivity curve
- [ ] Modular `src/`, FastAPI endpoint, results in this README

## What this cannot tell you

The campaign behind this data was not randomised. Everyone in it was contacted, so the model learns who subscribes, and not who subscribes **because** of the call. Those are different questions, and only the second one justifies spending on a call. A client who was going to subscribe anyway looks identical here to one who was persuaded.

Separating them needs a randomised holdout and uplift modelling. That is the obvious next version, and until it exists the policy should be read as prioritisation and not as measured impact.

## Data

Moro, S., Rita, P., and Cortez, P. (2014). *Bank Marketing*. UCI Machine Learning Repository. `bank-full.csv`, 45,211 records, 16 features, 11.7% conversion rate.
