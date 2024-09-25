import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    // Fetch historical data from your backend API
    axios.get('/api/sensor-data')
      .then(response => {
        setSensorData(response.data);
      })
      .catch(error => {
        console.error('Error fetching sensor data:', error);
      });
  }, []);

  return (
    <div className="App">
      <h1>IoT Sensor Data Dashboard</h1>
      <table>
        <thead>
          <tr>
            <th>Device ID</th>
            <th>Timestamp</th>
            <th>Temperature (°C)</th>
            <th>Humidity (%)</th>
            {/* Add other sensor fields */}
          </tr>
        </thead>
        <tbody>
          {sensorData.map((data, index) => (
            <tr key={index}>
              <td>{data.device_id}</td>
              <td>{data.timestamp}</td>
              <td>{data.temperature}</td>
              <td>{data.humidity}</td>
              {/* Add other sensor fields */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;