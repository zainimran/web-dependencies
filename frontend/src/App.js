import React from 'react'
import './App.css';
import Graph from "./components/Graph";
import { GeistProvider, CssBaseline } from '@geist-ui/react'


function App() {
  return (
    <GeistProvider>
      <CssBaseline /> 
      <Graph/>
    </GeistProvider>
  );
}

export default App;