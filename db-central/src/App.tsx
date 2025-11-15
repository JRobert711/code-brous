// src/App.tsx
import './styles/App.css';

function App() {
  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>✅ La aplicación está funcionando</h1>
      <p>Si ves este mensaje, React está renderizando correctamente.</p>
      <div style={{ marginTop: '20px', padding: '20px', background: '#f0f0f0', borderRadius: '10px' }}>
        <h3>Prueba los componentes:</h3>
        <button onClick={() => alert('Funciona!')} style={{ padding: '10px 20px', margin: '5px' }}>
          Botón de prueba
        </button>
      </div>
    </div>
  );
}

export default App;