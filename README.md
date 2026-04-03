# Pittsburgh Restaurant Health Score

A data analytics dashboard scoring 362 independent Pittsburgh 
restaurants on business health using live Google Places API data.

## Live Dashboard
[View the app](https://pittsburgh-restaurant-health.streamlit.app)

## Why I Built This
Restaurant technology platforms need to identify which independent 
restaurants are thriving (acquisition targets) and which are at-risk 
(retention priorities). This tool does exactly that.

## Methodology
Five weighted components build each restaurant's Health Score:
| Component | Weight | Rationale |
|---|---|---|
| Popularity Score | 30% | Neighborhood-normalized review volume |
| Rating Score | 30% | Aggressive bucketing to reward quality |
| Price Competitiveness | 15% | Mid-range pricing scores highest |
| Neighborhood Dominance | 15% | Review share vs local average |
| Recency Score | 10% | How recently customers left reviews |

## Tech Stack
Python · Google Places API · Pandas · Streamlit · Plotly

## Disclaimer
This is an independent analytical portfolio project. Scores are 
derived from publicly available Google Places data and do not 
represent any official assessment of restaurant quality or viability.
