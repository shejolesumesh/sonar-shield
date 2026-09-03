import { useCallback, useEffect, useState } from 'react'
import DetectionCard from '../components/DetectionCard'
import { listDetections, listImages, imageUrl, runDetections, friendlyError } from '../services/api'

const FILTERS = [
  ['all', 'All'],
  ['pending', 'Pending'],
  ['unknown', 'Unknown Anomalies'],
]

export default function ExpertReview() {
  const [filter, setFilter] = useState('pending')
  const [detections, setDetections] = useState([])
  const [images, setImages] = useState([])
  const [selectedImage, setSelectedImage] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    try {
      const params = filter === 'unknown' ? { unknown_only: true } : {}
      const r = await listDetections({ limit: 200, ...params })
      let rows = r.data
      if (filter === 'pending') rows = rows.filter((d) => d.status === 'PENDING')
      setDetections(rows)
    } catch (e) {
      setError(friendlyError(e))
    }
  }, [filter])

  useEffect(() => { load() }, [load])
  useEffect(() => {
    listImages().then((r) => setImages(r.data)).catch(() => {})
  }, [])

  async function rerun(imageId) {
    if (!imageId) return
    setBusy(true); setError('')
    try {
      await runDetections(imageId)
      await load()
    } catch (e) {
      setError(friendlyError(e))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Expert Review Queue</h2>

      <div className="flex flex-wrap gap-2 items-center">
        {FILTERS.map(([v, label]) => (
          <button key={v} onClick={() => setFilter(v)}
                  className={filter === v ? 'btn-primary !py-1 text-sm' : 'btn-secondary !py-1 text-sm'}>
            {label}
          </button>
        ))}
        <div className="ml-auto flex gap-2 items-center">
          <select className="input-field !w-auto text-sm" value={selectedImage}
                  onChange={(e) => setSelectedImage(e.target.value)}>
            <option value="">Re-run analysis on…</option>
            {images.map((im) => (
              <option key={im.id} value={im.id}>{im.filename.slice(0, 40)}</option>
            ))}
          </select>
          <button className="btn-secondary text-sm" disabled={busy || !selectedImage} onClick={() => rerun(selectedImage)}>
            {busy ? 'Running…' : 'Re-run'}
          </button>
        </div>
      </div>

      {error && <p className="card text-red-400 text-sm">{error}</p>}
      {detections.length === 0 ? (
        <p className="card text-slate-500">No detections in this view.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
          {detections.map((d) => (
            <DetectionWithThumb key={d.id} det={d} thumb={imageUrl(d.image_id, 'processed')} />
          ))}
        </div>
      )}
    </div>
  )
}

function DetectionWithThumb({ det, thumb }) {
  const [src, setSrc] = useState(thumb)
  return (
    <div className="space-y-1">
      {src && (
        <img src={src} alt="" onError={() => setSrc(null)}
             className="rounded border border-abyss-700 h-28 w-full object-cover" />
      )}
      <DetectionCard det={det} />
    </div>
  )
}
