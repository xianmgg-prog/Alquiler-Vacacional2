export const properties = [
  { id: 'prop-001', name: 'Ático Centro', type: 'Ático', location: 'Centro Histórico, Madrid', maxGuests: 4, bedrooms: 2, bathrooms: 1, size: 75, channel: 'Airbnb', channelId: 'airbnb-001', basePrice: 120, cleaningFee: 35, status: 'active' },
  { id: 'prop-002', name: 'Loft Playa', type: 'Loft', location: 'Barceloneta, Barcelona', maxGuests: 2, bedrooms: 1, bathrooms: 1, size: 45, channel: 'Booking.com', channelId: 'bk-002', basePrice: 95, cleaningFee: 25, status: 'active' },
  { id: 'prop-003', name: 'Estudio Universidad', type: 'Estudio', location: 'Salamanca, Madrid', maxGuests: 2, bedrooms: 1, bathrooms: 1, size: 32, channel: 'Airbnb', channelId: 'airbnb-003', basePrice: 65, cleaningFee: 20, status: 'active' },
  { id: 'prop-004', name: 'Dúplex Gran Vía', type: 'Dúplex', location: 'Gran Vía, Madrid', maxGuests: 6, bedrooms: 3, bathrooms: 2, size: 110, channel: 'Booking.com', channelId: 'bk-004', basePrice: 150, cleaningFee: 45, status: 'active' },
  { id: 'prop-005', name: 'Piso Eixample', type: 'Piso', location: 'Eixample, Barcelona', maxGuests: 4, bedrooms: 2, bathrooms: 1, size: 68, channel: 'Airbnb', channelId: 'airbnb-005', basePrice: 110, cleaningFee: 30, status: 'active' },
  { id: 'prop-006', name: 'Casa Rural Sierra', type: 'Casa', location: 'Sierra de Guadarrama', maxGuests: 8, bedrooms: 4, bathrooms: 2, size: 140, channel: 'Booking.com', channelId: 'bk-006', basePrice: 180, cleaningFee: 50, status: 'active' },
  { id: 'prop-007', name: 'Estudio Malasaña', type: 'Estudio', location: 'Malasaña, Madrid', maxGuests: 2, bedrooms: 1, bathrooms: 1, size: 28, channel: 'Airbnb', channelId: 'airbnb-007', basePrice: 70, cleaningFee: 20, status: 'active' },
];

export const performanceData = [
  { propertyId: 'prop-001', occupancyRate: 87, adr: 128.50, monthlyRevenue: 3355.00, monthlyBookings: 26, totalNights: 26, cleaningCost: 910, netProfit: 2445.00 },
  { propertyId: 'prop-002', occupancyRate: 92, adr: 102.00, monthlyRevenue: 2815.20, monthlyBookings: 28, totalNights: 28, cleaningCost: 700, netProfit: 2115.20 },
  { propertyId: 'prop-003', occupancyRate: 76, adr: 68.40, monthlyRevenue: 1558.80, monthlyBookings: 23, totalNights: 23, cleaningCost: 460, netProfit: 1098.80 },
  { propertyId: 'prop-004', occupancyRate: 81, adr: 165.00, monthlyRevenue: 4009.50, monthlyBookings: 25, totalNights: 25, cleaningCost: 1125, netProfit: 2884.50 },
  { propertyId: 'prop-005', occupancyRate: 90, adr: 115.50, monthlyRevenue: 3118.50, monthlyBookings: 27, totalNights: 27, cleaningCost: 810, netProfit: 2308.50 },
  { propertyId: 'prop-006', occupancyRate: 65, adr: 195.00, monthlyRevenue: 3802.50, monthlyBookings: 20, totalNights: 20, cleaningCost: 1000, netProfit: 2802.50 },
  { propertyId: 'prop-007', occupancyRate: 83, adr: 74.20, monthlyRevenue: 1845.80, monthlyBookings: 25, totalNights: 25, cleaningCost: 500, netProfit: 1345.80 },
];

export const todayOperations = [
  { id: 'res-101', propertyId: 'prop-001', guestName: 'María García', type: 'check-in', time: '15:00', cleaningStatus: 'completed', platform: 'Airbnb', nights: 3 },
  { id: 'res-102', propertyId: 'prop-002', guestName: 'John Smith', type: 'check-out', time: '11:00', cleaningStatus: 'pending', platform: 'Booking.com', nights: 5 },
  { id: 'res-103', propertyId: 'prop-004', guestName: 'Ana López', type: 'check-in', time: '16:00', cleaningStatus: 'pending', platform: 'Booking.com', nights: 2 },
  { id: 'res-104', propertyId: 'prop-005', guestName: 'Carlos Ruiz', type: 'check-out', time: '10:30', cleaningStatus: 'completed', platform: 'Airbnb', nights: 4 },
  { id: 'res-105', propertyId: 'prop-007', guestName: 'Laura Martínez', type: 'check-in', time: '14:00', cleaningStatus: 'completed', platform: 'Airbnb', nights: 1 },
];

const generateNext7Days = () => {
  const days = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date();
    d.setDate(d.getDate() + i);
    days.push(d.toISOString().split('T')[0]);
  }
  return days;
};

export const next7Days = generateNext7Days();

export const occupancyMatrix = {
  'prop-001': [true, true, true, false, true, true, false],
  'prop-002': [false, true, true, true, true, false, true],
  'prop-003': [true, false, true, true, false, true, true],
  'prop-004': [true, true, false, false, true, true, true],
  'prop-005': [false, true, true, true, false, false, true],
  'prop-006': [true, true, true, true, true, false, false],
  'prop-007': [true, false, false, true, true, true, true],
};

export const qualityScores = [
  { propertyId: 'prop-001', airbnb: { score: 4.8, totalReviews: 127, cleanliness: 4.9, communication: 4.8, location: 4.9, value: 4.7 }, booking: { score: 9.2, totalReviews: 89, cleanliness: 9.4, staff: 9.1, comfort: 9.3, value: 9.0 } },
  { propertyId: 'prop-002', airbnb: { score: 4.6, totalReviews: 84, cleanliness: 4.7, communication: 4.5, location: 4.8, value: 4.6 }, booking: { score: 8.8, totalReviews: 56, cleanliness: 9.0, staff: 8.7, comfort: 8.9, value: 8.6 } },
  { propertyId: 'prop-003', airbnb: { score: 4.9, totalReviews: 203, cleanliness: 4.9, communication: 4.9, location: 4.8, value: 4.9 }, booking: { score: 9.4, totalReviews: 112, cleanliness: 9.5, staff: 9.4, comfort: 9.3, value: 9.4 } },
  { propertyId: 'prop-004', airbnb: { score: 4.7, totalReviews: 95, cleanliness: 4.6, communication: 4.8, location: 4.9, value: 4.5 }, booking: { score: 9.0, totalReviews: 67, cleanliness: 8.9, staff: 9.1, comfort: 9.2, value: 8.8 } },
  { propertyId: 'prop-005', airbnb: { score: 4.5, totalReviews: 72, cleanliness: 4.6, communication: 4.4, location: 4.7, value: 4.5 }, booking: { score: 8.6, totalReviews: 45, cleanliness: 8.8, staff: 8.5, comfort: 8.7, value: 8.5 } },
  { propertyId: 'prop-006', airbnb: { score: 4.9, totalReviews: 156, cleanliness: 4.9, communication: 4.9, location: 4.8, value: 4.8 }, booking: { score: 9.5, totalReviews: 98, cleanliness: 9.6, staff: 9.4, comfort: 9.5, value: 9.3 } },
  { propertyId: 'prop-007', airbnb: { score: 4.4, totalReviews: 58, cleanliness: 4.5, communication: 4.3, location: 4.6, value: 4.5 }, booking: { score: 8.4, totalReviews: 34, cleanliness: 8.5, staff: 8.3, comfort: 8.6, value: 8.4 } },
];

export const revenueHistory = {
  labels: ['Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto'],
  datasets: [{ label: 'Ingresos Totales (€)', data: [18500, 21200, 24800, 28900, 32400, 35800], borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', fill: true, tension: 0.4 }],
};

export const channelDistribution = {
  labels: ['Airbnb', 'Booking.com'],
  datasets: [{ data: [58, 42], backgroundColor: ['#ff5a5f', '#003580'], borderWidth: 0 }],
};

export const getPropertyById = (id) => properties.find(p => p.id === id);

export const globalKPIs = {
  totalRevenueMTD: performanceData.reduce((sum, p) => sum + p.monthlyRevenue, 0),
  totalNetProfit: performanceData.reduce((sum, p) => sum + p.netProfit, 0),
  avgOccupancy: Math.round(performanceData.reduce((sum, p) => sum + p.occupancyRate, 0) / performanceData.length),
  avgADR: (performanceData.reduce((sum, p) => sum + p.adr, 0) / performanceData.length).toFixed(2),
  totalBookings: performanceData.reduce((sum, p) => sum + p.monthlyBookings, 0),
  totalProperties: properties.length,
};
