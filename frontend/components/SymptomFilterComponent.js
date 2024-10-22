import { useState, useRef } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import styles from '../styles/SymptomFilter.module.css';

const SymptomFilterComponent = ({ onFilter }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const endDateRef = useRef(null);

  const handleFilterClick = () => {
    if (!startDate || !endDate) {
      alert('Please select both start and end dates');
      return;
    }

    const start = startDate.toISOString().split('T')[0];
    const end = endDate.toISOString().split('T')[0];

    onFilter(start, end);
  };

  const handleKeyDown = (event, nextFieldRef) => {
    if (event.key === 'Enter' && nextFieldRef.current) {
      nextFieldRef.current.setFocus();
    }
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
          onKeyDown={(event) => handleKeyDown(event, endDateRef)}
        />
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <label>End Date: </label>
        <DatePicker
          selected={endDate}
          onChange={(date) => setEndDate(date)}
          dateFormat="yyyy-MM-dd"
          ref={endDateRef}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              handleFilterClick();
            }
          }}
        />
      </div>

      <button onClick={handleFilterClick} className={styles.button}>Filter Symptoms</button>
    </div>
  );
};

export default SymptomFilterComponent;
