'use client';
import { Line, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement, Filler } from 'chart.js';
import { revenueHistory, channelDistribution } from '@/data/mockData';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler);

export function RevenueChart() {
  const options = {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { callbacks: { label: (ctx) => `€${ctx.parsed.y.toLocaleString('es-ES')}` } } },
    scales: { y: { beginAtZero: true, grid: { color: '#f3f4f6' }, ticks: { callback: (val) => `€${val / 1000}k` } }, x: { grid: { display: false } } },
  };
  return <div className="h-64"><Line data={revenueHistory} options={options} /></div>;
}

export function ChannelChart() {
  const options = { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20 } } }, cutout: '65%' };
  return <div className="h-64 flex items-center justify-center"><Doughnut data={channelDistribution} options={options} /></div>;
}
