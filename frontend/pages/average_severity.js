import { useEffect, useState } from 'react';
import AverageSeverityChart from '../components/AverageSeverityChart';
import Link from 'next/link';
import styles from '../styles/Charts.module.css';

const AverageSeverity = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/average_symptom_severity/');
        const result = await response.json();
        setData(result);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className={styles.loading}>Loading...</div>;
  if (error) return <div className={styles.error}>Error fetching data: {error.message}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Average Symptom Severity</h1>
      <div className={styles.content}>
        <div className={styles.chartWrapper}>
          <AverageSeverityChart data={data} />
        </div>
      </div>
      <nav className={styles.nav}>
        <Link href="/" className={styles.navLink}>Home</Link>
      </nav>
    </div>
  );
};

export default AverageSeverity;
