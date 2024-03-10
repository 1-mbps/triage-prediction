import React, { useState } from 'react';
import './App.css';

const App: React.FC = () => {
  const [formData, setFormData] = useState({
    'age': '',
    'sex': '',
    'arrems': '',
    'tempf': '',
    'pulse': '',
    'respr': '',
    'bpsys': '',
    'bpdias': '',
    'popct': '',
    'cebvd': '',
    'eddial': '',
    'chf': '',
    'alzhd': '',
    'diabetes': '',
    'cad': '',
    'edhiv': '',
    'nochron': ''
  });
  const [prediction, setPrediction] = useState<number | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      alert(JSON.stringify(formData))
      // Send data to Flask backend
      const response = await fetch('http://localhost:3000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      setPrediction(result.prediction);
    } catch (error) {
      alert(error);
      // console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <label>
          Age:
          <input
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
          />
        </label>
        <br />
        <label>
          Sex:
          <input
            type="radio"
            name="radioOption"
            value="0"
            checked={formData.sex === '0'}
            onChange={() => setFormData({ ...formData, sex: '0' })}
          />
          Male
          <input
            type="radio"
            name="radioOption"
            value="1"
            checked={formData.sex === '1'}
            onChange={() => setFormData({ ...formData, sex: '1' })}
          />
          Female
        </label>
        {/* Unfinished: add the rest of the fields */}
        <br />
        <button type="submit">Predict</button>
      </form>
      {prediction !== null && <p>Prediction: {prediction}</p>}
    </div>
  );
};

export default App;
