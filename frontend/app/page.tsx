"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import axios from "axios";

const HomePage = () => {
  const [users, setUsers] = useState([]);
  const [checkins, setCheckins] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [treatments, setTreatments] = useState([]);
  const [tags, setTags] = useState([]);
  const [weather, setWeather] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [usersResponse, checkinsResponse, symptomsResponse, treatmentsResponse, tagsResponse, weatherResponse] = await Promise.all([
          axios.get('http://localhost:8000/users'),
          axios.get('http://localhost:8000/checkins'),
          axios.get('http://localhost:8000/symptoms'),
          axios.get('http://localhost:8000/treatments'),
          axios.get('http://localhost:8000/tags'),
          axios.get('http://localhost:8000/weather'),
        ]);

        setUsers(usersResponse.data);
        setCheckins(checkinsResponse.data);
        setSymptoms(symptomsResponse.data);
        setTreatments(treatmentsResponse.data);
        setTags(tagsResponse.data);
        setWeather(weatherResponse.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h1>User List</h1>
      <Table data={users} headers={['ID', 'Age', 'Sex', 'Country']} rowKeys={['user_id', 'age', 'sex', 'country']} />

      <h1>CheckIn List</h1>
      <Table data={checkins} headers={['ID', 'User ID', 'Date']} rowKeys={['checkin_id', 'user_id', 'date']} />

      <h1>Symptom List</h1>
      <Table data={symptoms} headers={['ID', 'CheckIn ID', 'Name', 'Severity']} rowKeys={['symptom_id', 'checkin_id', 'symptom_name', 'severity']} />

      <h1>Treatment List</h1>
      <Table data={treatments} headers={['ID', 'CheckIn ID', 'Name']} rowKeys={['treatment_id', 'checkin_id', 'treatment_name']} />

      <h1>Tag List</h1>
      <Table data={tags} headers={['ID', 'CheckIn ID', 'Name']} rowKeys={['tag_id', 'checkin_id', 'tag_name']} />

      <h1>Weather List</h1>
      <Table data={weather} headers={['ID', 'CheckIn ID', 'Description', 'Temperature', 'Humidity', 'Pressure']} rowKeys={['weather_id', 'checkin_id', 'description', 'temperature', 'humidity', 'pressure']} />
    </div>
  );
};

// Table component for rendering tabular data
const Table = ({ data, headers, rowKeys }) => (
  <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
    <thead>
      <tr>
        {headers.map((header, index) => (
          <th key={index} style={{ border: '1px solid #ddd', padding: '8px', background: '#f2f2f2', color: 'black' }}>{header}</th>
        ))}
      </tr>
    </thead>
    <tbody>
      {data.length > 0 ? (
        data.map((row, index) => (
          <tr key={index} style={{ border: '1px solid #ddd' }}>
            {rowKeys.map((key, i) => (
              <td key={i} style={{ border: '1px solid #ddd', padding: '8px', color: 'black' }}>{row[key]}</td>
            ))}
          </tr>
        ))
      ) : (
        <tr>
          <td colSpan={headers.length} style={{ textAlign: 'center', padding: '8px', color: 'black' }}>No data available</td>
        </tr>
      )}
    </tbody>
  </table>
);

export default HomePage;
