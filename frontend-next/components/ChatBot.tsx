'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, Send, Sparkles, X, Minimize2 } from 'lucide-react';
import { sendChatMessage } from '@/lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const EXAMPLE_QUESTIONS = [
  'Why is this region high risk?',
  'What are the weather conditions?',
  'Any port disruptions today?',
  'What is the main risk factor?',
];

export function ChatBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text?: string) => {
    const message = text || input.trim();
    if (!message || isLoading) return;

    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: message }]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage(message);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.response },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Chat toggle button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, type: 'spring' }}
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full flex items-center justify-center shadow-2xl ${
          isOpen ? 'hidden' : ''
        }`}
        style={{
          background: 'linear-gradient(135deg, var(--risk-color), color-mix(in srgb, var(--risk-color) 60%, #000))',
          boxShadow: '0 0 30px color-mix(in srgb, var(--risk-color) 40%, transparent)',
        }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        <MessageCircle className="w-6 h-6 text-white" />
        <motion.div
          className="absolute inset-0 rounded-full border-2"
          style={{ borderColor: 'var(--risk-color)' }}
          animate={{ scale: [1, 1.3, 1], opacity: [0.5, 0, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </motion.button>

      {/* Chat panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed bottom-6 right-6 z-50 w-[400px] max-w-[calc(100vw-3rem)] glass-card rounded-2xl overflow-hidden"
            style={{
              boxShadow: '0 0 60px rgba(0, 0, 0, 0.5), 0 0 40px color-mix(in srgb, var(--risk-color) 15%, transparent)',
            }}
          >
            {/* Header */}
            <div
              className="px-5 py-4 flex items-center justify-between"
              style={{
                background: 'linear-gradient(135deg, var(--risk-color)20, transparent)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
              }}
            >
              <div className="flex items-center gap-3">
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center"
                  style={{ background: 'var(--risk-color)30' }}
                >
                  <Sparkles className="w-4 h-4" style={{ color: 'var(--risk-color)' }} />
                </div>
                <div>
                  <h3 className="font-display text-sm font-bold tracking-wide text-white">
                    AI ANALYST
                  </h3>
                  <p className="text-xs text-slate-400">Ask about risk assessment</p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="p-2 rounded-lg hover:bg-white/5 transition-colors"
              >
                <X className="w-4 h-4 text-slate-400" />
              </button>
            </div>

            {/* Messages */}
            <div className="h-[300px] overflow-y-auto p-4 chat-container">
              {messages.length === 0 ? (
                <div className="text-center py-8">
                  <Sparkles className="w-8 h-8 text-slate-600 mx-auto mb-3" />
                  <p className="text-sm text-slate-500 mb-4">
                    Ask me anything about the current risk assessment
                  </p>
                  <div className="space-y-2">
                    {EXAMPLE_QUESTIONS.map((q, i) => (
                      <button
                        key={i}
                        onClick={() => handleSend(q)}
                        className="block w-full text-left px-3 py-2 text-sm text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  {messages.map((msg, i) => (
                    <div
                      key={i}
                      className={`chat-bubble ${
                        msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'
                      }`}
                    >
                      {msg.content}
                    </div>
                  ))}
                  {isLoading && (
                    <div className="chat-bubble chat-bubble-assistant">
                      <div className="typing-dots">
                        <span />
                        <span />
                        <span />
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-white/5">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSend();
                }}
                className="flex gap-2"
              >
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask a question..."
                  className="input-cyber flex-1"
                  disabled={isLoading}
                />
                <motion.button
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="px-4 rounded-lg flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                  style={{
                    background: 'linear-gradient(135deg, var(--risk-color), color-mix(in srgb, var(--risk-color) 60%, #000))',
                  }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Send className="w-4 h-4 text-white" />
                </motion.button>
              </form>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
