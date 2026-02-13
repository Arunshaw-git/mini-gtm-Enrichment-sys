import React from "react";

export default function CompanyTable({ companies }) {
  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "20px",
      }}
    >
      <thead>
        <tr>
          <th style={{ border: "1px solid #ddd", padding: "8px" }}>Domain</th>
          <th style={{ border: "1px solid #ddd", padding: "8px" }}>Industry</th>
          <th style={{ border: "1px solid #ddd", padding: "8px" }}>Company Size</th>
          <th style={{ border: "1px solid #ddd", padding: "8px" }}>Revenue Range</th>
          <th style={{ border: "1px solid #ddd", padding: "8px" }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {companies.map((c) => (
          <tr key={c.id}>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>{c.domain}</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>{c.industry || "-"}</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>{c.company_size || "-"}</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>{c.revenue_range || "-"}</td>
            <td style={{ border: "1px solid #ddd", padding: "8px" }}>{c.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}