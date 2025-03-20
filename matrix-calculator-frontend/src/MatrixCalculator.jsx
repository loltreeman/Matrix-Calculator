import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const API_URL = process.env.REACT_APP_API_URL || "https://trix-matrix-calculator.up.railway.app/";

export default function MatrixCalculator() {
  const [matrixA, setMatrixA] = useState("2, 1, -1; 1, 3, 2; 1, -1, 2");
  const [matrixB, setMatrixB] = useState("1, 0, 2; 0, 1, -1; -1, 2, 1");
  const [operation, setOperation] = useState("add");
  const [result, setResult] = useState(null);

  // This is a helper method to generate an "undefined" matrix with the same dimensions as matrixA input
  const generateUndefinedMatrix = (matrixStr) => {
    const rows = matrixStr.split(";");
    return rows.map((row) => {
      const cols = row.split(",");
      return cols.map(() => "undefined");
    });
  };

  const handleCalculate = async () => {
    try {
        const requestData = { matrixA, operation };

        if (operation === "scalar") {
            requestData.scalar = parseFloat(scalar); // Send scalar value
        } else if (operation !== "scalar") {
            requestData.matrixB = matrixB; // Send matrixB for add, subtract, and multiply
        }

        const response = await axios.post(`${API_URL}matrix/calculate/`, requestData);
        console.log("Full API Response:", response.data);
        setResult(response.data.result);
        } catch (error) {
        console.error("Error calculating:", error);
        setResult(generateUndefinedMatrix(matrixA));
        }
    };

  const renderMatrix = (matrix) => {
    return (
      <table className="table table-bordered text-center">
        <tbody>
          {matrix.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((value, colIndex) => (
                <td key={colIndex}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div
      className="container mt-4"
      style={{ fontFamily: "'Open Sans', sans-serif" }}
    >
      {/* This is the navbar where it will display Matrix Calculator */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-fluid justify-content-center">
          <span className="navbar-brand display-4">Matrix Calculator</span>
        </div>
      </nav>

      {/* This is where the matrix calculator will be shown */}
      <div className="card mt-4 shadow">
        <div className="card-body">
          <h2 className="card-title text-center mb-4">Matrix Operations</h2>

          {/* This is where the user will input Matrix A */}
          <div className="mb-3">
            <label className="form-label">
              Matrix A (comma-separated, ; for new row)
            </label>
            <textarea
              className="form-control"
              rows="3"
              value={matrixA}
              onChange={(e) => setMatrixA(e.target.value)}
            />
          </div>

          {/* This is where the user will input Matrix B */}
          <div className="mb-3">
            <label className="form-label">Matrix B (if needed)</label>
            <textarea
              className="form-control"
              rows="3"
              value={matrixB}
              onChange={(e) => setMatrixB(e.target.value)}
            />
          </div>

          {/* This is where the user can select the operations. */}
          <div className="mb-3">
            <label className="form-label">Operation</label>
            <select
              className="form-select"
              value={operation}
              onChange={(e) => setOperation(e.target.value)}
            >
              <option value="add">Addition</option>
              <option value="subtract">Subtraction</option>
              <option value="scalar">Scalar Multiplication</option>
              <option value="multiply">Matrix Multiplication</option>
              <option value="gauss">Gaussian Elimination</option>
              <option value="jordan">Gauss-Jordan Elimination</option>
            </select>
          </div>

          {/* This is the button to press calculate */}
          <button className="btn btn-primary w-100" onClick={handleCalculate}>
            Calculate
          </button>

          {/* This is where the results section will be displayed */}
          {result && Array.isArray(result) && (
            <div className="mt-4">
              <h4 className="text-center">Result</h4>
              {renderMatrix(result)}
            </div>
          )}
        </div>
      </div>

        {/* The footer where I would put hyperlinks because cloutchaser ako eme */}
        <footer className="mt-4 text-center py-3 bg-light">
        <div>
        <a
            href="https://github.com/loltreeman/Matrix-Calculator"  
            target="_blank"
            rel="noopener noreferrer"
            className="mx-2 text-decoration-none"
        >
            GitHub Repo
        </a>
        |
        <a
            href="https://x.com/trixtaos"  
            target="_blank"
            rel="noopener noreferrer"
            className="mx-2 text-decoration-none"
        >
            Twitter
        </a>
        </div>
        <small className="text-muted">© 2025 Trixtao </small>
    </footer>
    </div>
  );
}
