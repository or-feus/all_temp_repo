import * as React from 'react';
import type { NextPage } from 'next';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '../src/Link';
import ProTip from '../src/ProTip';
import Copyright from '../src/Copyright';
import Button_3x3 from "../components/Button_3x3";

const Home: NextPage = () => {
  return (
    <Container maxWidth="lg">
        <Button_3x3/>
    </Container>
  );
};

export default Home;
