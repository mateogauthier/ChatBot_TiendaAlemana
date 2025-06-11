import { useState, useEffect, useRef } from 'react';

const TiendaAlemanaChatbot = () => {
  const [messages, setMessages] = useState([
    { content: '¡Hola! Soy el asistente virtual de Tienda Alemana. ¿En qué puedo ayudarte hoy?', sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    checkConnection();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkConnection = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      setIsConnected(response.ok);
    } catch (error) {
      setIsConnected(false);
      console.error('Error conectando con el servidor:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendQuickQuestion = (question) => {
    setInputValue(question);
    setTimeout(() => sendMessage(question), 0);
  };

  const sendMessage = async (quickQuestion = null) => {
    const message = quickQuestion || inputValue.trim();
    
    if (!message || isTyping) return;

    // Agregar mensaje del usuario
    setMessages(prev => [...prev, { content: message, sender: 'user' }]);
    setInputValue('');
    setIsTyping(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Agregar respuesta del bot
      setMessages(prev => [...prev, { content: data.answer, sender: 'bot' }]);
      
    } catch (error) {
      setMessages(prev => [...prev, { 
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor verifica que el servidor esté funcionando.', 
        sender: 'bot' 
      }]);
      console.error('Error:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const TypingIndicator = () => (
    <div className="message bot">
      <div className="typing-indicator">
        <div className="typing-dots">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
      </div>
    </div>
  );

  const quickQuestions = [
    { text: 'Horarios', question: '¿Cuáles son los horarios de atención?' },
    { text: 'Ubicación', question: '¿Dónde están ubicados?' },
    { text: 'Productos', question: '¿Qué productos venden?' },
    { text: 'Delivery', question: '¿Hacen entregas a domicilio?' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center p-5">
      <style>{`
        .typing-indicator {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          background: #e5e7eb;
          border-radius: 18px;
          border-bottom-left-radius: 4px;
          max-width: 70px;
        }

        .typing-dots {
          display: flex;
          gap: 4px;
        }

        .typing-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #6b7280;
          animation: typing 1.4s infinite;
        }

        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }

        @keyframes typing {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-10px); }
        }

        .message.bot::before {
          content: "🤖";
          margin-right: 8px;
          font-size: 20px;
        }
      `}</style>
      
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-4xl h-96 md:h-[600px] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-red-600 to-red-700 text-white p-5 text-center relative">
          <div className={`absolute top-2 right-2 px-2 py-1 rounded-xl text-xs font-bold ${
            isConnected 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {isConnected ? 'CONECTADO' : 'DESCONECTADO'}
          </div>
          <h1 className="text-2xl font-bold mb-1">🛒 Tienda Alemana</h1>
          <p className="text-sm opacity-90">Chatbot de Atención al Cliente</p>
        </div>

        {/* Messages */}
        <div className="flex-1 p-5 overflow-y-auto bg-slate-50">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender} mb-4 flex ${
              message.sender === 'user' ? 'justify-end' : 'items-start'
            }`}>
              <div className={`max-w-[70%] p-3 rounded-2xl break-words ${
                message.sender === 'bot'
                  ? 'bg-gray-200 text-gray-800 rounded-bl-sm'
                  : 'bg-red-600 text-white rounded-br-sm'
              }`}>
                {message.content}
              </div>
            </div>
          ))}
          
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions */}
        <div className="px-5 pb-2 bg-white">
          <h3 className="text-xs text-gray-500 mb-2 uppercase tracking-wide font-medium">
            Preguntas frecuentes
          </h3>
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((item, index) => (
              <button
                key={index}
                onClick={() => sendQuickQuestion(item.question)}
                className="bg-red-50 text-red-600 border border-red-200 rounded-2xl px-3 py-1.5 text-xs hover:bg-red-600 hover:text-white transition-all duration-300"
              >
                {item.text}
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <div className="p-5 bg-white border-t border-gray-200">
          <div className="flex gap-3 items-center">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu mensaje aquí..."
              className="flex-1 p-3 border-2 border-gray-200 rounded-full text-sm outline-none focus:border-red-600 transition-colors duration-300"
            />
            <button
              onClick={() => sendMessage()}
              disabled={isTyping || !inputValue.trim()}
              className={`w-11 h-11 rounded-full flex items-center justify-center transition-colors duration-300 ${
                isTyping || !inputValue.trim()
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-red-600 hover:bg-red-700 cursor-pointer'
              } text-white`}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TiendaAlemanaChatbot;