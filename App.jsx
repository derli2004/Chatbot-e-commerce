import React from 'react';
import Chatbot from './components/Chatbot';  // Assuming chatbot.jsx is in the same folder
import 'bootstrap/dist/css/bootstrap.min.css';  // For Bootstrap styles


const App = () => {
    return (
        <div className="App" style={{ display: 'flex', justifyContent: 'center', padding: '20px', minHeight: '100vh', backgroundColor: '#6f42c1' }}>
            <div style={{ width: '100%', maxWidth: '600px', border: '1px solid #ddd', borderRadius: '8px', padding: '20px', backgroundColor: '#000000' }}>
                <h1 className="text-center mb-4" style={{ color: '#6f42c1' }}>Chatbot</h1>
                <Chatbot />
            </div>
        </div>
    );
};

export default App;
