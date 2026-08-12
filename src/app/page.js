import KPICards from '@/components/KPICards';
import PerformanceTable from '@/components/PerformanceTable';
import OperationalBlock from '@/components/OperationalBlock';
import QualityBlock from '@/components/QualityBlock';
import { RevenueChart, ChannelChart } from '@/components/ChartComponent';
import { Building2, BarChart3 } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <Building2 className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900">Rental Manager Pro</h1>
              <p className="text-xs text-gray-500">Demo — 7 propiedades activas</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 bg-green-50 text-green-700 text-xs font-medium rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
              Sistema Activo
            </span>
            <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-bold text-gray-600">AD</div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <section>
          <KPICards />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
            <div className="lg:col-span-2 card">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <h2 className="text-lg font-bold text-gray-900">Evolución de Ingresos</h2>
              </div>
              <RevenueChart />
            </div>
            <div className="card">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Distribución por Canal</h2>
              <ChannelChart />
            </div>
          </div>
        </section>

        <section><PerformanceTable /></section>
        <section><OperationalBlock /></section>
        <section><QualityBlock /></section>

        <footer className="text-center text-xs text-gray-400 pt-8 pb-4">
          <p>Vacation Rental Dashboard v1.0.0 — Modo Demo (Datos Simulados)</p>
          <p className="mt-1">No conectado a APIs reales de Airbnb ni Booking.com</p>
        </footer>
      </main>
    </div>
  );
}
