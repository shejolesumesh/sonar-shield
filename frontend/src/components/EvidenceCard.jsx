const NOT_AVAILABLE = 'Not available from current analysis'

function EvidenceSection({ title, items }) {
  return (
    <div>
      <h4 className="text-sm font-semibold text-sonar-400 mb-1">{title}</h4>
      <ul className="list-disc list-inside text-xs text-slate-300 space-y-0.5">
        {(items && items.length ? items : [NOT_AVAILABLE]).map((t, i) => (
          <li key={i} className={t === NOT_AVAILABLE ? 'italic text-slate-500' : ''}>{t}</li>
        ))}
      </ul>
    </div>
  )
}

export default function EvidenceCard({ detection }) {
  const ev = detection.evidence
  if (!ev) return null
  return (
    <div className="card space-y-3">
      <h3 className="font-bold text-lg">Evidence Card</h3>
      <EvidenceSection title="Confidence Evidence" items={ev.confidence_evidence} />
      <EvidenceSection title="Visual Evidence" items={ev.visual_evidence} />
      <EvidenceSection title="Shadow Evidence" items={ev.shadow_evidence} />
      {ev.explanation && (
        <p className="text-xs text-slate-400 italic">{ev.explanation}</p>
      )}
    </div>
  )
}
