import React from 'react';

const questions = [
  '¿Cuáles son los horarios de atención?',
  '¿Dónde están ubicados?',
  '¿Qué productos venden?',
  '¿Hacen entregas a domicilio?'
];

export default function QuickQuestions({ onSelect }) {
  return (
    <div className="quick-questions">
      <h3>Preguntas frecuentes</h3>
      <div className="quick-question-buttons">
        {questions.map((q, i) => (
          <button key={i} className="quick-question-btn" onClick={() => onSelect(q)}>
            {q.split('?')[0]}
          </button>
        ))}
      </div>
    </div>
  );
}
