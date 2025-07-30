import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';

// Components
import Sidebar from './components/Sidebar';
import Header from './components/Header';

// Pages
import Dashboard from './pages/Dashboard';
import MarketData from './pages/MarketData';
import Backtesting from './pages/Backtesting';
import Portfolio from './pages/Portfolio';
import AIInsights from './pages/AIInsights';

const App: React.FC = () => {
  return (
    <div className="flex h-screen bg-dark-900">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-dark-900">
          <div className="container mx-auto px-6 py-8">
            <Routes>
              <Route 
                path="/" 
                element={
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <Dashboard />
                  </motion.div>
                } 
              />
              <Route 
                path="/market" 
                element={
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <MarketData />
                  </motion.div>
                } 
              />
              <Route 
                path="/backtesting" 
                element={
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <Backtesting />
                  </motion.div>
                } 
              />
              <Route 
                path="/portfolio" 
                element={
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <Portfolio />
                  </motion.div>
                } 
              />
              <Route 
                path="/ai-insights" 
                element={
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                  >
                    <AIInsights />
                  </motion.div>
                } 
              />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
};

export default App; 