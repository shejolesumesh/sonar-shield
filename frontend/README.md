# SONAR-SHIELD Frontend

React 18 + Vite + Tailwind dashboard for the SONAR-SHIELD backend.

## Run

```bash
npm install
npm run dev
```

Open http://localhost:5173. The dev server proxies `/api/*` requests to
`http://localhost:8000` (the FastAPI backend) - see `vite.config.js`.

## Pages

- Dashboard - fleet-wide stats, risk distribution, top priorities
- Sonar Analysis - upload + run detection on a new image
- Detection Details - evidence card + expert review for one detection
- Recovery Priority - full P1-P4 priority queue
- Map / Heatmap - Leaflet map of geolocated detections
- Expert Review - browse/filter detections, confirm/reject/reclassify
- Reports - CSV/JSON export + summary stats
- Model Info - active detector mode, risk formula, model versions
