import React, { useState, useEffect } from 'react';
import ChatHeader from './components/ChatHeader';
import ChatMessages from './components/ChatMessages';
import ChatInput from './components/ChatInput';
import QuickQuestions from './components/QuickQuestions';
import env from './env';

const API_BASE_URL = env.API_SERVER_URL;

export default function App() {
  const [messages, setMessages] = useState([
    { content: '¡Hola! Soy el asistente virtual de Tienda Alemana. ¿En qué puedo ayudarte hoy?', sender: 'bot' }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then(res => setConnected(res.ok))
      .catch(() => setConnected(false));
  }, []);

  const sendMessage = async (question) => {
    if (!question) return;
    const userMessage = { content: question, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });

      const data = await res.json();
      setMessages(prev => [...prev, { content: data.answer, sender: 'bot' }]);
    } catch {
      setMessages(prev => [...prev, {
        content: 'Lo siento, hubo un error al procesar tu mensaje.',
        sender: 'bot'
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="chat-container">
      <ChatHeader connected={connected} />
      <ChatMessages messages={messages} isTyping={isTyping} />
      <QuickQuestions onSelect={sendMessage} />
      <ChatInput onSend={sendMessage} disabled={isTyping} />
    </div>
  );
}
