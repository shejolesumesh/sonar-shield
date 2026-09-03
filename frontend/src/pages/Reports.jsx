import { useEffect, useState } from 'react'
import { reportCsvUrl, reportJsonUrl, getReportSummary, friendlyError } from '../services/api'

export default function Reports() {
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getReportSummary().then((r) => setSummary(r.data)).catch((e) => setError(friendlyError(e)))
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Reports &amp; Export</h2>
      {error && <p className="card text-red-400">{error}</p>}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card space-y-3">
          <h3 className="font-semibold">Export detection register</h3>
          <p className="text-sm text-slate-400">
            CSV / JSON exports include every detection with AI labels, prototype risk scores,
            priorities, GPS (when provided), and expert review status.
          </p>
          <div className="flex gap-3">
            <a href={reportCsvUrl} download className="btn-primary no-underline">⬇ CSV</a>
            <a href={reportJsonUrl} download className="btn-secondary no-underline">⬇ JSON</a>
          </div>
        </div>

        <div className="card space-y-3">
          <h3 className="font-semibold">Fleet summary</h3>
          {!summary ? (
            <p className="text-sm text-slate-500">Loading…</p>
          ) : (
            <>
              <p className="text-xs text-slate-500">Generated {summary.generated_at_utc}</p>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <Metric label="Total detections" v={summary.total_rows} />
                <Metric label="Unknown anomalies" v={summary.unknown_anomalies} />
                <Metric label="Expert reviewed" v={summary.reviewed} />
                <Metric label="P1 critical" v={summary.by_priority.P1 ?? 0} />
              </div>
              <ul className="text-sm space-y-1">
                {Object.entries(summary.by_risk_level).map(([lvl, n]) => (
                  <li key={lvl}>{lvl}: <b>{n}</b></li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>

      {summary?.disclaimer && (
        <p className="text-xs text-yellow-400/80 card border-yellow-800">⚠ {summary.disclaimer}</p>
      )}
    </div>
  )
}

function Metric({ label, v }) {
  return (
    <div className="bg-abyss-900 rounded px-3 py-2">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="font-bold text-lg text-sonar-400">{v}</p>
    </div>
  )
}
