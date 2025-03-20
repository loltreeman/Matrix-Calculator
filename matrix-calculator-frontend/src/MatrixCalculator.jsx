import { useState } from "react";
import React from "react";
import axios from "axios";

export default function MatrixCalculator() {
  const [matrixA, setMatrixA] = useState("2,1,-1;1,3,2;1,-1,2");
  const [matrixB, setMatrixB] = useState("1,0,2;0,1,-1;-1,2,1");
  const [operation, setOperation] = useState("add");
  const [result, setResult] = useState(null);

  const handleCalculate = async () => {
    try {
      const response = await axios.post("http://localhost:5000/calculate", {
        matrixA,
        matrixB,
        operation,
      });
      setResult(response.data.result);
    } catch (error) {
      console.error("Error calculating:", error);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded-lg shadow-md">
      <h1 className="text-xl font-bold mb-4">Matrix Calculator</h1>
      <div>
        <label className="block">Matrix A (comma-separated, ; for new row)</label>
        <textarea
          className="w-full p-2 border rounded"
          value={matrixA}
          onChange={(e) => setMatrixA(e.target.value)}
        />
      </div>
      <div>
        <label className="block">Matrix B (if needed)</label>
        <textarea
          className="w-full p-2 border rounded"
          value={matrixB}
          onChange={(e) => setMatrixB(e.target.value)}
        />
      </div>
      <div>
        <label className="block">Operation</label>
        <select
          className="w-full p-2 border rounded"
          value={operation}
          onChange={(e) => setOperation(e.target.value)}
        >
          <option value="add">Addition</option>
          <option value="subtract">Subtraction</option>
          <option value="scalar">Scalar Multiplication</option>
          <option value="gauss">Gaussian Elimination</option>
          <option value="jordan">Gauss-Jordan Elimination</option>
        </select>
      </div>
      <button
        className="w-full mt-4 bg-blue-500 text-white p-2 rounded"
        onClick={handleCalculate}
      >
        Calculate
      </button>
      {result && (
        <div className="mt-4 p-2 bg-gray-100 rounded">
          <h2 className="font-bold">Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
