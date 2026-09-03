import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import { getMapPoints, getHeatmap, friendlyError } from '../services/api'

const riskColor = {
  LOW: '#22c55e', MEDIUM: '#eab308', HIGH: '#f97316', CRITICAL: '#ef4444',
}

export default function MapHeatmap() {
  const [heatmap, setHeatmap] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getHeatmap(), getMapPoints()])
      .then(([hm, mp]) => setHeatmap({ ...mp.data, hasAny: hm.data.has_data }))
      .catch((e) => setError(friendlyError(e)))
  }, [])

  if (error) return <p className="card text-red-400">{error}</p>
  if (!heatmap) return <p className="text-slate-500">Loading map…</p>

  const points = heatmap.points || []

  // Center on data if available; otherwise neutral ocean view
  const center = points.length
    ? [avg(points.map((p) => p.latitude)), avg(points.map((p) => p.longitude))]
    : [10.0, 75.0]

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Debris Map &amp; Density Heatmap</h2>

      {!heatmap.hasAny && (
        <div className="card border-yellow-700 text-yellow-300 text-sm">
          No geolocated detections yet. SONAR-SHIELD never invents coordinates - upload images
          with valid latitude/longitude metadata to populate this map.
        </div>
      )}

      <div className="card p-0 overflow-hidden">
        <MapContainer center={center} zoom={points.length ? 8 : 4} style={{ height: '520px', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                     attribution="© OpenStreetMap contributors" />
          {points.map((p) => (
            <CircleMarker
              key={p.detection_id}
              center={[p.latitude, p.longitude]}
              radius={8 + (5 - Math.min(p.priority, 4)) * 2}
              pathOptions={{
                color: riskColor[p.risk_level] || '#06b6d4',
                fillColor: riskColor[p.risk_level] || '#06b6d4',
                fillOpacity: 0.45,
                weight: 1.5,
              }}
            >
              <Popup>
                <b>{p.object_type}</b><br />
                Risk: {p.risk_level} · P{p.priority}<br />
                Confidence: {(p.confidence * 100).toFixed(0)}%<br />
                Status: {p.status}<br />
                <a href={`/detections/${p.detection_id}`}>Open details →</a>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      <div className="flex gap-4 text-xs text-slate-400">
        {Object.entries(riskColor).map(([lvl, c]) => (
          <span key={lvl} className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full inline-block" style={{ background: c }} />
            {lvl}
          </span>
        ))}
        <span>Marker size reflects recovery priority.</span>
      </div>
    </div>
  )
}

function avg(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length
}
