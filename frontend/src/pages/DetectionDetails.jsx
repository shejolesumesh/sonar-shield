import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import EvidenceCard from '../components/EvidenceCard'
import ReviewPanel from '../components/ReviewPanel'
import { getDetection, friendlyError } from '../services/api'

const riskColors = {
  LOW: 'bg-green-900/60 text-green-300',
  MEDIUM: 'bg-yellow-900/60 text-yellow-300',
  HIGH: 'bg-orange-900/60 text-orange-300',
  CRITICAL: 'bg-red-900/60 text-red-300',
}

export default function DetectionDetails() {
  const { id } = useParams()
  const [det, setDet] = useState(null)
  const [error, setError] = useState('')

  function reload() {
    getDetection(id).then((r) => setDet(r.data)).catch((e) => setError(friendlyError(e)))
  }

  useEffect(() => { reload() }, [id])

  if (error) return <p className="text-red-400 card">{error}</p>
  if (!det) return <p className="text-slate-500">Loading…</p>

  const gps = det.latitude != null && det.longitude != null
    ? `${det.latitude}, ${det.longitude}`
    : 'Not provided'

  return (
    <div className="space-y-6">
      <Link to="/review" className="text-sm text-sonar-400 hover:underline">← Back to Expert Review</Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card space-y-4">
          <h2 className="text-lg font-bold">{det.object_type}</h2>
          <div className="flex flex-wrap gap-2 text-xs">
            <span className={`badge ${riskColors[det.risk_level]}`}>Risk {det.risk_level} · {det.risk_score.toFixed(1)}</span>
            <span className="badge bg-blue-900/60 text-blue-300">P{det.priority}</span>
            <span className="badge bg-abyss-700">Conf {(det.confidence * 100).toFixed(0)}%</span>
            {det.is_unknown_anomaly && <span className="badge bg-purple-900/60 text-purple-300">LOW CONFIDENCE - REVIEW</span>}
            <span className="badge bg-slate-800">{det.status}</span>
          </div>

          <dl className="text-sm space-y-1 text-slate-300">
            <Row k="Raw detector label" v={det.raw_label} />
            <Row k="Model version" v={det.model_version} />
            <Row k="Severity score" v={det.severity_score.toFixed(1)} />
            <Row k="Location factor" v={det.location_factor.toFixed(1)} />
            <Row k="Estimated size" v={det.estimated_size_m2 != null ? `${det.estimated_size_m2.toFixed(1)} m²` : 'Not available'} />
            <Row k="GPS" v={gps} />
            <Row k="Depth" v={det.depth != null ? `${det.depth} m` : 'Not provided'} />
            <Row k="Bounding box" v={JSON.stringify(det.bbox)} />
          </dl>

          <div>
            <h4 className="text-sm font-semibold text-sonar-400 mb-2">Imagery</h4>
            <ImgBlock label="Original" src={det.image_storage_path ? `/api/images/${det.image_id}/original` : null} />
            <ImgBlock label="Processed" src={det.image_processed_path ? `/api/images/${det.image_id}/processed` : null} />
          </div>
        </div>

        <EvidenceCard detection={det} />

        <ReviewPanel
          detectionId={det.id}
          currentStatus={det.status}
          feedback={det.feedback || []}
          onSubmitted={reload}
        />
      </div>

      <p className="text-xs text-yellow-400/80">
        ⚠ Risk score is a prototype formula output, not a validated environmental risk assessment.
      </p>
    </div>
  )
}

function Row({ k, v }) {
  return (
    <div className="flex justify-between gap-2 border-b border-abyss-700 pb-1">
      <dt className="text-slate-500">{k}</dt>
      <dd className="text-right break-all">{v}</dd>
    </div>
  )
}

function ImgBlock({ label, src }) {
  if (!src) return <p className="text-xs italic text-slate-500">{label}: not available</p>
  return (
    <figure className="mb-2">
      <img src={src} alt={label} className="rounded border border-abyss-700 max-h-48 object-contain bg-black/30 w-full" />
      <figcaption className="text-xs text-slate-500 mt-1">{label}</figcaption>
    </figure>
  )
}
