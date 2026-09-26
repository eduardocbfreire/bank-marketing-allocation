# Decision log

The reasoning behind the project. Written for a reader who has to trust the
output without reading the code. Every entry states what was decided, why, and
what it would take to change the decision.

## 1. The decision problem

*Stated without the word "model", so that a reader who does not build models
can still check whether the framing is right.*

**The question.**
Given a fixed number of calls, who should be on the list, and what does the
campaign earn? The questions underneath it are in the README.

**Decision variable.**
For each client i, a binary choice: contact, or do not contact.

x_i = 1 if client i is on the call list, 0 if not.

**Objective function.**
Maximise the expected value of the campaign:

```
maximise  sum over i of  x_i * (p_i * V - C)
```

- p_i is the calibrated probability that client i subscribes if called
- V is the value of one conversion
- C is the cost of one call

A call only pays off when p_i * V is bigger than C. With the current values
that means p_i above 5%. The base rate is 11.7%, so the average client is
already worth calling. The problem is choosing the best ones inside the
capacity.

**Constraints.**

1. Capacity: the list can't be longer than the calls the team can make.
   `sum of x_i <= N`, with N = 3,000.
2. Coverage: every job group gets at least 2% of the calls, so no group is left
   out of the list. With 12 job groups that is at least 60 calls each, 720
   calls in total (24% of the capacity). The smallest group ("unknown", 288
   clients) still has enough clients to fill its 60.
3. Each x_i is 0 or 1. A client is called or not, there is no half call.

Without constraint 2, taking the top N by p_i * V - C is already the best list.
Constraint 2 is what turns this into an integer programming problem.

**Value assumptions.**

| Assumption | Value | Why it is defensible |
| --- | --- | --- |
| Value of one conversion | 100 EUR | Placeholder. It needs a real number from the business, like the margin of a term deposit over its life. What matters most is the ratio with the call cost. |
| Cost of one contact | 5 EUR | Placeholder. Agent time plus telephony for one call. At 100 EUR per conversion it puts the break even probability at 5%. |
| Contact capacity | 3,000 calls per campaign | "A few thousand" calls per campaign, as the team works today. It is tested from 0.5x to 2x, because this number moves the answer the most. |

All values live in `config/params.yaml`. Changing one of them re-runs the whole
pipeline without touching the code.

**Who decides this today, and how.**
Today the list comes from ranking clients on whatever score is available.
Nobody can say what a bad pick costs, or which clients never make the list at
all.

The floor to beat is a random list: 3,000 random calls give about 351
conversions and an expected value of about 20,095 EUR.

**Cost of being wrong.**
The two errors don't cost the same.

- Calling a client who doesn't subscribe wastes one call: 5 EUR.
- Not calling a client who would subscribe loses the conversion minus the call:
  95 EUR.

Missing a buyer costs 19 times more than a wasted call. There is also a cost
that doesn't show in money: a list that always leaves the same groups out.
That is why the coverage constraint exists.

## 2. Data decisions

**Dataset.** `bank-full.csv`: 45,211 clients, 16 columns plus the target,
11.7% conversion. It has no economic context columns, so the economy is an
unobserved cause in the DAG.

**Leakage.** `duration` is excluded from the feature set. It is the call length
in seconds, so it only exists after the call has happened and cannot inform the
decision of who to call. It is listed in `config/params.yaml` under
`data.leakage_columns`.

`day`, `month` and `campaign` are also out of the causal DAG. They describe the
calls of this campaign and not the client, so they are not known when the list
is built.

**Missing values.** There are no nulls. Some columns use "unknown" as a
category: `job` (288), `education` (1,857), `contact` (13,020) and `poutcome`
(36,959). "Unknown" stays as its own category, because in `contact` it
converts at only 4.1% and that difference is information.

**`pdays = -1`.** In this dataset -1 means the client was never contacted
before. That is 36,954 clients (82%), the same ones with `previous = 0` and
`poutcome = "unknown"`. The three columns repeat each other, so only `poutcome`
goes into the causal discovery.

## 3. Modelling decisions

*Pending.*

## 4. Optimisation decisions

*Pending.*

## 5. Limitations

**Causality.** The campaign was not randomised, so the model estimates
propensity and not the incremental effect of the contact. Uplift modelling on a
randomised holdout is the stated next step.
