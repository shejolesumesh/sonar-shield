import { useEffect, useState } from 'react'
import { getModelInfo, getHealth, friendlyError } from '../services/api'

export default function ModelInfo() {
  const [info, setInfo] = useState(null)
  const [health, setHealth] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getModelInfo(), getHealth()])
      .then(([m, h]) => { setInfo(m.data); setHealth(h.data) })
      .catch((e) => setError(friendlyError(e)))
  }, [])

  if (error) return <p className="card text-red-400">{error}</p>
  if (!info) return <p className="text-slate-500">Loading…</p>

  const w = info.risk_formula.weights

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold">Model Information</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card space-y-3">
          <h3 className="font-semibold">Active Detector</h3>
          <p className="text-sm">
            Mode: <b className={info.is_demo_model ? 'text-yellow-300' : 'text-green-300'}>
              {info.active_mode}
            </b>
          </p>
          {info.is_demo_model && (
            <p className="text-xs text-yellow-300 bg-yellow-900/30 border border-yellow-800 rounded p-2">
              The DEMO MODEL produces deterministic heuristic pseudo-detections for development.
              Its outputs are NOT scientifically validated predictions of debris type or location.
            </p>
          )}
          {info.fallback_reason && (
            <p className="text-xs text-slate-400">Fallback reason: <code>{info.fallback_reason}</code></p>
          )}
          {!info.is_demo_model && (
            <ul className="text-sm space-y-1 text-slate-300">
              <li>Model: <code>{info.model_name}</code></li>
              <li>Format: <code>{info.model_format}</code></li>
              <li>Version: <code>{info.model_version}</code></li>
              <li>Supported class: <code>{info.supported_classes?.join(', ')}</code></li>
              <li>Input / output: <code>{JSON.stringify(info.input_shape)} → {JSON.stringify(info.output_shape)}</code></li>
              <li>NMS: <code>{info.nms_in_model ? 'included in model' : 'applied by SONAR-SHIELD'}</code></li>
            </ul>
          )}
          {info.class_metadata_note && <p className="text-xs text-slate-400">{info.class_metadata_note}</p>}
          <ul className="text-sm space-y-1 text-slate-300">
            <li>Configured detector: <code>{info.configured_detector_type}</code></li>
            <li>Known-class threshold: <code>{info.known_class_threshold}</code></li>
            <li>Min detection confidence: <code>{info.min_detection_confidence}</code></li>
            <li>Backend health: <code>{health?.database}</code></li>
          </ul>
        </div>

        <div className="card space-y-3">
          <h3 className="font-semibold">Prototype Risk Formula</h3>
          <pre className="bg-abyss-900 rounded p-3 text-xs overflow-x-auto">{info.risk_formula.expression}</pre>
          <ul className="text-xs space-y-0.5 text-slate-400">
            <li>w_confidence = {w.confidence}</li>
            <li>w_severity = {w.severity}</li>
            <li>w_size = {w.size}</li>
            <li>w_location = {w.location}</li>
          </ul>
          <p className="text-xs italic text-slate-500">{info.risk_formula.label}</p>
        </div>
      </div>

      <div className="card space-y-2">
        <h3 className="font-semibold">Model Versions</h3>
        {info.versions.length === 0 ? (
          <p className="text-sm text-slate-500">No model versions registered yet - run an analysis.</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-slate-500 text-left text-xs uppercase">
              <tr><th className="py-1">Version</th><th>Model</th><th>Description</th><th>Active</th></tr>
            </thead>
            <tbody>
              {info.versions.map((v) => (
                <tr key={v.version} className="border-t border-abyss-700">
                  <td className="py-1.5"><code>{v.version}</code></td>
                  <td>{v.model_name}</td>
                  <td className="text-xs text-slate-400 max-w-md truncate">{v.description}</td>
                  <td>{v.is_active ? '✓' : ''}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card space-y-2">
        <h3 className="font-semibold">Feedback &amp; Retraining Policy</h3>
        <p className="text-sm text-slate-300">
          Expert feedback collected so far: <b className="text-sonar-400">{info.feedback_collected}</b>
        </p>
        <p className="text-xs text-slate-500">{info.retraining_note}</p>
      </div>
    </div>
  )
}
