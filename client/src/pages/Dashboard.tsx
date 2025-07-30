import React from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Activity,
  BarChart3,
  Users,
  Target
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  AreaChart,
  Area
} from 'recharts';

const Dashboard: React.FC = () => {
  const stats = [
    {
      title: 'Portfolio Value',
      value: '$25,430.50',
      change: '+12.5%',
      changeType: 'positive',
      icon: DollarSign
    },
    {
      title: 'Total Return',
      value: '+$2,847.30',
      change: '+8.2%',
      changeType: 'positive',
      icon: TrendingUp
    },
    {
      title: 'Active Positions',
      value: '8',
      change: '+2',
      changeType: 'positive',
      icon: Activity
    },
    {
      title: 'Win Rate',
      value: '68.5%',
      change: '+5.2%',
      changeType: 'positive',
      icon: Target
    }
  ];

  const portfolioData = [
    { date: 'Jan', value: 22000 },
    { date: 'Feb', value: 23500 },
    { date: 'Mar', value: 22800 },
    { date: 'Apr', value: 24200 },
    { date: 'May', value: 25100 },
    { date: 'Jun', value: 25430 }
  ];

  const marketData = [
    { name: 'S&P 500', value: 4500, change: 0.5, color: '#3B82F6' },
    { name: 'NASDAQ', value: 14000, change: 0.8, color: '#10B981' },
    { name: 'DOW', value: 35000, change: 0.3, color: '#F59E0B' },
    { name: 'VIX', value: 15.5, change: -2.0, color: '#EF4444' }
  ];

  const recentTrades = [
    {
      symbol: 'AAPL',
      action: 'BUY',
      quantity: 10,
      price: 175.50,
      timestamp: '2 hours ago',
      pnl: '+$45.20'
    },
    {
      symbol: 'TSLA',
      action: 'SELL',
      quantity: 5,
      price: 250.75,
      timestamp: '1 day ago',
      pnl: '+$125.40'
    },
    {
      symbol: 'GOOGL',
      action: 'BUY',
      quantity: 3,
      price: 3000.00,
      timestamp: '2 days ago',
      pnl: '+$89.10'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-dark-400 mt-2">Welcome back! Here's your trading overview.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="bg-dark-800 rounded-lg p-6 border border-dark-700 card-hover">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-dark-400 text-sm font-medium">{stat.title}</p>
                <p className="text-2xl font-bold text-white mt-2">{stat.value}</p>
                <div className={`flex items-center mt-2 ${
                  stat.changeType === 'positive' ? 'text-success-500' : 'text-danger-500'
                }`}>
                  {stat.changeType === 'positive' ? (
                    <TrendingUp className="w-4 h-4 mr-1" />
                  ) : (
                    <TrendingDown className="w-4 h-4 mr-1" />
                  )}
                  <span className="text-sm font-medium">{stat.change}</span>
                </div>
              </div>
              <div className="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Performance Chart */}
        <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Portfolio Performance</h3>
            <select className="bg-dark-700 border border-dark-600 text-white text-sm rounded-lg px-3 py-1">
              <option>1M</option>
              <option>3M</option>
              <option>6M</option>
              <option>1Y</option>
            </select>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={portfolioData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="date" 
                stroke="#9CA3AF"
                fontSize={12}
              />
              <YAxis 
                stroke="#9CA3AF"
                fontSize={12}
                tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#fff'
                }}
                formatter={(value: number) => [`$${value.toLocaleString()}`, 'Portfolio Value']}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#3B82F6" 
                strokeWidth={3}
                dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#3B82F6', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Market Overview */}
        <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Market Overview</h3>
            <span className="text-sm text-dark-400">Real-time</span>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={marketData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="name" 
                stroke="#9CA3AF"
                fontSize={12}
              />
              <YAxis 
                stroke="#9CA3AF"
                fontSize={12}
                tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#fff'
                }}
                formatter={(value: number, name: string, props: any) => [
                  `${value.toLocaleString()} (${props.payload.change > 0 ? '+' : ''}${props.payload.change}%)`,
                  name
                ]}
              />
              <Bar 
                dataKey="value" 
                fill="#3B82F6"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Market Indices */}
      <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
        <h3 className="text-lg font-semibold text-white mb-4">Market Indices</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {marketData.map((index, idx) => (
            <div key={idx} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg">
              <div>
                <p className="text-white font-medium">{index.name}</p>
                <p className="text-dark-400 text-sm">{index.value.toLocaleString()}</p>
              </div>
              <div className="text-right">
                <p className={`text-sm font-medium ${index.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {index.change > 0 ? '+' : ''}{index.change}%
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Trades */}
      <div className="bg-dark-800 rounded-lg border border-dark-700">
        <div className="p-6 border-b border-dark-700">
          <h3 className="text-lg font-semibold text-white">Recent Trades</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {recentTrades.map((trade, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-dark-700 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    trade.action === 'BUY' ? 'bg-success-600' : 'bg-danger-600'
                  }`}>
                    <span className="text-white text-xs font-bold">{trade.action}</span>
                  </div>
                  <div>
                    <p className="text-white font-medium">{trade.symbol}</p>
                    <p className="text-dark-400 text-sm">{trade.quantity} shares @ ${trade.price}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-success-500 font-medium">{trade.pnl}</p>
                  <p className="text-dark-400 text-sm">{trade.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 