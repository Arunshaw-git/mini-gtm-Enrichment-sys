import React, { useState } from "react";
import Papa from "papaparse";
import axios from "axios";

export default function CsvUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!file) return alert("Please select a CSV file.");

    setLoading(true);

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: async function (results) {
        // Extract domains
        const domains = results.data.map((row) => row.domain).filter(Boolean);

        if (domains.length === 0) {
          alert("No valid domains found in CSV.");
          setLoading(false);
          return;
        }

        try {
          await axios.post("http://localhost:8000/upload-csv", { domains });
          onUploadComplete(); // refresh table
        } catch (err) {
          console.error("Error submitting CSV:", err);
          alert("Upload failed.");
        } finally {
          setLoading(false);
        }
      },
    });
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading} style={{ marginLeft: "10px" }}>
        {loading ? "Uploading..." : "Upload CSV"}
      </button>
    </div>
  );
}