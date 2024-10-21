import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const TriggerImpactChart = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.trigger),
    datasets: [
      {
        label: 'Average Severity',
        data: data.map(item => item.average_severity),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Average Severity',
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default TriggerImpactChart;
