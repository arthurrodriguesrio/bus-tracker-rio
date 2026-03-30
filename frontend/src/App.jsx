// 1. IMPORTAÇÃO DE COMPONENTES: Traz o componente principal do
// monitoramento, com toda a lógica de mapas, tabelas e
// integração om o FastAPI
import BusTest from "./components/BusTest";

// 2. COMPONENTE RAIZ: Primeiro componente a carregar pelo React,
// exibindo o 'BusTracker'
function App() {
  return <BusTest />;
}

// 3. Exportação para acesso pelo index/main
export default App;