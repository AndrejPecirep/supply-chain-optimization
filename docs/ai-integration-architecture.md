# AI Integration Architecture

## Components

1. Demand Forecasting Model - predicts SKU-level demand for the next 30-90 days.
2. Supplier Risk Agent - extracts contract terms and combines them with operational supplier KPIs.
3. Document Parser - converts manifests and scanned shipping documents into JSON.
4. Human-in-the-loop - high-risk findings must be reviewed by procurement/legal before action.

## Ethics and controls

- AI output is advisory, not an automatic legal or procurement decision.
- Risk scores include source data and explanations.
- High-risk suppliers require manager review.
- Contract analysis must not replace legal counsel.
