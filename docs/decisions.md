# Design Decisions

A running log of the significant choices made while building RecoverAI, and why.

### Why Streamlit instead of NiceGUI
Streamlit's built-in charting, dataframes, and multi-page app support let the
whole dashboard be built in pure Python with minimal boilerplate — ideal for
a buildathon timeline where the point is the AI system, not the UI framework.

### Why five separate modules instead of one big pipeline function
Each module (risk, ML, diagnosis, strategy, policy) has a single
responsibility and can be unit-tested, replaced, or reasoned about in
isolation. In particular, keeping the Policy Engine completely separate
from the Strategy Engine is what makes the "AI recommends, policy decides"
safety story credible rather than just a diagram.

### Why Logistic Regression AND Random Forest, not just one
Comparing two structurally different models (linear vs. ensemble) and
picking by ROC-AUC gives genuine ML evidence for the project rather than a
single unvalidated model choice, and produces a real Model Performance page
instead of a stub.

### Why simulate outcomes instead of skipping execution entirely
A system that only *recommends* is a classifier. A system that *executes,
observes an outcome, and updates metrics* is what the brief specifically
asks for. Since no real merchant money is available, outcomes are simulated
using the model's own recovery probability (adjusted per action) — realistic
enough to demonstrate the full loop without touching real payments.

### Why SQLite instead of a file log
SQLite gives structured, queryable audit history (filter by action, outcome,
payment) with zero setup — appropriate for a project meant to run entirely
on a laptop from PyCharm, with no external database dependency.

### Why the LLM/rules layer never touches money directly
This mirrors how real fintech systems are built: models produce signals and
explanations; a separate, auditable, deterministic policy layer makes the
final call. It's also simply safer, and it's explicitly called out in the
brief as the kind of judgment a strong AI project should demonstrate.
