'use client';
import { TrendingUp, TrendingDown, Home, DollarSign, Percent, PiggyBank } from 'lucide-react';
import { globalKPIs } from '@/data/mockData';

export default function KPICards() {
  const kpis = [
    { title: 'Ingresos MTD', value: `€${globalKPIs.totalRevenueMTD.toLocaleString('es-ES', { minimumFractionDigits: 2 })}`, icon: DollarSign, trend: '+12.5%', trendUp: true, color: 'text-blue-600', bg: 'bg-blue-50' },
    { title: 'Ocupación Global', value: `${globalKPIs.avgOccupancy}%`, icon: Percent, trend: '+3.2%', trendUp: true, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { title: 'ADR Medio', value: `€${globalKPIs.avgADR}`, icon: Home, trend: '-1.8%', trendUp: false, color: 'text-amber-600', bg: 'bg-amber-50' },
    { title: 'Beneficio Neto', value: `€${globalKPIs.totalNetProfit.toLocaleString('es-ES', { minimumFractionDigits: 2 })}`, icon: PiggyBank, trend: '+8.4%', trendUp: true, color: 'text-violet-600', bg: 'bg-violet-50' },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {kpis.map((kpi) => {
        const Icon = kpi.icon;
        const TrendIcon = kpi.trendUp ? TrendingUp : TrendingDown;
        return (
          <div key={kpi.title} className="card card-hover">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg ${kpi.bg}`}><Icon className={`w-6 h-6 ${kpi.color}`} /></div>
              <div className={`flex items-center gap-1 text-sm font-medium ${kpi.trendUp ? 'text-green-600' : 'text-red-600'}`}>
                <TrendIcon className="w-4 h-4" />{kpi.trend}
              </div>
            </div>
            <p className="text-sm text-gray-500 font-medium">{kpi.title}</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">{kpi.value}</p>
          </div>
        );
      })}
    </div>
  );
}
