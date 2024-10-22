import { useState } from 'react';
import SymptomFilterComponent from '../components/SymptomFilterComponent';
import { Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import styles from '../styles/SymptomFilter.module.css';
import Link from 'next/link';

Chart.register(...registerables);

const SymptomFilter = () => {
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFilter = async (startDate, endDate) => {
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/filtered_symptoms?start_date=${startDate}&end_date=${endDate}`
      );
      const result = await response.json();
      setFilteredData(result);
    } catch (error) {
      console.error('Error fetching filtered symptoms:', error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = {
    labels: filteredData.map(item => item.symptom),
    datasets: [
      {
        label: 'Average Severity',
        data: filteredData.map(item => item.average_severity),
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Symptom Filter</h1>
      <SymptomFilterComponent onFilter={handleFilter} />

      {loading && <div className={styles.loading}>Loading...</div>}

      {filteredData.length > 0 && (
        <div className={styles.content}>
          <div className={styles.tableWrapper}>
            <h2>Filtered Symptoms</h2>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Symptom</th>
                  <th>Average Severity</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((item, index) => (
                  <tr key={index}>
                    <td>{item.date}</td>
                    <td>{item.symptom}</td>
                    <td>{item.average_severity ? item.average_severity.toFixed(2) : 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className={styles.chartWrapper}>
            <h2>Severity Chart</h2>
            <Bar data={chartData} options={{ responsive: true }} />
          </div>
        </div>
      )}

      <nav className={styles.nav}>
        <Link href="/" className={styles.navLink}>Home</Link>
      </nav>
    </div>
  );
};

export default SymptomFilter;
