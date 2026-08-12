'use client';
import { Star, ThumbsUp, Sparkles, MessageCircle, Sofa } from 'lucide-react';
import { qualityScores, getPropertyById } from '@/data/mockData';

export default function QualityBlock() {
  const avgAirbnb = (qualityScores.reduce((sum, q) => sum + q.airbnb.score, 0) / qualityScores.length).toFixed(2);
  const avgBooking = (qualityScores.reduce((sum, q) => sum + q.booking.score, 0) / qualityScores.length).toFixed(1);

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Star className="w-5 h-5 text-amber-500" />
          <h2 className="text-lg font-bold text-gray-900">Calidad y Reseñas</h2>
        </div>
        <div className="flex gap-4 text-sm">
          <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-500" /><span className="font-bold text-gray-900">{avgAirbnb}</span><span className="text-gray-500">Airbnb</span></div>
          <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-700" /><span className="font-bold text-gray-900">{avgBooking}</span><span className="text-gray-500">Booking</span></div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {qualityScores.map((q) => {
          const prop = getPropertyById(q.propertyId);
          return (
            <div key={q.propertyId} className="border border-gray-100 rounded-lg p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900 text-sm truncate">{prop.name}</h3>
                <span className={`badge text-xs ${prop.channel === 'Airbnb' ? 'bg-rose-50 text-rose-700' : 'bg-blue-50 text-blue-700'}`}>{prop.channel}</span>
              </div>
              <div className="flex items-baseline gap-2 mb-3">
                <span className="text-2xl font-bold text-gray-900">{prop.channel === 'Airbnb' ? q.airbnb.score : q.booking.score}</span>
                <span className="text-sm text-gray-400">/{prop.channel === 'Airbnb' ? '5' : '10'}</span>
                <span className="text-xs text-gray-400 ml-auto">{prop.channel === 'Airbnb' ? q.airbnb.totalReviews : q.booking.totalReviews} reseñas</span>
              </div>
              <div className="space-y-2">
                {prop.channel === 'Airbnb' ? (
                  <>
                    <ScoreBar icon={Sparkles} label="Limpieza" value={q.airbnb.cleanliness} max={5} color="bg-rose-500" />
                    <ScoreBar icon={MessageCircle} label="Comunicación" value={q.airbnb.communication} max={5} color="bg-rose-500" />
                    <ScoreBar icon={ThumbsUp} label="Ubicación" value={q.airbnb.location} max={5} color="bg-rose-500" />
                    <ScoreBar icon={Sofa} label="Relación calidad" value={q.airbnb.value} max={5} color="bg-rose-500" />
                  </>
                ) : (
                  <>
                    <ScoreBar icon={Sparkles} label="Limpieza" value={q.booking.cleanliness} max={10} color="bg-blue-600" />
                    <ScoreBar icon={MessageCircle} label="Personal" value={q.booking.staff} max={10} color="bg-blue-600" />
                    <ScoreBar icon={Sofa} label="Confort" value={q.booking.comfort} max={10} color="bg-blue-600" />
                    <ScoreBar icon={ThumbsUp} label="Relación calidad" value={q.booking.value} max={10} color="bg-blue-600" />
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ScoreBar({ icon: Icon, label, value, max, color }) {
  const percentage = (value / max) * 100;
  return (
    <div className="flex items-center gap-2">
      <Icon className="w-3.5 h-3.5 text-gray-400 shrink-0" />
      <span className="text-xs text-gray-500 w-24 shrink-0">{label}</span>
      <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${percentage}%` }} />
      </div>
      <span className="text-xs font-medium text-gray-700 w-6 text-right">{value}</span>
    </div>
  );
}
