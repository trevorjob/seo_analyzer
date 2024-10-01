import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/api/analyze/", {
        url,
      });
      setResult(response.data);
    } catch (err) {
      setError("An error occurred while fetching data.");
      setLoading(false);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  const renderOgTags = (ogTags) => {
    return Object.entries(ogTags).map(([key, value]) => (
      <li key={key}>
        <strong>{key}:</strong> {value}
      </li>
    ));
  };

  return (
    <div className="container mx-auto p-5">
      <h2>PLEASE BE PATIENT AS IT TAKES A WHILE TO COMPLETE THE ANALYSIS</h2>
      <h1 className="text-3xl font-bold">SEO Analyzer</h1>
      <form onSubmit={handleSubmit} className="mt-4">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL to analyze"
          required
          className="border rounded p-2 mr-2"
        />
        <button
          type="submit"
          className={`bg-blue-500 text-white rounded p-2 ${
            loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
          disabled={loading} // Disable button when loading
        >
          {loading ? "Analyzing..." : "Analyze"} {/* Conditional button text */}
        </button>
      </form>

      {error && <div className="mt-4 text-red-500">{error}</div>}
      {result && (
        <h2>
          <strong>Overall SEO Score:</strong> {result.seo_score} / 100
        </h2>
      )}
      {result && (
        <div className="mt-4 bg-gray-100 p-4 rounded">
          <h2 className="text-xl font-semibold">Analysis Results:</h2>
          <p>
            <strong>Page Title:</strong> {result.report.title}
          </p>
          <p>
            <strong>Meta Description:</strong> {result.report.meta_description}
          </p>
          <p>
            <strong>Canonical URL:</strong> {result.report.canonical_url}
          </p>
          <p>
            <strong>Favicon Present:</strong>{" "}
            {result.report.favicon_present ? "Yes" : "No"}
          </p>
          <p>
            <strong>Mobile Friendly:</strong>{" "}
            {result.report.mobile_friendly ? "Yes" : "No"}
          </p>
          <p>
            <strong>Noindex Tag:</strong>{" "}
            {result.report.noindex_tag ? "Yes" : "No"}
          </p>
          <p>
            <strong>SSL Certificate:</strong>{" "}
            {result.report.ssl_certificate ? "Yes" : "No"}
          </p>
          <p>
            <strong>Robots.txt Present:</strong>{" "}
            {result.report.robots_txt ? "Yes" : "No"}
          </p>
          <p>
            <strong>Image Alt Tags:</strong> {result.report.image_alt_tags}
          </p>
          <p>
            <strong>Images Without Alt Tags:</strong>{" "}
            {result.report.images_without_alt}
          </p>
          <p>
            <strong>Page Speed:</strong> {result.report.page_speed_ms} ms
          </p>

          <p>
            <strong>Keyword Density:</strong>{" "}
            {result.report.keyword_density || "Not Available"}
          </p>
          <p>
            <strong>Broken Links:</strong> {result.report.broken_links}
          </p>
          <p>
            <strong>Headings:</strong>{" "}
            {result.report.headings.length > 0
              ? result.report.headings.join(", ")
              : "No headings found"}
          </p>
          <p>
            <strong>Hreflang Tags:</strong>{" "}
            {result.report.hreflang_tags.length > 0
              ? result.report.hreflang_tags.join(", ")
              : "No hreflang tags found"}
          </p>
          <p>
            <strong>Open Graph Tags:</strong>{" "}
            <ul className="list-disc pl-5">
              {result.report.og_tags ? (
                renderOgTags(result.report.og_tags)
              ) : (
                <li>No Open Graph tags found</li>
              )}
            </ul>
          </p>
        </div>
      )}
    </div>
  );
};

export default App;
