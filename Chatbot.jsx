import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import 'bootstrap/dist/css/bootstrap.min.css';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [options, setOptions] = useState([]);
    const [isButtonHovered, setIsButtonHovered] = useState(false);
    const [isOptionHovered, setIsOptionHovered] = useState([]);
    const [cart, setCart] = useState([]);
    const [showCart, setShowCart] = useState(false);
    const [isCartHovered, setIsCartHovered] = useState(false);
    const messagesEndRef = useRef(null);

    const sendMessage = async (message) => {
        if (message.trim() === '') return;
        const userMessage = { sender: 'user', text: message };
        setMessages(prev => [...prev, userMessage]);
        setOptions([]);
        setInput('');

        const res = await axios.post('http://127.0.0.1:5000/chat', { message: message });
        const fullBotMessage = res.data.message;
        const botImageUrl = res.data.image_url;

        const newBotMessage = {
            sender: 'bot',
            text: '',
            image_url: botImageUrl
        };
        setMessages(prev => [...prev, newBotMessage]);

        let index = 0;
        const typingInterval = setInterval(() => {
            if (index < fullBotMessage.length) {
                newBotMessage.text += fullBotMessage[index];
                setMessages(prev => {
                    const updatedMessages = [...prev];
                    updatedMessages[updatedMessages.length - 1] = { ...newBotMessage };
                    return updatedMessages;
                });
                index++;
            } else {
                clearInterval(typingInterval);
                if (res.data.options) {
                    setOptions(res.data.options);
                    setIsOptionHovered(Array(res.data.options.length).fill(false));
                }
            }
        }, 30);
    };

    useEffect(() => {
        const fetchInitialMessage = async () => {
            const res = await axios.post('http://127.0.0.1:5000/chat', { message: 'start' });
            const botMessage = { sender: 'bot', text: '' };
            setMessages([botMessage]);
            let index = 0;
            const typingInterval = setInterval(() => {
                if (index < res.data.message.length) {
                    botMessage.text += res.data.message[index];
                    setMessages(prev => [...prev.slice(0, -1), { ...botMessage }]);
                    index++;
                } else {
                    clearInterval(typingInterval);
                    if (res.data.options) {
                        setOptions(res.data.options);
                        setIsOptionHovered(Array(res.data.options.length).fill(false));
                    }
                }
            }, 30);
        };
        fetchInitialMessage();
    }, []);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage(input);
        }
    };

    const handleOptionClick = (option) => {
        sendMessage(option);
    };

    const handleOptionHover = (index, isHovered) => {
        setIsOptionHovered(prev => {
            const updated = [...prev];
            updated[index] = isHovered;
            return updated;
        });
    };

    const addToCart = (product) => {
        setCart(prev => [...prev, product]);
    };

    const removeFromCart = (index) => {
        setCart(prev => prev.filter((_, i) => i !== index));
    };

    const fakeCheckout = () => {
        setCart([]);
        setShowCart(false);
        alert('Order placed. Thank you!✨');
    };

    return (
        <div className="chatbot-container" style={{ maxWidth: '100%', margin: 'auto' }}>
            <div className="messages-container" style={{ padding: '20px', background: '#e7e4f1', borderRadius: '8px', minHeight: '300px', overflowY: 'scroll', maxHeight: '400px' }}>
                {messages.map((msg, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, transform: 'translateY(10px)' }}
                        animate={{ opacity: 1, transform: 'translateY(0)' }}
                        transition={{ duration: 0.5 }}
                        style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}
                    >
                        <p style={{
                            fontWeight: 'bold',
                            color: msg.sender === 'user' ? '#ffffff' : '#6f42c1',
                            backgroundColor: msg.sender === 'user' ? '#6f42c1' : '#e6f0ff',
                            padding: '8px',
                            borderRadius: '10px',
                            display: 'inline-block'
                        }}>
                            {msg.sender === 'user' ? 'You' : 'Bot'} :
                            {msg.image_url ? (
                                <>
                                    {msg.text.split('\n').map((line, idx) => (
                                        <React.Fragment key={idx}>{line}<br /></React.Fragment>
                                    ))}
                                    <div style={{ marginTop: '10px' }}>
                                        <img src={msg.image_url} alt="product" style={{ width: '200px', borderRadius: '10px' }} />
                                    </div>
                                    <div>
                                        <button onClick={() => addToCart({ name: msg.text, image: msg.image_url })} className="btn btn-sm mt-2" style={{ backgroundColor: '#6f42c1', color: '#fff' }}>Add to Cart</button>
                                    </div>
                                </>
                            ) : msg.text}
                        </p>
                    </motion.div>
                ))}
            </div>

            <div className="input-container" style={{ display: 'flex', alignItems: 'center', marginTop: '10px' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                    className="form-control"
                    style={{ flex: 1, borderRadius: '25px', padding: '10px', marginRight: '10px', border: '1px solid #6f42c1' }}
                />
                <button
                    onClick={() => sendMessage(input)}
                    className="btn"
                    style={{ backgroundColor: isButtonHovered ? '#ffffff' : '#6f42c1', color: isButtonHovered ? '#000000' : '#ffffff', borderRadius: '8px', padding: '10px 16px', transition: 'all 0.3s ease', border: '1px solid #6f42c1' }}
                    onMouseEnter={() => setIsButtonHovered(true)}
                    onMouseLeave={() => setIsButtonHovered(false)}
                >
                    Send
                </button>
                            <button
            onClick={() => setShowCart(true)}
            className="btn position-relative ms-2"
            onMouseEnter={() => setIsCartHovered(true)}
            onMouseLeave={() => setIsCartHovered(false)}
            style={{
                backgroundColor: isCartHovered ? '#ffffff' : '#6f42c1',
                color: isCartHovered ? '#000000' : '#ffffff',
                padding: '10px 16px',
                borderRadius: '8px',
                border: '1px solid #6f42c1',
                transition: 'all 0.3s ease',
            }}
            >
            View Cart
            {cart.length > 0 && (
                <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {cart.length}
                </span>
            )}
            </button>
                
            </div>

            {options.length > 0 && (
                <div className="options-container" style={{ marginTop: '20px', display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                    {options.map((option, index) => (
                        <motion.button
                            key={index}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3 }}
                            onClick={() => handleOptionClick(option)}
                            className="btn btn-block mb-2"
                            style={{
                                backgroundColor: isOptionHovered[index] ? '#ffffff' : '#6f42c1',
                                color: isOptionHovered[index] ? '#000000' : '#ffffff',
                                borderRadius: '20px',
                                padding: '10px 20px',
                                transition: 'all 0.2s ease',
                                border: '1px solid #6f42c1',
                                flex: '1 1 auto',
                                minWidth: '150px',
                                textAlign: 'center'
                            }}
                            onMouseEnter={() => handleOptionHover(index, true)}
                            onMouseLeave={() => handleOptionHover(index, false)}
                        >
                            {option}
                        </motion.button>
                    ))}
                </div>
            )}

            {showCart && (
                <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Your Cart</h5>
                                <button type="button" className="btn-close" onClick={() => setShowCart(false)}></button>
                            </div>
                            <div className="modal-body">
                                {cart.length === 0 ? (
                                    <p>Your cart is empty.</p>
                                ) : (
                                    cart.map((item, index) => (
                                        <div key={index} className="d-flex justify-content-between align-items-center mb-2">
                                            <img src={item.image} alt="" style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '5px' }} />
                                            <span className="ms-2 flex-grow-1">{item.name}</span>
                                            <button className="btn btn-sm btn-danger" onClick={() => removeFromCart(index)}>x</button>
                                        </div>
                                    ))
                                )}
                            </div>
                            <div className="modal-footer">
                                {cart.length > 0 && (
                                    <button className="btn btn-success" onClick={fakeCheckout}>Checkout</button>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <div ref={messagesEndRef} />
        </div>
    );
};

export default Chatbot;
