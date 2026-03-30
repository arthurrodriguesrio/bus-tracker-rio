import React from "react";

// 1. EXIBIÇÃO TABULAR: Recebe os 'buses' em array filtrado e ordenado
// pelo backend, com visão comparativa entre os veículos
export default function BusTable({ buses }) {
  return (
    // 2. TABELA ACESSÍVEL: Criação de grade visual para
    // os dados de forma automática
    <table border="1" cellPadding="5">
        <thead>
            <tr>
                <th>Ônibus</th>
                <th>Velocidade (km/h)</th>
                <th>ETA (min)</th>
            </tr>
        </thead>
<tbody>
    {/* 3. Mapeia cada array de buses para linhas correspondentes 
     na tabela */}
    {buses.map((bus) => (
        <tr key={bus.order}>
         {/* Atualização de dados em tempo real com valores do back */}   
        <td>{bus.order}</td>
        <td>{bus.speed}</td>
        <td>{bus.eta_minutes}</td>
        </tr>
    ))}
</tbody>
    </table>
  );
}