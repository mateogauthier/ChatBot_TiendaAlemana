import React from 'react';

export default function ChatMessages({ messages, isTyping }) {
  return (
    <div className="chat-messages">
      {messages.map((msg, i) => (
        <div key={i} className={"message " + msg.sender}>
          <div className="message-content">{msg.content}</div>
        </div>
      ))}
      {isTyping && (
        <div className="message bot" id="typingIndicator">
          <div className="typing-indicator">
            <div className="typing-dots">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
