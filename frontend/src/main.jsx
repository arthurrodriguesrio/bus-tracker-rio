import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' // Variáveis de cor e design system
import App from './App.jsx' // Inicio da lógica do Bus-Tracker

/* React transforma código JavaScript em elemento visuais */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* Componente que orquestra o monitoramento de ônibus e alertas */}
    <App />
  </StrictMode>,
);
