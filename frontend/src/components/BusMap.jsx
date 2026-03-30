// 1. CONFIG DO MAPA INTERATIVO: Componentes para quadro, margens
// indicadores de loc, "balões" para clicar; CSS para zoom e camadas
// além de correções no React/Vite/Webpack
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

//2. CORREÇÃO DE ÍCONES DO LEAFFLET: Garantia dos 
// marcadores na tela
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

export default function BusMap({ buses }) {
  return (
    // 3. CONTAINER DO MAPA: Definições de ponto inicial
    // e ferramenta para zoom, além de design do mapa,
    // exibição de tempo estimado com servço Geofencing
    <MapContainer
      center={[-22.90, -43.20]}
      zoom={13}
      style={{ height: "100%", marginTop: "100%" }}
    >
    <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {buses.map((bus) => (
        <Marker key={bus.order} position={[bus.lat, bus.lng]}>
          <Popup>
            <b>Ônibus {bus.order}</b><br />
            ETA: {bus.eta_minutes} min
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}