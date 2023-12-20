// SearchResults.js
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Button, Table, Container } from "react-bootstrap";
import BookButton from "./BookButton";
import MyBookings from "./MyBookings";

const SearchResults = ({ searchDeparture, searchArrival }) => {
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState([]);

  const fetchSearchResults = async () => {
    try {
      setLoading(true);

      const response = await fetch(
        `http://localhost:5000/search-results?departure=${searchDeparture}&arrival=${searchArrival}`,
        {
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch search results");
      }

      const data = await response.json();

      setResults(data);
    } catch (error) {
      console.error("Error fetching search results:", error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSearchResults();
  }, [searchDeparture, searchArrival]);

  const handleBookingComplete = () => {
    // Refetch search results when booking is completed
    fetchSearchResults();
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <Container className="mt-4 search-result-container">
      <h3>
        Search results for {searchDeparture} to {searchArrival}:
      </h3>
      {results.length === 0 ? (
        <p>No matching schedules found.</p>
      ) : (
        <>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Departure Place</th>
                <th>Arrival Place</th>
                <th>Departure Time</th>
                <th>Book</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result) => (
                <tr key={result.id}>
                  <td>{result.departure_place}</td>
                  <td>{result.arrival_place}</td>
                  <td>{new Date(result.departure_time).toLocaleString()}</td>
                  <td>
                    <Link
                      to={{
                        pathname: "/myBookings",
                        state: { resultData: result },
                      }}
                    >
                      <BookButton
                        scheduleId={result.id}
                        onBookingComplete={handleBookingComplete}
                      />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          <MyBookings />
        </>
      )}
    </Container>
  );
};

export default SearchResults;
