import { useEffect, useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// 1.Exportação da função BusTracker com gerenciamento geal, desde lista de alertas
// até a linha escolhida para monitoramento
export default function BusTracker() {
  const [alerts, setAlerts] = useState([]);
  const [busData, setBusData] = useState([]);
  const [selectedLine, setSelectedLine] = useState("");
  
  // Formulário de novo alerta, integrado com coordenadas e horários
  const [formData, setFormData] = useState({
    email: "",
    line: "",
    start_time: "08:00",
    end_time: "09:00",
    address: "",
    lat: -22.9068, 
    lon: -43.1729
  });

  // 2. BUSCA EM TEMPO REAL (Pooling): Consome rota/status do Back, envia
  // localização do usuário p/ cálculo de ETA
  const fetchBusRealTime = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/status/${selectedLine}`, {
        params: { 
          lat: formData.lat, 
          lon: formData.lon 
        }
      });

      // Se res.data.success for true, pegamos a lista dentro de res.data.data
      if (res.data && res.data.success === true) {
        const listaOnibus = Array.isArray(res.data.data) ? res.data.data : [];
        setBusData(listaOnibus);
        console.log("Lista de ônibus recebida:", listaOnibus);
      } else {
        console.warn("API retornou sucesso falso ou sem dados");
        setBusData([]);
      }

    } catch (err) {
      console.error("Erro na conexão com o Backend:", err);
      setBusData([]); // Garante que continue sendo uma lista vazia para não quebrar o map
    }
  };

  // 3. SINCRONIZAÇÃO: Atualiza a lista de alertas ativos no banco
  const fetchAlerts = async () => {
    try {
      const res = await axios.get("http://localhost:8000/alerts");
      // Seu main retorna { "alerts": [...] }
      setAlerts(res.data.alerts || []);
    } catch (err) {
      console.error("Erro ao buscar alertas:", err);
    }
  };

  // 4. GEOCODIFICAÇÃO (Nominatim API): Converte endereço textual em 
  // coordenadas (lat/lon)
  const handleSearchAddress = async () => {
    if (!formData.address) return alert("Por favor, digite um endereço.");
    try {
      const res = await axios.get(`https://nominatim.openstreetmap.org/search`, {
        params: {
          q: formData.address + ", Rio de Janeiro",
          format: "json",
          limit: 1
        }
      });

      if (res.data.length > 0) {
        const { lat, lon, display_name } = res.data[0];
        setFormData({ 
          ...formData, 
          lat: parseFloat(lat), 
          lon: parseFloat(lon) 
        });
        alert(`Localizado: ${display_name}`);
      } else {
        alert("Endereço não encontrado no RJ.");
      }
    } catch (err) {
      alert("Erro ao buscar endereço.");
    }
  };

  // 5. GERENCIAMENTO DE CICLO DE VIDA (useEffect): Define intervalo 
  // de 30 segundos para atualização automatica (Real-Time), evitando
  // vazamento de memória na troca de linha (clearInterval)
  const handleCreateAlert = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/alert", formData);
      alert("Alerta criado!");
      fetchAlerts();
    } catch (err) {
      alert("Erro ao criar: " + err.response?.data?.detail || "Erro desconhecido");
    }
  };

  // 6. Cancela um alerta
  const cancelAlert = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/alert/${id}`);
      fetchAlerts();
    } catch (err) {
      console.error("Erro ao cancelar:", err);
    }
  };

  // Efeito para atualizar ônibus a cada 30s e alertas ao carregar
  useEffect(() => {
    if (selectedLine && selectedLine.trim() !== "") {
        fetchBusRealTime();
        fetchAlerts();
        const interval = setInterval(fetchBusRealTime, 30000);
        return () => clearInterval(interval);
    } else {
        fetchAlerts();
    } 
  }, [selectedLine]);

  return (
    <div style={{ padding: "20px", backgroundColor: "#121212", minHeight: "100vh", color: "#fff", fontFamily: 'Arial' }}>
      
      <h1 style={{ textAlign: "center", marginBottom: "30px" }}> BUS-TRACKER</h1>

      {/* FORMULÁRIO DE CRIAÇÃO */}
      <div style={{ backgroundColor: "#1e1e1e", padding: "20px", borderRadius: "10px", marginBottom: "30px", border: "1px solid #333" }}>
        <h3 style={{ textAlign: "center", marginTop: 0 }}>Criar Novo Alerta</h3>
        <form onSubmit={handleCreateAlert} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
          <input style={inputStyle} type="email" placeholder="Email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} required />
          <input style={inputStyle} type="text" placeholder="Linha (ex: 383)" value={formData.line} onChange={e => setFormData({...formData, line: e.target.value})} required />
          <input style={inputStyle} type="time" value={formData.start_time} onChange={e => setFormData({...formData, start_time: e.target.value})} required />
          <input style={inputStyle} type="time" value={formData.end_time} onChange={e => setFormData({...formData, end_time: e.target.value})} required />
          
          {/* CAMPO DE ENDEREÇO E BOTÃO DE BUSCA */}
          <input 
            style={{ ...inputStyle, gridColumn: "span 2" }} 
            type="text" 
            placeholder="Endereço (Ex: Rua Uruguai, 300, Tijuca)" 
            value={formData.address} 
            onChange={e => setFormData({...formData, address: e.target.value})} 
          />
          <button 
            type="button" 
            onClick={handleSearchAddress} 
            style={{ ...btnSubmitStyle, backgroundColor: "#007bff", gridColumn: "span 2", marginBottom: "5px" }}
          >
            LOCALIZAR NO MAPA
          </button>

          {/* EXIBIÇÃO APENAS PARA CONFERÊNCIA */}
          <div style={{ gridColumn: "span 2", textAlign: "center", fontSize: "12px", color: "#888" }}>
            Coordenadas: {formData.lat.toFixed(4)}, {formData.lon.toFixed(4)}
          </div>

          <button type="submit" style={btnSubmitStyle}>CADASTRAR ALERTA</button>
        </form>
      </div>

      {/* MAPA E TABELA LADO A LADO */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "30px", height: "450px" }}>
        
        {/* MAPA */}
        <div style={{ flex: 1, border: "1px solid #444", borderRadius: "10px", overflow: "hidden" }}>
          <MapContainer center={[-22.9068, -43.1729]} zoom={12} style={{ height: "100%", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {busData.map((bus) => (
              <CircleMarker 
                key={bus.bus_id} 
                center={[bus.lat, bus.lon]} 
                radius={8} 
                pathOptions={{ color: 'red', fillColor: 'red', fillOpacity: 0.8 }}
              >
                <Popup>
                  <strong>Ônibus: {bus.bus_id}</strong><br/>
                  Linha: {selectedLine}<br/>
                  Chegada: {bus.eta_min} min
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>

        {/* TABELA */}
        <div style={{ flex: 1, border: "1px solid #444", borderRadius: "10px", backgroundColor: "#1e1e1e", overflowY: "auto" }}>
          <div style={{ padding: "10px", borderBottom: "1px solid #333", display: "flex", justifyContent: "space-between" }}>
            <span>Monitorando: <strong>{selectedLine}</strong></span>
            <input 
              style={{ width: "60px", background: "#333", color: "#fff", border: "1px solid #555" }} 
              placeholder="Linha" 
              onBlur={(e) => setSelectedLine(e.target.value)} 
            />
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead style={{ backgroundColor: "#252525" }}>
              <tr>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Velocidade</th>
                <th style={thStyle}>Distância</th>
                <th style={thStyle}>ETA</th>
              </tr>
            </thead>
            <tbody>
              {busData.length > 0 ? busData.map((bus) => (
                <tr key={bus.bus_id} style={{ borderBottom: "1px solid #333" }}>
                  <td style={tdStyle}>{bus.bus_id}</td>
                  <td style={tdStyle}>{bus.speed} km/h</td>
                  <td style={tdStyle}>{bus.distance_km} km</td>
                  <td style={tdStyle}>{bus.eta_min} min</td>
                </tr>
              )) : (
                <tr><td colSpan="4" style={{ textAlign: "center", padding: "20px", color: "#666" }}>Buscando ônibus...</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* ALERTAS ATIVOS */}
      <div>
        <h3 style={{ textAlign: "center", borderBottom: "1px solid #333", paddingBottom: "10px" }}>Alertas Ativos</h3>
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {alerts.map((alert) => (
            <div key={alert.id} style={alertCardStyle}>
              <span>🔔 <strong>Linha {alert.line}</strong> - {alert.email} ({alert.start_time} às {alert.end_time})</span>
              <button onClick={() => cancelAlert(alert.id)} style={btnCancelStyle}>CANCELAR</button>
            </div>
          ))}
        </div>
      </div>

    </div> 
  ); 
} 

// Estilos
const inputStyle = { padding: "10px", backgroundColor: "#333", color: "#fff", border: "1px solid #444", borderRadius: "5px" };
const btnSubmitStyle = { gridColumn: "span 2", padding: "12px", backgroundColor: "#28a745", color: "#fff", fontWeight: "bold", border: "none", borderRadius: "5px", cursor: "pointer" };
const thStyle = { padding: "12px", textAlign: "left", fontSize: "14px", color: "#aaa" };
const tdStyle = { padding: "12px", fontSize: "14px" };
const alertCardStyle = { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "15px", backgroundColor: "#1e1e1e", border: "1px solid #333", borderRadius: "8px" };
const btnCancelStyle = { backgroundColor: "#dc3545", color: "#fff", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer", fontSize: "12px" };