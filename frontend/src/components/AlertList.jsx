import { useEffect, useState } from "react";
import axios from "axios";

// 1. DADOS (List State): 'alerts' armazena o array de objetos do back
export default function AlertList() {
  const [alerts, setAlerts] = useState([]);
  // 2. SINCRONIZAÇÃO (Fetching): Consome GET do FastAPI, usando
  // 'try/catch para quebra do Front caso o servidor esteja offline
  const fetchAlerts = async () => {
    try {
      const res = await axios.get("http://localhost:8000/alerts");
      // Se res.data.alerts for nulo, fica definido como lista vazia
      setAlerts(res.data.alerts || []);
    } catch (err) {
      console.error("Erro ao buscar alertas:", err);
    }
  };

  
  useEffect(() => {
    fetchAlerts();
  }, []);

// 3. RETORNO DE INTERFACE (UI), com atualização de lista através
// do array 'alers', com 'key' de referência. Além de feedbak
// para lista vazia
  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Alertas Ativos</h3>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id}>
            Linha: {alert.line} | Email: {alert.email}
          </li>
        ))}
      </ul>
    </div>
  );
}