import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Send, X, User, Bot } from 'lucide-react';
import { chatWithMentor } from '../services/api';

interface ChatProps {
  context?: any;
}

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
}

export const Chat: React.FC<ChatProps> = ({ context }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: "Hi! I'm your AI Career Mentor. Ask me anything about your resume or career path.", sender: 'bot' }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const toggleChat = () => setIsOpen(!isOpen);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      // Pass a simplified string context of the resume analysis
      const contextStr = context ? JSON.stringify(context.skill_gap) : "";
      const response = await chatWithMentor(userMsg.text, contextStr);
      
      const botMsg: Message = { id: Date.now() + 1, text: response.reply, sender: 'bot' };
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      const errorMsg: Message = { id: Date.now() + 1, text: "Sorry, I'm having trouble connecting right now.", sender: 'bot' };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <motion.button
        className="fixed bottom-6 right-6 p-4 bg-primary text-white rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={toggleChat}
      >
        {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
      </motion.button>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            className="fixed bottom-24 right-6 w-96 h-[500px] bg-white rounded-2xl shadow-2xl border border-slate-200 flex flex-col z-40 overflow-hidden"
          >
            {/* Header */}
            <div className="bg-secondary p-4 text-white flex items-center gap-3">
              <div className="p-2 bg-slate-700 rounded-full">
                <Bot size={20} />
              </div>
              <div>
                <h3 className="font-semibold">Career Mentor</h3>
                <p className="text-xs text-slate-300">Online • AI Powered</p>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
              {messages.map((msg) => (
                <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`
                    max-w-[80%] p-3 rounded-2xl text-sm
                    ${msg.sender === 'user' 
                      ? 'bg-primary text-white rounded-tr-none' 
                      : 'bg-white text-slate-800 border border-slate-200 rounded-tl-none shadow-sm'}
                  `}>
                    {msg.text}
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-white p-3 rounded-2xl rounded-tl-none border border-slate-200 shadow-sm">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 bg-white border-t border-slate-100">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  placeholder="Ask a question..."
                  className="flex-1 p-2 border border-slate-300 rounded-lg focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                />
                <button 
                  onClick={handleSend}
                  disabled={!input.trim() || isTyping}
                  className="p-2 bg-primary text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
