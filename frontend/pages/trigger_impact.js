import { useEffect, useState } from 'react';
import TriggerImpactChart from '../components/TriggerImpactChart';
import Link from 'next/link';
import styles from '../styles/Charts.module.css';

const TriggerImpact = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/trigger_impact/');
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
      <h1 className={styles.title}>Trigger Impact on Severity</h1>
      <div className={styles.content}>
        <div className={styles.chartWrapper}>
          <TriggerImpactChart data={data} />
        </div>
      </div>
      <nav className={styles.nav}>
        <Link href="/" className={styles.navLink}>Home</Link>
      </nav>
    </div>
  );
};

export default TriggerImpact;
