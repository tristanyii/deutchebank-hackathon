"use client";

import React, { useState, useRef, useEffect } from 'react';

// SVG Icon for the chat button
const ChatIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
  </svg>
);

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I'm an AI assistant. How can I help you find resources today?", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Automatically scroll to the bottom of the chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputValue.trim() === '' || isLoading) return;

    const userMessage = { text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // --- Backend API Call ---
    // The simulation is replaced with a real fetch call to your Python server.
    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputValue })
      });

      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      const botResponse = { text: data.reply, sender: 'bot' };
      setMessages(prev => [...prev, botResponse]);

    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      const errorResponse = { text: "Sorry, I'm having trouble connecting to the AI. Please try again later.", sender: 'bot' };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }

    /* // --- Old Backend API Call Simulation (now replaced) ---
    setTimeout(() => {
      const botResponse = { text: `Echo: "${userMessage.text}". (This is a simulated response. Connect me to your Python API!)`, sender: 'bot' };
      setMessages(prev => [...prev, botResponse]);
      setIsLoading(false);
    }, 1500);
    */
  };

  return (
    <div>
      {/* Chat Bubble Button */}
      <button
        onClick={toggleChat}
        className="fixed bottom-5 right-5 bg-indigo-600 text-white p-4 rounded-full shadow-lg hover:bg-indigo-700 transition-transform transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 z-50"
        aria-label="Open chat"
      >
        <ChatIcon />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-20 right-5 w-80 h-96 bg-white rounded-lg shadow-2xl flex flex-col z-50 transition-all duration-300">
          {/* Header */}
          <div className="bg-indigo-600 text-white p-3 rounded-t-lg flex justify-between items-center">
            <h3 className="font-semibold">AI Resource Assistant</h3>
            <button onClick={toggleChat} className="text-white hover:text-gray-200">&times;</button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto">
            {messages.map((msg, index) => (
              <div key={index} className={`mb-3 flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`rounded-lg px-3 py-2 max-w-xs ${msg.sender === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                  <div className="rounded-lg px-3 py-2 bg-gray-200 text-gray-500">
                      Typing...
                  </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={handleSendMessage} className="p-2 border-t border-gray-200">
            <div className="flex">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask about resources..."
                className="flex-1 p-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                className="bg-indigo-600 text-white px-4 rounded-r-md hover:bg-indigo-700 disabled:bg-indigo-300"
                disabled={isLoading}
              >
                Send
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
