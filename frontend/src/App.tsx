import { useState } from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { ThemeProvider } from './theme';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function AppContent() {
  const [count, setCount] = useState(0);

  return (
    <Container maxWidth="md" sx={{ textAlign: 'center', py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 4 }}>
        <a href='https://vite.dev' target='_blank'>
          <img src={viteLogo} className='logo' alt='Vite logo' />
        </a>
        <a href='https://react.dev' target='_blank'>
          <img src={reactLogo} className='logo react' alt='React logo' />
        </a>
      </Box>
      
      <Typography variant="h3" component="h1" gutterBottom>
        Vite + React + MUI
      </Typography>
      
      <Box sx={{ my: 4 }}>
        <Button 
          variant="contained" 
          size="large" 
          onClick={() => setCount(count => count + 1)}
          sx={{ mb: 2 }}
        >
          count is {count}
        </Button>
        
        <Typography variant="body1" sx={{ mb: 2 }}>
          Edit <code>src/App.tsx</code> and save to test HMR
        </Typography>
      </Box>
      
      <Typography variant="body2" color="text.secondary">
        Click on the Vite and React logos to learn more
      </Typography>
    </Container>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
