import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Truck, Building2, Package, TrendingUp, MapPin, Zap } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  const dashboards = [
    {
      title: 'Driver Dashboard',
      description: 'Find profitable return loads, navigate routes, and maximize earnings',
      icon: Truck,
      color: 'bg-blue-500',
      path: '/driver',
      features: ['Route Planning', 'Load Matching', 'Real-time Navigation', 'Earnings Tracker']
    },
    {
      title: 'Owner Dashboard',
      description: 'Track your fleet in real-time, monitor performance, and optimize operations',
      icon: Building2,
      color: 'bg-green-500',
      path: '/owner',
      features: ['Fleet Tracking', 'Performance Analytics', 'Revenue Reports', 'Driver Management']
    },
    {
      title: 'Vendor Dashboard',
      description: 'Post loads, find drivers, and manage shipments efficiently',
      icon: Package,
      color: 'bg-purple-500',
      path: '/vendor',
      features: ['Post Loads', 'Find Drivers', 'Track Shipments', 'Payment Management']
    }
  ];

  const stats = [
    { label: 'Active Trucks', value: '500+', icon: Truck },
    { label: 'Loads Matched', value: '10K+', icon: Package },
    { label: 'Cost Saved', value: '₹2Cr+', icon: TrendingUp },
    { label: 'Cities Covered', value: '50+', icon: MapPin }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-md border-b border-white/10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Truck className="w-8 h-8 text-blue-400" />
              <h1 className="text-2xl font-bold text-white">Deadheading Optimization</h1>
            </div>
            <div className="flex items-center space-x-2 text-green-400">
              <Zap className="w-5 h-5" />
              <span className="text-sm font-medium">AI-Powered</span>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-white mb-6">
            Eliminate Empty Return Trips
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            AI-powered system to match drivers with profitable return loads, 
            reducing fuel waste and maximizing earnings
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <stat.icon className="w-8 h-8 text-blue-400" />
                <span className="text-3xl font-bold text-white">{stat.value}</span>
              </div>
              <p className="text-gray-300">{stat.label}</p>
            </div>
          ))}
        </div>

        {/* Dashboards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {dashboards.map((dashboard, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 hover:border-white/40 transition-all duration-300 hover:transform hover:scale-105 cursor-pointer"
              onClick={() => navigate(dashboard.path)}
            >
              <div className={`${dashboard.color} w-16 h-16 rounded-xl flex items-center justify-center mb-6`}>
                <dashboard.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">{dashboard.title}</h3>
              <p className="text-gray-300 mb-6">{dashboard.description}</p>
              <ul className="space-y-2 mb-6">
                {dashboard.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center text-gray-300">
                    <div className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-3"></div>
                    {feature}
                  </li>
                ))}
              </ul>
              <button className="w-full bg-white/20 hover:bg-white/30 text-white font-semibold py-3 rounded-lg transition-colors">
                Open Dashboard
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-16 border-t border-white/10">
        <h3 className="text-3xl font-bold text-white text-center mb-12">How It Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-blue-500/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-blue-400">1</span>
            </div>
            <h4 className="text-xl font-semibold text-white mb-2">Driver Marks Deadheading</h4>
            <p className="text-gray-300">After delivery, driver marks return trip as empty</p>
          </div>
          <div className="text-center">
            <div className="bg-green-500/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-green-400">2</span>
            </div>
            <h4 className="text-xl font-semibold text-white mb-2">AI Finds Loads</h4>
            <p className="text-gray-300">System automatically matches profitable return loads</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-500/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-purple-400">3</span>
            </div>
            <h4 className="text-xl font-semibold text-white mb-2">Driver Earns Money</h4>
            <p className="text-gray-300">Accept load and earn instead of driving empty</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black/30 backdrop-blur-md border-t border-white/10 mt-16">
        <div className="container mx-auto px-6 py-8">
          <p className="text-center text-gray-400">
            © 2026 Deadheading Optimization System. Powered by AI & OpenStreetMap.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
