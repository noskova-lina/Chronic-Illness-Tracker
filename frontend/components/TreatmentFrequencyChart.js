import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Регистрация необходимых компонентов Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const TreatmentFrequencyChart = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.treatment_name), // Используем treatment_name как метки
    datasets: [
      {
        label: 'Frequency',
        data: data.map(item => item.frequency), // Используем frequency как данные
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default TreatmentFrequencyChart;
