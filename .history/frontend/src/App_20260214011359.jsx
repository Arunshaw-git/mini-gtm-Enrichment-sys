import React, { useState, useEffect } from "react";
import CsvUpload from "./components/CsvUpload";
import CompanyTable from "./components/CompanyTable";
import axios from "axios";

export default function App() {
  const [companies, setCompanies] = useState([]);

  // Fetch all companies from backend
  const fetchCompanies = async () => {
    try {
      const res = await axios.get("http://localhost:8000/companies");
      setCompanies(res.data);
    } catch (err) {
      console.error("Error fetching companies:", err);
    }
  };

  useEffect(() => {
    fetchCompanies();
    const interval = setInterval(fetchCompanies, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Company Enrichment</h1>
      <CsvUpload onUploadComplete={fetchCompanies} />
      <CompanyTable companies={companies} />
    </div>
  );
}