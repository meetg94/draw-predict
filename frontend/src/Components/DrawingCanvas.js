import { useEffect, useState, useRef } from 'react';

import axios from 'axios';

function DrawingCanvas() {

    const [drawing, setDrawing] = useState(false);
    const canvasRef = useRef(null);
    const contextRef = useRef(null);

    useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = window.innerWidth * 0.5;
    canvas.height = window.innerHeight * 0.5;
    canvas.style.width = `${window.innerWidth * 0.5}`;
    canvas.style.height = `${window.innerHeight * 0.5}`;

    const context = canvas.getContext('2d');
    context.lineCap = 'round';
    context.strokeStyle = 'black';
    context.lineWidth = 5;
    contextRef.current = context;
}, []);

  

    const startDrawing = ({ nativeEvent }) => {
        const { clientX, clientY, target } = nativeEvent;
        const { top, left } = target.getBoundingClientRect();
        const x = clientX - left;
        const y = clientY - top;
        contextRef.current.beginPath();
        contextRef.current.moveTo(x, y);
        setDrawing(true);
    };

    const finishDrawing = () => {
        contextRef.current.closePath();
        setDrawing(false);
    };

  const draw = ({ nativeEvent }) => {
    if (!drawing) {
        return;
    }
    const { clientX, clientY, target } = nativeEvent;
    const { top, left } = target.getBoundingClientRect();
    const x = clientX - left;
    const y = clientY - top;
    contextRef.current.lineTo(x, y);
    contextRef.current.stroke();
  };

  const predict = async () => {
    //Send the drawn image to the server for prediction
    const canvas = canvasRef.current;
    const dataUrl = canvas.toDataURL();

    try {
        const response = await axios.post('http://localhost:8000/predict/', {
            image: dataUrl
        });

        console.log(response.data);
    } catch (error) {
        console.error('Failed to predict image:', error.message);
    }
  };

  const clear = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
  };

  return (
    <div>
      <canvas 
        ref={canvasRef}
        onMouseDown={startDrawing}
        onMouseUp={finishDrawing}
        onMouseMove={draw}
      />
      <button onClick={predict}>Predict</button>
      <button onClick={clear}>Clear</button>
    </div>
  );
}

export default DrawingCanvas;
