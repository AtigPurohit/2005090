import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const AllTrains = () => {
  const [trainSchedules, setTrainSchedules] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/trains/schedule')
      .then(response => {
        setTrainSchedules(response.data);
      })
      .catch(error => {
        console.error('Error fetching train schedules:', error);
      });
  }, []);

  return (
    <div>
      <Typography variant="h4" component="h1" gutterBottom>
        All Trains
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Train Name</TableCell>
              <TableCell>Train Number</TableCell>
              <TableCell>Departure Time</TableCell>
              <TableCell>Seats Available (Sleeper)</TableCell>
              <TableCell>Seats Available (AC)</TableCell>
              <TableCell>Price (Sleeper)</TableCell>
              <TableCell>Price (AC)</TableCell>
              <TableCell>Delayed By (minutes)</TableCell>
              <TableCell>Action</TableCell> {/* Add this column for the link */}
            </TableRow>
          </TableHead>
          <TableBody>
            {trainSchedules.map(train => (
              <TableRow key={train.train_id}>
                <TableCell>{train.train_name}</TableCell>
                <TableCell>{train.train_id}</TableCell>
                <TableCell>{train.departure_time}</TableCell>
                <TableCell>{train.seats_available_sleeper}</TableCell>
                <TableCell>{train.seats_available_ac}</TableCell>
                <TableCell>{train.price_sleeper}</TableCell>
                <TableCell>{train.price_ac}</TableCell>
                <TableCell>{train.delayed_by}</TableCell>
                <TableCell>
                  <Link to={`/trains/${train.train_id}`}>View Details</Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default AllTrains;
