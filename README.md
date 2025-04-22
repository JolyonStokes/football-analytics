# ⚽ Football Data Analytics Portfolio

Welcome to my football analytics portfolio — a collection of club-specific data science projects using event-level data to uncover performance insights.

Each folder represents an independent analysis, using modern data science practices and football-specific techniques like xG models, simulations, and visual storytelling.

---

## 📁 Project Index

### 🔴 Bayer Leverkusen – 2023/24 xPts Model
📂 [`/leverkusen_analysis`](./leverkusen_analysis)

A match-by-match **expected points (xPts)** model using **Monte Carlo simulation** based on StatsBomb's open event data for Bayer Leverkusen's 2023/24 Bundesliga season.

- Shot-by-shot xG simulation
- xPts vs actual points over the season
- Rolling performance visualization
- Built using `statsbombpy`, `pandas`, and `matplotlib`

➡️ Aimed at identifying **over/underperformance** and variance in results based on shot quality.

---

### ⚽ **Norwich City – xPts Simulation & Rolling xG Analysis**
- Simulates **expected points (xPts)** for each match using a **shot-by-shot Monte Carlo model**
- Compares xPts to actual points earned to assess **over- or under-performance**
- Plots **rolling xG averages** (xGF and xGA) with contextual annotations (e.g., injuries, suspensions)
- Tools: `numpy`, `pandas`, `matplotlib`, `scipy`

> 📊 *Insight: Norwich began the season creating plenty of chances but leaking goals. Mid-season, attacking output dropped with a tightening of defensive structure — likely due to key attacking absences.*
> - *Full post season analysis coming soon with Medium article*

---

### 🎯 **Ante Crnac – Shot Profile & Comparative Analysis**
- Compares his output to **other Championship forwards in his age bracket**
- - Considering his lack of experience in the championship and periods in and out of the team, he has strong goal scoring and npxG/90 numbers.
- - At the time of writing he is joint top scorer among those U22 (7 goals) despite taking 1.25 fewer shots per 90 than joint top (U22) scorer Mayenda.
- - Only 3 have a better npxG/shot ratio. With a more solidifed role/position within the squad, he has shown promise of an impressive output next season.

---

### 🕸️ **Player Radars – Performance Archetypes**
- Builds radar charts for selected players using key metrics
- - Comparison of Sargent and Sainz this season against last season.
  - Sainz has built on a promising 2023/24 season with an immense goal scoring season.
  - Sargent has supplemented his scoring output with some top creative output, perhaps facilitating the increase in performance of Sainz this season.
- 

---

## 📦 Tools & Libraries Used
- `pandas` / `numpy` — data wrangling and modeling
- `matplotlib` — static visuals and custom plots
- `scipy` — smoothing (Savitzky-Golay)
- `PIL` — for badge/logo integration
- Git for version control

---

## 🧰 In Progress
- Each current project is in progress with new analysis coming soon.

---

## 📬 Contact
👤 [Jolyon Stokes](https://github.com/JolyonStokes)  
🧠 Always open to feedback, collaboration or roles in data analytics and football performance.
Check out my bluesky @jolyonstokes.bsky.social for more commentary

---
## 📄 License
MIT License — feel free to fork, adapt, and build upon this work with credit.
---
