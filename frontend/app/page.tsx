"use client";

import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';

export default function Page() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  // State for filters
  const [startDate, setStartDate] = useState('2016-06-01');
  const [endDate, setEndDate] = useState('2016-07-31');
  const [ageGroup, setAgeGroup] = useState('25-34');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/average_symptom_severity/?startDate=${startDate}&endDate=${endDate}&ageGroup=${ageGroup}`);
        const result = await response.json();
        setData(result);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data: ", error);
      }
    };

    fetchData();
  }, [startDate, endDate, ageGroup]); // Adding dependencies to re-fetch data when filters change

  const chartData = {
    labels: data.map(entry => entry.date),
    datasets: [
      {
        label: 'Average Symptom Severity',
        data: data.map(entry => entry.average_severity),
        fill: false,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
      },
    ],
  };

  return (
    <div>
      <h1>Average Symptom Severity Over Time</h1>

      {/* Filter control elements */}
      <div>
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <label>
          Age Group:
          <select value={ageGroup} onChange={(e) => setAgeGroup(e.target.value)}>
            <option value="18-24">18-24</option>
            <option value="25-34">25-34</option>
            <option value="35-44">35-44</option>
            <option value="45-54">45-54</option>
            <option value="55+">55+</option>
          </select>
        </label>
        <button onClick={() => setLoading(true)}>Apply Filters</button> {/* Button to apply filters */}
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <Line data={chartData} options={{
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Average Severity',
              },
            },
            x: {
              title: {
                display: true,
                text: 'Date',
              },
            },
          },
        }} />
      )}
    </div>
  );
}
