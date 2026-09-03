import { useRef, useState } from 'react'
import {
  uploadSonarImage, runDetections, getImage, imageUrl, friendlyError,
} from '../services/api'
import DetectionCard from '../components/DetectionCard'

const EMPTY_META = {
  latitude: '', longitude: '', depth: '', timestamp: '',
  sonar_frequency_khz: '', swath_width_m: '', vessel_name: '', heave: '', pitch: '', roll: '', notes: '',
}

export default function SonarAnalysis() {
  const fileRef = useRef(null)
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [meta, setMeta] = useState(EMPTY_META)
  const [busy, setBusy] = useState(false)
  const [step, setStep] = useState('')
  const [image, setImage] = useState(null)
  const [detections, setDetections] = useState([])
  const [error, setError] = useState('')

  function pickFile(f) {
    setFile(f)
    setError('')
    setImage(null)
    setDetections([])
    if (f) setPreviewUrl(URL.createObjectURL(f))
    else setPreviewUrl(null)
  }

  function updateMeta(k, v) {
    setMeta((m) => ({ ...m, [k]: v }))
  }

  async function analyze() {
    if (!file) return
    setBusy(true)
    setError('')
    try {
      // Only send numeric fields that were actually filled in
      const clean = {}
      for (const [k, v] of Object.entries(meta)) {
        if (v === '') continue
        if (['latitude', 'longitude', 'depth', 'sonar_frequency_khz', 'swath_width_m', 'heave', 'pitch', 'roll'].includes(k)) {
          clean[k] = Number(v)
        } else {
          clean[k] = v
        }
      }

      setStep('Uploading image…')
      const up = await uploadSonarImage(file, Object.keys(clean).length ? clean : null)
      const imageId = up.data.id

      setStep('Running detection analysis…')
      await runDetections(imageId)

      setStep('Loading results…')
      const detail = await getImage(imageId)
      setImage(detail.data)
      setDetections(detail.data.detections)
      setStep('')
    } catch (e) {
      setError(friendlyError(e))
      setStep('')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Sonar Analysis</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Upload panel */}
        <div className="card space-y-4">
          <h3 className="font-semibold">1 · Upload side-scan sonar image</h3>

          <label
            className="block border-2 border-dashed border-abyss-700 rounded-lg p-6 text-center cursor-pointer hover:border-sonar-500 transition"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => { e.preventDefault(); pickFile(e.dataTransfer.files[0]) }}
          >
            <input
              ref={fileRef} type="file" accept=".png,.jpg,.jpeg,.tif,.tiff,.bmp"
              className="hidden"
              onChange={(e) => pickFile(e.target.files?.[0])}
            />
            {previewUrl ? (
              <img src={previewUrl} alt="preview" className="max-h-56 mx-auto rounded" />
            ) : (
              <>
                <p className="text-sonar-400 font-medium">Click or drop an image here</p>
                <p className="text-xs text-slate-500 mt-1">PNG, JPG, TIF, BMP · max 25 MB</p>
              </>
            )}
          </label>
          {file && <p className="text-xs text-slate-400">Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(1)} MB)</p>}

          <details>
            <summary className="cursor-pointer text-sm text-sonar-400">Optional sonar metadata (GPS, depth…)</summary>
            <div className="grid grid-cols-2 gap-3 mt-3">
              <Field label="Latitude (-90..90)" value={meta.latitude} onChange={(v) => updateMeta('latitude', v)} placeholder="12.9716" />
              <Field label="Longitude (-180..180)" value={meta.longitude} onChange={(v) => updateMeta('longitude', v)} placeholder="77.5946" />
              <Field label="Depth (m)" value={meta.depth} onChange={(v) => updateMeta('depth', v)} placeholder="42.5" />
              <Field label="Timestamp" value={meta.timestamp} onChange={(v) => updateMeta('timestamp', v)} placeholder="2025-01-15T08:30Z" />
              <Field label="Sonar freq (kHz)" value={meta.sonar_frequency_khz} onChange={(v) => updateMeta('sonar_frequency_khz', v)} />
              <Field label="Swath width (m)" value={meta.swath_width_m} onChange={(v) => updateMeta('swath_width_m', v)} />
              <Field label="Vessel name" value={meta.vessel_name} onChange={(v) => updateMeta('vessel_name', v)} />
              <Field label="Heave (metadata)" value={meta.heave} onChange={(v) => updateMeta('heave', v)} />
              <Field label="Pitch (metadata)" value={meta.pitch} onChange={(v) => updateMeta('pitch', v)} />
              <Field label="Roll (metadata)" value={meta.roll} onChange={(v) => updateMeta('roll', v)} />
            </div>
            <textarea
              className="input-field mt-3" rows="2" placeholder="Notes"
              value={meta.notes} onChange={(e) => updateMeta('notes', e.target.value)}
            />
          </details>

          <button className="btn-primary w-full" disabled={!file || busy} onClick={analyze}>
            {busy ? step || 'Working…' : 'Analyze Image'}
          </button>
          {error && <p className="text-sm text-red-400">{error}</p>}
        </div>

        {/* Results panel */}
        <div className="space-y-4">
          <div className="card">
            <h3 className="font-semibold mb-3">2 · Preprocessed view</h3>
            {image?.processed_path ? (
              <div className="space-y-2">
                <img src={imageUrl(image.id, 'processed')} alt="processed" className="w-full rounded" />
                <p className="text-xs text-slate-500">
                  Denoised, contrast-enhanced (CLAHE), shadow-emphasized, letterboxed to 640×640.
                  The original is preserved untouched.
                </p>
              </div>
            ) : (
              <p className="text-sm text-slate-500">
                Run an analysis to see the preprocessed sonar frame here.
              </p>
            )}
          </div>
          {image?.sonar_info?.quality && <QualityCard quality={image.sonar_info.quality} motion={image.sonar_info.motion_status} />}

          <div className="card">
            <h3 className="font-semibold mb-3">
              3 · Detections ({detections.length})
            </h3>
            {detections.length === 0 ? (
              <p className="text-sm text-slate-500">No detections yet.</p>
            ) : (
              <div className="space-y-2">
                {detections.map((d) => <DetectionCard key={d.id} det={d} />)}
              </div>
            )}
            {detections.some((d) => d.is_unknown_anomaly) && (
              <p className="text-xs text-purple-300 mt-3">
                Purple badges mark LOW CONFIDENCE - REVIEW regions - the detector's predicted class is
                still shown, but confidence was below the classification threshold, so it is flagged
                for expert review instead of being auto-confirmed.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function QualityCard({ quality, motion }) {
  const dropout = quality.dropout
  return <div className="card text-sm space-y-1">
    <h3 className="font-semibold">Sonar Quality</h3>
    <p className="text-xs text-slate-400">Image-derived indicators only; not calibrated sonar measurements.</p>
    <p>Overall quality: <b>{quality.overall_quality_score}/100</b> · Contrast: {quality.contrast_stddev} · Noise indicator: {quality.noise_indicator}</p>
    <p>Resolution: {quality.resolution_px.width}×{quality.resolution_px.height} · Shadow visibility: {(quality.acoustic_shadow_visibility_fraction * 100).toFixed(1)}%</p>
    <p>Data dropout: {dropout.detected ? 'Detected' : 'Not detected'} ({dropout.affected_percentage}%)</p>
    {dropout.detected && <p className="text-yellow-300">Low-quality sonar region detected. AI confidence may be affected.</p>}
    <p className="text-xs text-slate-400">{motion}</p>
  </div>
}

function Field({ label, value, onChange, placeholder }) {
  return (
    <label className="text-xs">
      <span className="text-slate-500 block mb-1">{label}</span>
      <input className="input-field" value={value} placeholder={placeholder}
             onChange={(e) => onChange(e.target.value)} />
    </label>
  )
}
