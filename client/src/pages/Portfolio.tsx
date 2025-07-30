import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Trash2, 
  TrendingUp, 
  PieChart, 
  DollarSign, 
  BarChart3
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart as RechartsPieChart, Pie, Cell } from 'recharts';

interface Portfolio {
  id: string;
  name: string;
  totalValue: number;
  totalReturn: number;
  returnPercentage: number;
  assets: Asset[];
  createdAt: string;
}

interface Asset {
  symbol: string;
  name: string;
  shares: number;
  avgPrice: number;
  currentPrice: number;
  marketValue: number;
  return: number;
  returnPercentage: number;
  allocation: number;
}

const Portfolio: React.FC = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [selectedPortfolio, setSelectedPortfolio] = useState<Portfolio | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showAddAssetModal, setShowAddAssetModal] = useState(false);
  const [newPortfolioName, setNewPortfolioName] = useState('');
  const [newAsset, setNewAsset] = useState({
    symbol: '',
    shares: 0,
    avgPrice: 0
  });

  // Mock data for demonstration
  useEffect(() => {
    const mockPortfolios: Portfolio[] = [
      {
        id: '1',
        name: 'Growth Portfolio',
        totalValue: 125000,
        totalReturn: 8750,
        returnPercentage: 7.5,
        createdAt: '2024-01-15',
        assets: [
          {
            symbol: 'AAPL',
            name: 'Apple Inc.',
            shares: 50,
            avgPrice: 150,
            currentPrice: 175,
            marketValue: 8750,
            return: 1250,
            returnPercentage: 16.7,
            allocation: 7.0
          },
          {
            symbol: 'TSLA',
            name: 'Tesla Inc.',
            shares: 30,
            avgPrice: 200,
            currentPrice: 250,
            marketValue: 7500,
            return: 1500,
            returnPercentage: 25.0,
            allocation: 6.0
          },
          {
            symbol: 'MSFT',
            name: 'Microsoft Corp.',
            shares: 40,
            avgPrice: 300,
            currentPrice: 350,
            marketValue: 14000,
            return: 2000,
            returnPercentage: 16.7,
            allocation: 11.2
          },
          {
            symbol: 'GOOGL',
            name: 'Alphabet Inc.',
            shares: 25,
            avgPrice: 120,
            currentPrice: 140,
            marketValue: 3500,
            return: 500,
            returnPercentage: 16.7,
            allocation: 2.8
          },
          {
            symbol: 'NVDA',
            name: 'NVIDIA Corp.',
            shares: 20,
            avgPrice: 400,
            currentPrice: 600,
            marketValue: 12000,
            return: 4000,
            returnPercentage: 50.0,
            allocation: 9.6
          }
        ]
      },
      {
        id: '2',
        name: 'Conservative Portfolio',
        totalValue: 75000,
        totalReturn: 2250,
        returnPercentage: 3.1,
        createdAt: '2024-02-01',
        assets: [
          {
            symbol: 'JNJ',
            name: 'Johnson & Johnson',
            shares: 100,
            avgPrice: 150,
            currentPrice: 155,
            marketValue: 15500,
            return: 500,
            returnPercentage: 3.3,
            allocation: 20.7
          },
          {
            symbol: 'PG',
            name: 'Procter & Gamble',
            shares: 80,
            avgPrice: 140,
            currentPrice: 145,
            marketValue: 11600,
            return: 400,
            returnPercentage: 3.6,
            allocation: 15.5
          }
        ]
      }
    ];
    setPortfolios(mockPortfolios);
    setSelectedPortfolio(mockPortfolios[0]);
  }, []);

  const createPortfolio = () => {
    if (!newPortfolioName.trim()) return;
    
    const newPortfolio: Portfolio = {
      id: Date.now().toString(),
      name: newPortfolioName,
      totalValue: 0,
      totalReturn: 0,
      returnPercentage: 0,
      assets: [],
      createdAt: new Date().toISOString().split('T')[0]
    };
    
    setPortfolios([...portfolios, newPortfolio]);
    setSelectedPortfolio(newPortfolio);
    setNewPortfolioName('');
    setShowCreateModal(false);
  };

  const addAsset = () => {
    if (!selectedPortfolio || !newAsset.symbol || newAsset.shares <= 0 || newAsset.avgPrice <= 0) return;
    
    const currentPrice = Math.random() * 200 + 50; // Mock current price
    const marketValue = newAsset.shares * currentPrice;
    const returnValue = marketValue - (newAsset.shares * newAsset.avgPrice);
    const returnPercentage = (returnValue / (newAsset.shares * newAsset.avgPrice)) * 100;
    
    const newAssetObj: Asset = {
      symbol: newAsset.symbol.toUpperCase(),
      name: `${newAsset.symbol.toUpperCase()} Corp.`,
      shares: newAsset.shares,
      avgPrice: newAsset.avgPrice,
      currentPrice,
      marketValue,
      return: returnValue,
      returnPercentage,
      allocation: 0 // Will be calculated
    };
    
    const updatedPortfolio = {
      ...selectedPortfolio,
      assets: [...selectedPortfolio.assets, newAssetObj]
    };
    
    // Recalculate portfolio totals
    const totalValue = updatedPortfolio.assets.reduce((sum, asset) => sum + asset.marketValue, 0);
    const totalReturn = updatedPortfolio.assets.reduce((sum, asset) => sum + asset.return, 0);
    const newReturnPercentage = totalValue > 0 ? (totalReturn / (totalValue - totalReturn)) * 100 : 0;
    
    updatedPortfolio.totalValue = totalValue;
    updatedPortfolio.totalReturn = totalReturn;
    updatedPortfolio.returnPercentage = newReturnPercentage;
    
    // Recalculate allocations
    updatedPortfolio.assets = updatedPortfolio.assets.map(asset => ({
      ...asset,
      allocation: totalValue > 0 ? (asset.marketValue / totalValue) * 100 : 0
    }));
    
    setPortfolios(portfolios.map(p => p.id === selectedPortfolio.id ? updatedPortfolio : p));
    setSelectedPortfolio(updatedPortfolio);
    setNewAsset({ symbol: '', shares: 0, avgPrice: 0 });
    setShowAddAssetModal(false);
  };

  const removeAsset = (symbol: string) => {
    if (!selectedPortfolio) return;
    
    const updatedAssets = selectedPortfolio.assets.filter(asset => asset.symbol !== symbol);
    const totalValue = updatedAssets.reduce((sum, asset) => sum + asset.marketValue, 0);
    const totalReturn = updatedAssets.reduce((sum, asset) => sum + asset.return, 0);
    const newReturnPercentage = totalValue > 0 ? (totalReturn / (totalValue - totalReturn)) * 100 : 0;
    
    const updatedPortfolio = {
      ...selectedPortfolio,
      assets: updatedAssets.map(asset => ({
        ...asset,
        allocation: totalValue > 0 ? (asset.marketValue / totalValue) * 100 : 0
      })),
      totalValue,
      totalReturn,
      returnPercentage: newReturnPercentage
    };
    
    setPortfolios(portfolios.map(p => p.id === selectedPortfolio.id ? updatedPortfolio : p));
    setSelectedPortfolio(updatedPortfolio);
  };

  const getPerformanceColor = (percentage: number) => {
    if (percentage > 0) return 'text-green-400';
    if (percentage < 0) return 'text-red-400';
    return 'text-gray-400';
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Portfolio</h1>
          <p className="text-dark-400 mt-2">Manage your investment portfolio</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-all hover:scale-105"
        >
          <Plus size={20} />
          New Portfolio
        </button>
      </div>

      {/* Portfolio Selection */}
      <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
        <h2 className="text-xl font-semibold text-white mb-4">Select Portfolio</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {portfolios.map((portfolio) => (
            <div
              key={portfolio.id}
              onClick={() => setSelectedPortfolio(portfolio)}
              className={`p-4 rounded-lg border cursor-pointer transition-all hover:scale-105 ${
                selectedPortfolio?.id === portfolio.id
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-dark-700 bg-dark-700/50 hover:border-dark-600'
              }`}
            >
              <h3 className="text-white font-semibold">{portfolio.name}</h3>
              <p className="text-dark-400 text-sm">${portfolio.totalValue.toLocaleString()}</p>
              <p className={`text-sm ${getPerformanceColor(portfolio.returnPercentage)}`}>
                {portfolio.returnPercentage > 0 ? '+' : ''}{portfolio.returnPercentage.toFixed(2)}%
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Portfolio Details */}
      {selectedPortfolio && (
        <div className="space-y-6">
          {/* Portfolio Summary */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
              <div className="flex items-center gap-3">
                <DollarSign className="text-blue-400" size={24} />
                <div>
                  <p className="text-dark-400 text-sm">Total Value</p>
                  <p className="text-white text-2xl font-bold">
                    ${selectedPortfolio.totalValue.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
              <div className="flex items-center gap-3">
                <TrendingUp className="text-green-400" size={24} />
                <div>
                  <p className="text-dark-400 text-sm">Total Return</p>
                  <p className={`text-2xl font-bold ${getPerformanceColor(selectedPortfolio.totalReturn)}`}>
                    ${selectedPortfolio.totalReturn.toLocaleString()}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
              <div className="flex items-center gap-3">
                <BarChart3 className="text-purple-400" size={24} />
                <div>
                  <p className="text-dark-400 text-sm">Return %</p>
                  <p className={`text-2xl font-bold ${getPerformanceColor(selectedPortfolio.returnPercentage)}`}>
                    {selectedPortfolio.returnPercentage > 0 ? '+' : ''}{selectedPortfolio.returnPercentage.toFixed(2)}%
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
              <div className="flex items-center gap-3">
                <PieChart className="text-orange-400" size={24} />
                <div>
                  <p className="text-dark-400 text-sm">Assets</p>
                  <p className="text-white text-2xl font-bold">{selectedPortfolio.assets.length}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Asset Allocation Chart */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
              <h3 className="text-white font-semibold mb-4">Asset Allocation</h3>
              {selectedPortfolio.assets.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                <RechartsPieChart>
                  <Pie
                    data={selectedPortfolio.assets}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ symbol, percent }) => `${symbol} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="marketValue"
                    nameKey="symbol"
                  >
                    {selectedPortfolio.assets.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                                  </RechartsPieChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-64 text-dark-400">
                  <p>No assets to display. Add some assets to see the allocation chart.</p>
                </div>
              )}
            </div>

            {/* Performance Chart */}
            <div className="bg-dark-800 rounded-lg p-6 border border-dark-700">
              <h3 className="text-white font-semibold mb-4">Portfolio Performance</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={[
                  { month: 'Jan', value: 100000 },
                  { month: 'Feb', value: 105000 },
                  { month: 'Mar', value: 110000 },
                  { month: 'Apr', value: 108000 },
                  { month: 'May', value: 115000 },
                  { month: 'Jun', value: 125000 }
                ]}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="month" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                  <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Assets Table */}
          <div className="bg-dark-800 rounded-lg border border-dark-700">
            <div className="p-6 border-b border-dark-700">
              <div className="flex justify-between items-center">
                <h3 className="text-white font-semibold">Assets</h3>
                <button
                  onClick={() => setShowAddAssetModal(true)}
                  className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-lg flex items-center gap-2 text-sm transition-all hover:scale-105"
                >
                  <Plus size={16} />
                  Add Asset
                </button>
              </div>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-dark-700">
                  <tr>
                    <th className="text-left p-4 text-dark-300 font-medium">Symbol</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Name</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Shares</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Avg Price</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Current Price</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Market Value</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Return</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Allocation</th>
                    <th className="text-left p-4 text-dark-300 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedPortfolio.assets.map((asset, index) => (
                    <tr
                      key={asset.symbol}
                      className="border-b border-dark-700 hover:bg-dark-700/50 transition-colors"
                    >
                      <td className="p-4 text-white font-semibold">{asset.symbol}</td>
                      <td className="p-4 text-dark-300">{asset.name}</td>
                      <td className="p-4 text-white">{asset.shares.toLocaleString()}</td>
                      <td className="p-4 text-white">${asset.avgPrice.toFixed(2)}</td>
                      <td className="p-4 text-white">${asset.currentPrice.toFixed(2)}</td>
                      <td className="p-4 text-white">${asset.marketValue.toLocaleString()}</td>
                      <td className={`p-4 ${getPerformanceColor(asset.returnPercentage)}`}>
                        ${asset.return.toLocaleString()} ({asset.returnPercentage > 0 ? '+' : ''}{asset.returnPercentage.toFixed(2)}%)
                      </td>
                      <td className="p-4 text-white">{asset.allocation.toFixed(1)}%</td>
                      <td className="p-4">
                        <button
                          onClick={() => removeAsset(asset.symbol)}
                          className="text-red-400 hover:text-red-300 p-1 transition-colors"
                        >
                          <Trash2 size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Create Portfolio Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-dark-800 rounded-lg p-6 w-full max-w-md border border-dark-700">
            <h3 className="text-white text-xl font-semibold mb-4">Create New Portfolio</h3>
            <input
              type="text"
              placeholder="Portfolio Name"
              value={newPortfolioName}
              onChange={(e) => setNewPortfolioName(e.target.value)}
              className="w-full p-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-dark-400 mb-4"
            />
            <div className="flex gap-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 p-3 bg-dark-700 text-white rounded-lg hover:bg-dark-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={createPortfolio}
                className="flex-1 p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Asset Modal */}
      {showAddAssetModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-dark-800 rounded-lg p-6 w-full max-w-md border border-dark-700">
            <h3 className="text-white text-xl font-semibold mb-4">Add Asset</h3>
            <input
              type="text"
              placeholder="Symbol (e.g., AAPL)"
              value={newAsset.symbol}
              onChange={(e) => setNewAsset({ ...newAsset, symbol: e.target.value })}
              className="w-full p-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-dark-400 mb-4"
            />
            <input
              type="number"
              placeholder="Number of Shares"
              value={newAsset.shares}
              onChange={(e) => setNewAsset({ ...newAsset, shares: Number(e.target.value) })}
              className="w-full p-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-dark-400 mb-4"
            />
            <input
              type="number"
              placeholder="Average Price"
              value={newAsset.avgPrice}
              onChange={(e) => setNewAsset({ ...newAsset, avgPrice: Number(e.target.value) })}
              className="w-full p-3 bg-dark-700 border border-dark-600 rounded-lg text-white placeholder-dark-400 mb-4"
            />
            <div className="flex gap-3">
              <button
                onClick={() => setShowAddAssetModal(false)}
                className="flex-1 p-3 bg-dark-700 text-white rounded-lg hover:bg-dark-600 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={addAsset}
                className="flex-1 p-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Add Asset
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Portfolio; 