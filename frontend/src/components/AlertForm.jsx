// Ferramentas React para gerenciamento de dados,
// ações automáticase comunicação com Backend
import { useState, useEffect } from "react";
import axios from "axios";

// 1. FORMULÁRIO: Armazenamento temporário antes do banco
export default function AlertForm({ currentLine }) {
  const [email, setEmail] = useState("");
  const [start, setStart] = useState("08:00");
  const [end, setEnd] = useState("10:00");
  const [lat, setLat] = useState(-22.90);
  const [lon, setLon] = useState(-43.20);
  const [message, setMessage] = useState("");
  const [alerts, setAlerts] = useState([]);

// 2. BUSCA DE DADOS (React): Função assíncrona entre Front com SQLite do Back
  const loadAlerts = async () => {
    const res = await axios.get("http://localhost:8000/alerts");
    setAlerts(res.data.alerts);
  };

// Garantia que a lista carregue apenas 1x ao abrir a página  
  useEffect(() => {
    loadAlerts();
  }, []);
// 3. CRIAÇÃO DE ALERTA (Post): Envia objeto JSON para /alert do FastAPI
  const createAlert = async () => {
    try {
      await axios.post("http://localhost:8000/alert", {
        email,
        line: currentLine,
        lat,
        lon,
        start_time: start,
        end_time: end,
      });

      setMessage("Alerta criado com sucesso!");
      loadAlerts();
    } catch (e) {
      setMessage("Erro ao criar alerta");
    }
  };

  const deleteAlert = async (id) => {
    await axios.delete(`http://localhost:8000/alert/${id}`);
    loadAlerts();
  };

// 4. INTERFACE VISUAL
  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Cadastrar Alerta</h3>

      <input
        placeholder="Seu email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <div>
        Horário início:
        <input type="time" value={start} onChange={(e) => setStart(e.target.value)} />
        Horário fim:
        <input type="time" value={end} onChange={(e) => setEnd(e.target.value)} />
      </div>

      <div>
        Latitude:
        <input value={lat} onChange={(e) => setLat(e.target.value)} />
        Longitude:
        <input value={lon} onChange={(e) => setLon(e.target.value)} />
      </div>

      <button onClick={createAlert}>Criar Alerta</button>

      <p>{message}</p>

      <h3>Alertas Ativos</h3>
      <ul>
        {alerts.map((a) => (
          <li key={a.id}>
            Linha {a.line} | {a.email} | {a.start_time}-{a.end_time}
            <button onClick={() => deleteAlert(a.id)}>Cancelar</button>
          </li>
        ))}
      </ul>
    </div>
  );
}