'use client';
import { useState } from 'react';
import { ArrowUpDown, Search, ExternalLink } from 'lucide-react';
import { performanceData, getPropertyById } from '@/data/mockData';

export default function PerformanceTable() {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'monthlyRevenue', direction: 'desc' });
  const [selectedProperty, setSelectedProperty] = useState(null);

  const combinedData = performanceData.map((perf) => {
    const prop = getPropertyById(perf.propertyId);
    return { ...prop, ...perf };
  });

  const filtered = combinedData.filter((item) =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sorted = [...filtered].sort((a, b) => {
    if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === 'asc' ? -1 : 1;
    if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === 'asc' ? 1 : -1;
    return 0;
  });

  const handleSort = (key) => {
    setSortConfig((prev) => ({ key, direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc' }));
  };

  const SortHeader = ({ label, sortKey }) => (
    <button onClick={() => handleSort(sortKey)} className="flex items-center gap-1 hover:text-blue-600 transition-colors font-semibold">
      {label}<ArrowUpDown className="w-3 h-3" />
    </button>
  );

  return (
    <div className="card">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h2 className="text-lg font-bold text-gray-900">Rendimiento por Piso</h2>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input type="text" placeholder="Buscar piso..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-64" />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200 text-left text-gray-500">
              <th className="pb-3 font-semibold">Piso</th>
              <th className="pb-3"><SortHeader label="Ocupación" sortKey="occupancyRate" /></th>
              <th className="pb-3"><SortHeader label="ADR (€)" sortKey="adr" /></th>
              <th className="pb-3"><SortHeader label="Ingresos Mes" sortKey="monthlyRevenue" /></th>
              <th className="pb-3">Canal</th>
              <th className="pb-3">Acción</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sorted.map((item) => (
              <tr key={item.propertyId} className="hover:bg-gray-50 transition-colors cursor-pointer" onClick={() => setSelectedProperty(item)}>
                <td className="py-3">
                  <div><p className="font-semibold text-gray-900">{item.name}</p><p className="text-xs text-gray-500">{item.location}</p></div>
                </td>
                <td className="py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${item.occupancyRate >= 85 ? 'bg-green-500' : item.occupancyRate >= 70 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${item.occupancyRate}%` }} />
                    </div>
                    <span className="font-medium">{item.occupancyRate}%</span>
                  </div>
                </td>
                <td className="py-3 font-medium">€{item.adr.toFixed(2)}</td>
                <td className="py-3 font-bold text-gray-900">€{item.monthlyRevenue.toFixed(2)}</td>
                <td className="py-3">
                  <span className={`badge ${item.channel === 'Airbnb' ? 'bg-rose-100 text-rose-700' : 'bg-blue-100 text-blue-700'}`}>{item.channel}</span>
                </td>
                <td className="py-3">
                  <button className="p-1 hover:bg-gray-100 rounded transition-colors"><ExternalLink className="w-4 h-4 text-gray-400" /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedProperty && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={() => setSelectedProperty(null)}>
          <div className="bg-white rounded-xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-xl font-bold mb-4">{selectedProperty.name}</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span className="text-gray-500">Ubicación:</span> <span className="font-medium">{selectedProperty.location}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Huéspedes máx:</span> <span className="font-medium">{selectedProperty.maxGuests}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Habitaciones:</span> <span className="font-medium">{selectedProperty.bedrooms}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Ocupación:</span> <span className="font-medium">{selectedProperty.occupancyRate}%</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Ingresos mes:</span> <span className="font-bold text-green-600">€{selectedProperty.monthlyRevenue.toFixed(2)}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Beneficio neto:</span> <span className="font-bold text-blue-600">€{selectedProperty.netProfit.toFixed(2)}</span></div>
            </div>
            <button onClick={() => setSelectedProperty(null)} className="mt-6 w-full py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors">Cerrar</button>
          </div>
        </div>
      )}
    </div>
  );
}
