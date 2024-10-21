import { useState } from 'react';
import SymptomFilterComponent from '../components/SymptomFilterComponent';

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

  return (
    <div>
      <SymptomFilterComponent onFilter={handleFilter} />

      {loading && <p>Loading...</p>}

      {filteredData.length > 0 && (
        <div>
          <h2>Filtered Symptoms</h2>
          <table>
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
                  <td>{item.average_severity.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default SymptomFilter;
