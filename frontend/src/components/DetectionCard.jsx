import { Link } from 'react-router-dom'

const riskColors = {
  LOW: 'bg-green-900/60 text-green-300',
  MEDIUM: 'bg-yellow-900/60 text-yellow-300',
  HIGH: 'bg-orange-900/60 text-orange-300',
  CRITICAL: 'bg-red-900/60 text-red-300',
}

export default function DetectionCard({ det }) {
  return (
    <Link to={`/detections/${det.id}`} className="card block hover:border-sonar-500 transition">
      <div className="flex items-center justify-between mb-2">
        <span className="font-semibold">{det.object_type}</span>
        {det.is_unknown_anomaly && (
          <span className="badge bg-purple-900/60 text-purple-300">LOW CONFIDENCE - REVIEW</span>
        )}
      </div>
      <div className="flex flex-wrap gap-2 text-xs">
        <span className="badge bg-abyss-700">Conf {(det.confidence * 100).toFixed(0)}%</span>
        <span className={`badge ${riskColors[det.risk_level] || 'bg-abyss-700'}`}>
          Risk {det.risk_level}
        </span>
        <span className="badge bg-blue-900/60 text-blue-300">
          P{det.priority}
        </span>
        {det.status !== 'PENDING' && (
          <span className="badge bg-slate-800 text-slate-300">{det.status}</span>
        )}
      </div>
    </Link>
  )
}
