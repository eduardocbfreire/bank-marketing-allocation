# Contact Allocation Under Capacity Constraint

> **Status: in progress.** The data layer, the business framing and the exploratory analysis are in place. The calibrated propensity model, the allocation policy and the results are still being built. The Answer section below is written last, on purpose.

Deciding which clients a capacity-limited contact team should call, using a calibrated propensity model as an input to a constrained optimisation problem rather than as the answer itself.

## Context

A retail bank runs outbound telemarketing campaigns for term deposits. The base is around 41,000 clients and the conversion rate is 11.3%, so most calls end in a no.

The binding problem is not accuracy, it is capacity. The contact team can work through a few thousand clients per campaign window, not the whole base. Somebody has to decide who gets called, and today that decision is made by ranking and gut feeling, with no way to say what it costs to be wrong.

## Business question

> Given a fixed contact budget, which subset of clients should we prioritise to maximise the expected value of the campaign, without systematically abandoning any relevant client segment?

Five questions have to be answered with data, not opinion:

1. Does always calling the highest-probability clients actually maximise return?
2. What happens to expected value if capacity moves by 50% in either direction?
3. Is any client group being systematically excluded by the policy?
4. How reliable is the probability the model produces?
5. Are we prioritising clients who would convert anyway, or clients who convert because of the call?

## Answer

*Analysis in progress.* This section will carry the headline result, the chart comparing the optimised policy against the naive baselines, and the direct answer to each of the five questions above.

## How

Four layers, each one feeding the next. The model is an input to a decision, not the deliverable.

| Layer | What it does | Tools |
| --- | --- | --- |
| Data | Explore and prepare the campaign base | DuckDB, pandas |
| Predictive | Estimate a **calibrated** conversion probability per client | scikit-learn, MLflow |
| Expected value | Convert probability into currency, using conversion value and contact cost | pandas |
| Prescriptive | Choose who to call under capacity and coverage constraints | PuLP |

Two design decisions carry most of the weight.

**Calibration over ranking.** A model that ranks well can still be badly wrong about the level of the probabilities. Ranking is enough to sort a list, but the optimisation layer multiplies probability by money, so a probability of 0.4 has to mean 40%. Evaluation uses PR-AUC and Brier Score rather than ROC-AUC and accuracy.

**Optimisation over top-k.** Taking the top k scores is optimal only when every client costs the same and no other constraint exists. Add a minimum coverage per segment, and the best affordable set is no longer the highest-scoring set.

### Repository structure

```
├── config/params.yaml      # every business assumption, nothing hard-coded
├── data/raw/               # bank-additional-full.csv, 41,188 clients
├── docs/decisions.md       # the decision problem and every technical trade-off
├── notebooks/              # exploration and modelling
├── src/bank_marketing/     # the pipeline as importable, testable functions
├── tests/                  # pytest
└── outputs/figures/        # charts used in the README
```

### Running it

```bash
uv sync --extra dev
uv run jupyter lab
uv run pytest
```

### Roadmap

- [x] Repository, environment, dataset
- [ ] Exploratory analysis and the decision problem written down in `docs/decisions.md`
- [ ] Calibrated propensity model, evaluated with PR-AUC and Brier Score
- [ ] Allocation policy in PuLP, compared against top-k and random, with capacity sensitivity
- [ ] Modular `src/`, FastAPI endpoint, results in this README

## Known limitation, stated up front

The campaign behind this dataset was not randomised. The model therefore measures **propensity**, who is likely to convert, and not the **incremental effect of being called**. A client who would have subscribed anyway looks identical to one who subscribed because of the call. Uplift modelling on a randomised holdout is the natural next step, and the policy should be read with that caveat.

## Data

Moro, S., Rita, P., and Cortez, P. (2014). *Bank Marketing*. UCI Machine Learning Repository. File `bank-additional-full.csv`, 41,188 records, 20 features, 11.3% conversion rate.
