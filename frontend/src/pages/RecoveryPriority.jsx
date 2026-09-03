import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getPriorityQueue, friendlyError } from '../services/api'

const prioStyles = {
  1: 'bg-red-900/60 text-red-300',
  2: 'bg-orange-900/60 text-orange-300',
  3: 'bg-yellow-900/60 text-yellow-300',
  4: 'bg-green-900/60 text-green-300',
}

export default function RecoveryPriority() {
  const [items, setItems] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    getPriorityQueue().then((r) => setItems(r.data)).catch((e) => setError(friendlyError(e)))
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Recovery Priority Queue</h2>
      {error && <p className="card text-red-400">{error}</p>}
      {items.length === 0 && !error && (
        <p className="card text-slate-500">
          No pending detections. Upload and analyze sonar imagery first.
        </p>
      )}

      <div className="space-y-3">
        {items.map((d, idx) => {
          const gps = d.latitude != null && d.longitude != null
            ? `${d.latitude}, ${d.longitude}`
            : 'not available'
          return (
            <div key={d.detection_id} className="card flex flex-col md:flex-row md:items-center gap-3 justify-between">
              <div className="flex items-start gap-4">
                <span className={`text-2xl font-black w-14 h-14 flex items-center justify-center rounded ${prioStyles[d.priority]}`}>
                  P{d.priority}
                </span>
                <div>
                  <Link to={`/detections/${d.detection_id}`} className="font-semibold hover:text-sonar-400">
                    #{idx + 1} · {d.object_type}
                  </Link>
                  {d.is_unknown_anomaly && (
                    <span className="badge bg-purple-900/60 text-purple-300 ml-2">LOW CONFIDENCE - REVIEW</span>
                  )}
                  <p className="text-xs text-slate-400 mt-1 max-w-xl">{d.rationale}</p>
                  <p className="text-xs text-slate-500 mt-1">
                    GPS: {gps} · Depth: {d.depth != null ? `${d.depth} m` : 'n/a'}
                  </p>
                </div>
              </div>
              <div className="flex gap-2 text-xs shrink-0">
                <span className="badge bg-abyss-700">Risk {d.risk_score.toFixed(1)}</span>
                <span className="badge bg-abyss-700">Conf {(d.confidence * 100).toFixed(0)}%</span>
                <span className="badge bg-blue-900/60 text-blue-300">{d.risk_level}</span>
              </div>
            </div>
          )
        })}
      </div>

      <p className="text-xs text-yellow-400/80">
        ⚠ Priority ordering derives from the prototype risk formula and demo detector output.
        Field teams should validate before committing recovery resources.
      </p>
    </div>
  )
}
