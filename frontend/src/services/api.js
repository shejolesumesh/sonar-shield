import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getHealth = () => api.get('/health')

export const uploadSonarImage = (file, metadata) => {
  const fd = new FormData()
  fd.append('file', file)
  if (metadata) fd.append('metadata_json', JSON.stringify(metadata))
  return api.post('/sonar/upload', fd)
}

export const runDetections = (imageId) =>
  api.post(`/detections/run?image_id=${encodeURIComponent(imageId)}`)

export const listDetections = (params = {}) => api.get('/detections', { params })
export const getDetection = (id) => api.get(`/detections/${id}`)
export const getPriorityQueue = () => api.get('/detections/priority-queue')

export const listImages = () => api.get('/images')
export const getImage = (id) => api.get(`/images/${id}`)
export const imageUrl = (id, kind) => `/api/images/${id}/${kind}`

export const getHeatmap = () => api.get('/heatmap')
export const getMapPoints = () => api.get('/map-points')

export const submitFeedback = (payload) => api.post('/feedback', payload)
export const listFeedback = (params = {}) => api.get('/feedback', { params })

export const getModelInfo = () => api.get('/model')

export const getReportSummary = () => api.get('/reports/summary')
export const reportCsvUrl = '/api/reports/export/csv'
export const reportJsonUrl = '/api/reports/export/json'

export function friendlyError(err) {
  if (err?.response?.data?.detail) {
    const d = err.response.data.detail
    return typeof d === 'string' ? d : 'Invalid input - check your entries.'
  }
  if (err?.code === 'ERR_NETWORK') return 'Cannot reach backend at :8000. Is it running?'
  return err.message || 'Unexpected error'
}
