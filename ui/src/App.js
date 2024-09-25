import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('https://your-api-endpoint.amazonaws.com/dev/sensor-data');
        const data = await response.json();
        setSensorData(data.Items); // Adjust based on your API's response
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>IoT Sensor Data Dashboard</h1>
      {sensorData.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Device ID</th>
              <th>Timestamp</th>
              <th>Temperature (°C)</th>
              <th>Humidity (%)</th>
              {/* Add other sensor fields as needed */}
            </tr>
          </thead>
          <tbody>
            {sensorData.map((data, index) => (
              <tr key={index}>
                <td>{data.device_id}</td>
                <td>{data.timestamp}</td>
                <td>{data.temperature}</td>
                <td>{data.humidity}</td>
                {/* Add other sensor fields as needed */}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No sensor data available.</p>
      )}
    </div>
  );
}

export default App;