import { useEffect, useState } from 'react';
import TriggerImpactChart from '../components/TriggerImpactChart';

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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error fetching data: {error.message}</div>;

  return (
    <div>
      <h1>Trigger Impact on Severity</h1>
      <TriggerImpactChart data={data} />
    </div>
  );
};

export default TriggerImpact;
