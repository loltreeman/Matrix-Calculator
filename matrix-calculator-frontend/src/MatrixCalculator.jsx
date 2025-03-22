import React, { useState } from "react";
import axios from "axios";
import Fraction from "fraction.js";
import "bootstrap/dist/css/bootstrap.min.css";

const API_URL = process.env.REACT_APP_API_URL || "https://trix-matrix-calculator.up.railway.app/";

export default function MatrixCalculator() {
  const [matrixA, setMatrixA] = useState("2, 1, -1; 1, 3, 2; 1, -1, 2");
  const [matrixB, setMatrixB] = useState("1, 0, 2; 0, 1, -1; -1, 2, 1");
  const [operation, setOperation] = useState("add");
  const [scalar, setScalar] = useState(2); // This is only for scalar multiplication
  const [result, setResult] = useState(null);
  const [solutionStatus, setSolutionStatus] = useState("");
  const [showFractions, setShowFractions] = useState(false);


  const getMatrixSize = (matrixStr) => {
    if (!matrixStr.trim()) return "0x0";
  
    const rows = matrixStr.split(";").map(row => row.trim()).filter(row => row !== "");
    const numRows = rows.length;
    
    if (numRows === 0) return "0x0";
  
    const numCols = rows[0].split(",").map(col => col.trim()).filter(col => col !== "").length;
    
    // Check for inconsistent column count across rows
    if (!rows.every(row => row.split(",").map(col => col.trim()).filter(col => col !== "").length === numCols)) {
      return "Error: Inconsistent row lengths";
    }
  
    return `${numRows}x${numCols}`;
  };
  

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
            requestData.scalar = parseFloat(scalar);  
        } else if (operation !== "scalar") {
            requestData.matrixB = matrixB; 
        }

        const response = await axios.post(`${API_URL}matrix/calculate/`, requestData);
        console.log("Full API Response:", response.data);
        
        setResult(response.data.result);
        setSolutionStatus(response.data.solution_status); // This is to store solution status
    } catch (error) {
        console.error("Error calculating:", error);
        setResult(generateUndefinedMatrix(matrixA));
        setSolutionStatus("Error calculating matrix");
    }
};

  const renderMatrix = (matrix) => {
    return (
      <table className="table table-bordered text-center">
        <tbody>
          {matrix.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((value, colIndex) => (
                <td key={colIndex}>
                  {showFractions
                    ? new Fraction(value).toFraction(true)
                    : value}
                </td>
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
              Matrix A (comma-separated, ; for new row) - Size: {getMatrixSize(matrixA)}
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
            <label className="form-label">
              Matrix B (if needed) - Size: {getMatrixSize(matrixB)}
            </label>
            <textarea
              className="form-control"
              rows="3"
              value={matrixB}
              onChange={(e) => setMatrixB(e.target.value)}
            />
          </div>


          {/* This is where the user can select the scalar operations. */}
          {operation === "scalar" && (
            <div className="mb-3">
              <label className="form-label">Scalar Value</label>
              <input
                type="number"
                className="form-control"
                value={scalar}
                onChange={(e) => setScalar(e.target.value)}
              />
            </div>
          )}

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

      {/* This is a checkbox to toggle fractions */}
      <div className="form-check mb-3">
            <input
              className="form-check-input"
              type="checkbox"
              id="showFractions"
              checked={showFractions}
              onChange={(e) => setShowFractions(e.target.checked)}
            />
            <label className="form-check-label" htmlFor="showFractions">
              Display results as fractions
            </label>
          </div>

          <button className="btn btn-primary w-100" onClick={handleCalculate}>
            Calculate
          </button>

          {result && Array.isArray(result) && (
            <div className="mt-4">
              <h4 className="text-center">Result</h4>
              {renderMatrix(result)}
            </div>
          )}

      {/* This is to display Solution Status */}
      {solutionStatus && (
            <div className="alert alert-info mt-3 text-center">
              {solutionStatus === "unique" && "The system has a unique solution."}
              {solutionStatus === "infinite" && "The system has infinitely many solutions."}
              {solutionStatus === "none" && "The system has no solution."}
              {/* Otherwise, display the raw message */}
              {solutionStatus !== "unique" && solutionStatus !== "infinite" && solutionStatus !== "none" && solutionStatus}
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
