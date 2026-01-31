import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import VendorDashboard from './pages/VendorDashboard';
import ReceiverDashboard from './pages/ReceiverDashboard';
import DriverScanner from './pages/DriverScanner';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/vendor/:vendorId" element={<VendorDashboard />} />
        <Route path="/receiver/:receiverId" element={<ReceiverDashboard />} />
        <Route path="/driver/scan/:loadId" element={<DriverScanner />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
