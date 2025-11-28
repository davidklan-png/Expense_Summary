import React from 'react';
import ReactDOM from 'react-dom/client';
import { TestDemo } from '../TestDemo';
import './styles.css';
import '../animations.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <TestDemo />
  </React.StrictMode>
);
