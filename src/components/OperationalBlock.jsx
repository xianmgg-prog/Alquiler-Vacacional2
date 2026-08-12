'use client';
import { Calendar, Clock, CheckCircle2, AlertCircle, ArrowRightLeft } from 'lucide-react';
import { todayOperations, next7Days, occupancyMatrix, properties, getPropertyById } from '@/data/mockData';

export default function OperationalBlock() {
  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric' });
  };

  const getDayLabel = (index) => {
    if (index === 0) return 'Hoy';
    if (index === 1) return 'Mañ';
    return formatDate(next7Days[index]);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="card">
        <div className="flex items-center gap-2 mb-5">
          <Clock className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-bold text-gray-900">Operativa del Día</h2>
        </div>
        <div className="space-y-3">
          {todayOperations.map((op) => {
            const prop = getPropertyById(op.propertyId);
            const isCheckIn = op.type === 'check-in';
            return (
              <div key={op.id} className="flex items-center gap-4 p-3 rounded-lg border border-gray-100 hover:border-gray-200 transition-colors">
                <div className={`p-2 rounded-lg ${isCheckIn ? 'bg-green-50 text-green-600' : 'bg-orange-50 text-orange-600'}`}>
                  <ArrowRightLeft className="w-4 h-4" style={{ transform: isCheckIn ? 'rotate(180deg)' : 'none' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-bold uppercase ${isCheckIn ? 'text-green-600' : 'text-orange-600'}`}>{isCheckIn ? 'Check-in' : 'Check-out'}</span>
                    <span className="text-xs text-gray-400">• {op.time}</span>
                  </div>
                  <p className="font-semibold text-gray-900 truncate">{prop.name}</p>
                  <p className="text-xs text-gray-500">{op.guestName} • {op.nights} noches • {op.platform}</p>
                </div>
                <div className={`flex items-center gap-1 text-xs font-medium ${op.cleaningStatus === 'completed' ? 'text-green-600' : 'text-amber-600'}`}>
                  {op.cleaningStatus === 'completed' ? <><CheckCircle2 className="w-4 h-4" /> Limpio</> : <><AlertCircle className="w-4 h-4" /> Pendiente</>}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="card">
        <div className="flex items-center gap-2 mb-5">
          <Calendar className="w-5 h-5 text-violet-600" />
          <h2 className="text-lg font-bold text-gray-900">Ocupación Próximos 7 Días</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr>
                <th className="text-left pb-3 font-semibold text-gray-500">Piso</th>
                {next7Days.map((_, i) => (
                  <th key={i} className="pb-3 text-center font-semibold text-gray-500 min-w-[40px]">{getDayLabel(i)}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {properties.map((prop) => (
                <tr key={prop.id}>
                  <td className="py-2 font-medium text-gray-900 truncate max-w-[120px]">{prop.name}</td>
                  {occupancyMatrix[prop.id].map((occupied, i) => (
                    <td key={i} className="py-2 text-center">
                      <div className={`w-6 h-6 rounded mx-auto ${occupied ? 'bg-red-400' : 'bg-green-400'}`} title={occupied ? 'Ocupado' : 'Libre'} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex items-center justify-center gap-4 mt-4 text-xs text-gray-500">
          <div className="flex items-center gap-1"><div className="w-3 h-3 rounded bg-green-400" /> Libre</div>
          <div className="flex items-center gap-1"><div className="w-3 h-3 rounded bg-red-400" /> Ocupado</div>
        </div>
      </div>
    </div>
  );
}
