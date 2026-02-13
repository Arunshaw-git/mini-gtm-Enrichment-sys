// App.jsx
import { useState, useEffect } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch all companies
  const fetchCompanies = async () => {
    try {
      const res = await fetch("http://localhost:8000/companies");
      const data = await res.json();
      setCompanies(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCompanies();
    // Optionally poll every 5-10 seconds to update statuses
    const interval = setInterval(fetchCompanies, 5000);
    return () => clearInterval(interval);
  }, []);

  // Handle CSV file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Upload CSV
  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload-csv", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("Uploaded:", data);
      setFile(null);
      fetchCompanies(); // refresh list
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Company Enrichment</h1>

      {/* CSV Upload */}
      <div style={{ marginBottom: 20 }}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? "Uploading..." : "Upload CSV"}
        </button>
      </div>

      {/* Companies Table */}
      <table border="1" cellPadding="10" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>Domain</th>
            <th>Industry</th>
            <th>Company Size</th>
            <th>Revenue Range</th>
            <th>Status</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {companies.map((c) => (
            <tr key={c.id}>
              <td>{c.domain}</td>
              <td>{c.industry || "-"}</td>
              <td>{c.company_size || "-"}</td>
              <td>{c.revenue_range || "-"}</td>
              <td>{c.status}</td>
              <td>{new Date(c.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}