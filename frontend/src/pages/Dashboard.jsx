import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import {
  getHealth, getReportSummary, getPriorityQueue, listDetections, getHeatmap, friendlyError,
} from '../services/api'

export default function Dashboard() {
  const [health, setHealth] = useState(null)
  const [summary, setSummary] = useState(null)
  const [queue, setQueue] = useState([])
  const [recent, setRecent] = useState([])
  const [heatmap, setHeatmap] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.allSettled([
      getHealth(), getReportSummary(), getPriorityQueue(), listDetections({ limit: 6 }), getHeatmap(),
    ]).then(([h, s, q, r, hm]) => {
      if (h.status === 'fulfilled') setHealth(h.value.data)
      else setError(friendlyError(h.reason))
      if (s.status === 'fulfilled') setSummary(s.value.data)
      if (q.status === 'fulfilled') setQueue(q.value.data.slice(0, 5))
      if (r.status === 'fulfilled') setRecent(r.value.data)
      if (hm.status === 'fulfilled') setHeatmap(hm.value.data)
    })
  }, [])

  const levelData = summary
    ? Object.entries(summary.by_risk_level).map(([level, count]) => ({ level, count }))
    : []

  return (
    <div className="space-y-6">
      {error && (
        <div className="card border-red-700 text-red-300 text-sm">
          Backend unreachable - {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title="Detector Mode" value={health?.detector_mode ?? '—'} sub={health?.demo_model ? 'Demo model active' : 'Trained model active'} />
        <StatCard title="Total Detections" value={summary?.total_rows ?? '—'} sub={`${summary?.unknown_anomalies ?? 0} unknown anomalies`} />
        <StatCard title="Expert Reviewed" value={summary?.reviewed ?? '—'} sub="Confirmed / rejected / reclassified" />
        <StatCard title="Map Coverage" value={heatmap?.has_data ? `${heatmap.points.length} pts` : 'None'} sub={heatmap?.has_data ? 'Geolocated detections' : 'No GPS-tagged data yet'} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card">
          <h3 className="font-bold mb-3">Risk Level Distribution</h3>
          {levelData.length === 0 ? (
            <p className="text-sm text-slate-500">No detections yet. Upload a sonar image to begin.</p>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={levelData}>
                <XAxis dataKey="level" stroke="#94a3b8" />
                <YAxis allowDecimals={false} stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#0b2a42', border: 'none' }} />
                <Bar dataKey="count" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card">
          <h3 className="font-bold mb-3 flex items-center justify-between">
            Top Recovery Priorities
            <Link to="/priority" className="text-xs text-sonar-400 hover:underline">View all →</Link>
          </h3>
          {queue.length === 0 ? (
            <p className="text-sm text-slate-500">No pending detections.</p>
          ) : (
            <ul className="space-y-2">
              {queue.map((d) => (
                <li key={d.detection_id} className="flex items-center justify-between text-sm bg-abyss-900 rounded px-3 py-2">
                  <span>{`P${d.priority}`} · {d.object_type}</span>
                  <span className={`badge ${riskBadge(d.risk_level)}`}>{d.risk_level}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="font-bold mb-3 flex items-center justify-between">
          Recent Detections
          <Link to="/review" className="text-xs text-sonar-400 hover:underline">Review →</Link>
        </h3>
        {recent.length === 0 ? (
          <p className="text-sm text-slate-500">Nothing yet - head to Sonar Analysis to upload an image.</p>
        ) : (
          <ul className="space-y-2">
            {recent.map((d) => (
              <li key={d.id} className="flex items-center justify-between text-sm bg-abyss-900 rounded px-3 py-2">
                <Link to={`/detections/${d.id}`} className="hover:text-sonar-400">{d.object_type}</Link>
                <span className="badge bg-abyss-700">Conf {(d.confidence * 100).toFixed(0)}%</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <p className="text-xs text-yellow-400/80">
        ⚠ All risk scores on this page are PROTOTYPE values from transparent formulas and/or a demo
        detector. They are decision-support signals only.
      </p>
    </div>
  )
}

function StatCard({ title, value, sub }) {
  return (
    <div className="card">
      <p className="text-xs uppercase tracking-wide text-slate-500">{title}</p>
      <p className="text-2xl font-bold text-sonar-400 mt-1">{value}</p>
      <p className="text-xs text-slate-500 mt-1">{sub}</p>
    </div>
  )
}

function riskBadge(level) {
  return {
    LOW: 'bg-green-900/60 text-green-300',
    MEDIUM: 'bg-yellow-900/60 text-yellow-300',
    HIGH: 'bg-orange-900/60 text-orange-300',
    CRITICAL: 'bg-red-900/60 text-red-300',
  }[level] || 'bg-abyss-700'
}
