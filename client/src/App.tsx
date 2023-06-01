import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { HomePage } from './pages/home-page/HomePage'
import { NavBar } from './components/NavBar/NavBar'

export const App: React.FC = () => {
  return (
    <>
      <NavBar />
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </Router>
    </>
  )
}
