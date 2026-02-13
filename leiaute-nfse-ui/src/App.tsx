import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from '@/components/Layout'
import SearchPage from '@/pages/SearchPage'
import ServiceDetailPage from '@/pages/ServiceDetailPage'
import RulesPage from '@/pages/RulesPage'
import ScenariosPage from '@/pages/ScenariosPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<SearchPage />} />
          <Route path="/services/:codigo" element={<ServiceDetailPage />} />
          <Route path="/rules" element={<RulesPage />} />
          <Route path="/scenarios" element={<ScenariosPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
