import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import SonarAnalysis from './pages/SonarAnalysis'
import DetectionDetails from './pages/DetectionDetails'
import RecoveryPriority from './pages/RecoveryPriority'
import MapHeatmap from './pages/MapHeatmap'
import ExpertReview from './pages/ExpertReview'
import Reports from './pages/Reports'
import ModelInfo from './pages/ModelInfo'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analysis" element={<SonarAnalysis />} />
        <Route path="/detections/:id" element={<DetectionDetails />} />
        <Route path="/priority" element={<RecoveryPriority />} />
        <Route path="/map" element={<MapHeatmap />} />
        <Route path="/review" element={<ExpertReview />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/model" element={<ModelInfo />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}
