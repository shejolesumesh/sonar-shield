import { useState } from 'react'
import { submitFeedback, friendlyError } from '../services/api'

const ACTIONS = [
  ['CONFIRM', 'Confirm AI label'],
  ['REJECT', 'Reject (not debris / false positive)'],
  ['RECLASSIFY', 'Reclassify'],
]

export default function ReviewPanel({ detectionId, currentStatus, feedback, onSubmitted }) {
  const [action, setAction] = useState('CONFIRM')
  const [expertLabel, setExpertLabel] = useState('')
  const [comment, setComment] = useState('')
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  async function submit() {
    setBusy(true); setErr(''); setMsg('')
    try {
      await submitFeedback({
        detection_id: detectionId,
        action,
        expert_label: expertLabel || null,
        comment: comment || null,
      })
      setMsg(`Recorded: ${action}. AI's original label is preserved in the audit trail.`)
      setComment(''); setExpertLabel('')
      onSubmitted?.()
    } catch (e) {
      setErr(friendlyError(e))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="card space-y-3">
      <h3 className="font-bold text-lg">Expert Review</h3>
      <p className="text-xs text-slate-500">Current status: <span className="badge bg-slate-800">{currentStatus}</span></p>

      <div className="space-y-2">
        {ACTIONS.map(([value, label]) => (
          <label key={value} className="flex items-center gap-2 text-sm cursor-pointer">
            <input type="radio" name="action" checked={action === value}
                   onChange={() => setAction(value)} className="accent-cyan-400" />
            {label}
          </label>
        ))}
      </div>

      {action === 'RECLASSIFY' && (
        <input className="input-field" placeholder="Corrected class (required)"
               value={expertLabel} onChange={(e) => setExpertLabel(e.target.value)} />
      )}

      <textarea className="input-field" rows="3" placeholder="Optional comment"
                value={comment} onChange={(e) => setComment(e.target.value)} />

      <button className="btn-primary w-full" disabled={busy || (action === 'RECLASSIFY' && !expertLabel.trim())} onClick={submit}>
        {busy ? 'Saving...' : 'Submit Review'}
      </button>
      {msg && <p className="text-xs text-green-400">{msg}</p>}
      {err && <p className="text-xs text-red-400">{err}</p>}

      {feedback.length > 0 && (
        <details>
          <summary className="cursor-pointer text-xs text-sonar-400">Audit trail ({feedback.length})</summary>
          <ul className="mt-2 space-y-2">
            {feedback.map((f) => (
              <li key={f.id} className="text-xs bg-abyss-900 rounded p-2">
                <b>{f.action}</b> - AI said "{f.ai_label}"
                {f.expert_label && <> -&gt; expert says "{f.expert_label}"</>}
                {f.comment && <p className="text-slate-500 mt-1">{f.comment}</p>}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  )
}
