import { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const SymptomFilterComponent = ({ onFilter }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleFilterClick = () => {
    if (!startDate || !endDate) {
      alert('Please select both start and end dates');
      return;
    }

    // Convert dates to string format (YYYY-MM-DD)
    const start = startDate.toISOString().split('T')[0];
    const end = endDate.toISOString().split('T')[0];

    // Invoke callback passed from parent component to handle API call
    onFilter(start, end);
  };

  return (
    <div>
      <h2>Filter Symptoms by Date Range</h2>

      <div style={{ marginBottom: '1rem' }}>
        <label>Start Date: </label>
        <DatePicker
          selected={startDate}
          onChange={(date) => setStartDate(date)}
          dateFormat="yyyy-MM-dd"
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>End Date: </label>
        <DatePicker
          selected={endDate}
          onChange={(date) => setEndDate(date)}
          dateFormat="yyyy-MM-dd"
        />
      </div>

      <button onClick={handleFilterClick}>Filter Symptoms</button>
    </div>
  );
};

export default SymptomFilterComponent;
