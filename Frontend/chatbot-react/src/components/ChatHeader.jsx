import React from 'react';

export default function ChatHeader({ connected }) {
  return (
    <div className="chat-header">
      <div className={"connection-status " + (connected ? "connected" : "disconnected")}>
        {connected ? "CONECTADO" : "DESCONECTADO"}
      </div>
      <h1>🛒 Tienda Alemana</h1>
      <p>Chatbot de Atención al Cliente</p>
    </div>
  );
}
