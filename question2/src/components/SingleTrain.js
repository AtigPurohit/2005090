import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Typography } from '@mui/material';

const SingleTrain = () => {
  const { trainId } = useParams();
  const [train, setTrain] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:5000/trains/schedule/${trainId}`)
      .then(response => {
        setTrain(response.data);
      })
      .catch(error => {
        console.error('Error fetching single train:', error);
      });
  }, [trainId]);

  if (!train) {
    return <Typography variant="h4" component="h1">Loading train details...</Typography>;
  }

  return (
    <div>
      <Typography variant="h4" component="h1" gutterBottom>
        {train.train_name} (Train Number: {train.train_id})
      </Typography>
      <Typography variant="body1" gutterBottom>
        Departure Time: {train.departure_time}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Seats Available (Sleeper): {train.seats_available_sleeper}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Seats Available (AC): {train.seats_available_ac}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Price (Sleeper): {train.price_sleeper}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Price (AC): {train.price_ac}
      </Typography>
      <Typography variant="body1" gutterBottom>
        Delayed By (minutes): {train.delayed_by}
      </Typography>
    </div>
  );
};

export default SingleTrain;
