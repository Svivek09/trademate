import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  BarChart3, 
  TrendingUp, 
  Activity, 
  Briefcase, 
  Brain,
  Settings,
  HelpCircle
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const navItems = [
    {
      path: '/',
      icon: BarChart3,
      label: 'Dashboard',
      description: 'Overview & Analytics'
    },
    {
      path: '/market',
      icon: TrendingUp,
      label: 'Market Data',
      description: 'Real-time Quotes & Charts'
    },
    {
      path: '/backtesting',
      icon: Activity,
      label: 'Backtesting',
      description: 'Strategy Testing'
    },
    {
      path: '/portfolio',
      icon: Briefcase,
      label: 'Portfolio',
      description: 'Portfolio Management'
    },
    {
      path: '/ai-insights',
      icon: Brain,
      label: 'AI Insights',
      description: 'AI-Powered Analysis'
    }
  ];

  return (
    <div className="w-64 bg-dark-800 border-r border-dark-700 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-dark-700">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">TradeMate</h1>
            <p className="text-xs text-dark-400">Trading Analytics</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3 py-3 rounded-lg transition-all duration-200 group ${
                isActive
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'text-dark-300 hover:bg-dark-700 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <div className="flex-1">
              <div className="font-medium">{item.label}</div>
              <div className="text-xs opacity-75">{item.description}</div>
            </div>
          </NavLink>
        ))}
      </nav>

      {/* Bottom Actions */}
      <div className="p-4 border-t border-dark-700 space-y-2">
        <button className="w-full flex items-center space-x-3 px-3 py-2 text-dark-300 hover:text-white hover:bg-dark-700 rounded-lg transition-colors duration-200">
          <Settings className="w-4 h-4" />
          <span className="text-sm">Settings</span>
        </button>
        <button className="w-full flex items-center space-x-3 px-3 py-2 text-dark-300 hover:text-white hover:bg-dark-700 rounded-lg transition-colors duration-200">
          <HelpCircle className="w-4 h-4" />
          <span className="text-sm">Help</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar; 