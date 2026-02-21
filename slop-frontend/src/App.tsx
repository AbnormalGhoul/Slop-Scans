import { useState, useEffect } from 'react'
import './App.css'
import { CircularProgressBar } from './CircularProgressBar'

function App() {
  const [progress, setProgress] = useState(65)
  const [color, setColor] = useState('#10b981')
  const [text, setText] = useState("Human")

  const handleColorChange = (value: number) => {
    if (value >= 1 && value <= 30) {
      setColor('#ef4444') // red
    } else if (value >= 31 && value <= 69) {
      setColor('#eab308') // yellow
    } else if (value >= 70 && value <= 100) {
      setColor('#10b981') // green
    }
  }

  useEffect(() => {
    handleColorChange(progress)
  }, [progress])

  const handleProgressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newProgress = Number(e.target.value)
    setProgress(newProgress)
  }

  const handleTextChange = (value: number) => {
    if (value >= 1 && value <= 30) {
      setText("AI")
    } else if (value >= 31 && value <= 69) {
      setText("Mixed")
    } else if (value >= 70 && value <= 100) {
      setText("Human")
    }
  }

  useEffect(() => {
    handleTextChange(progress)
  }, [progress])

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Slop Scan</h1>
      
      <div style={{ marginBottom: '40px' }}>
        <CircularProgressBar 
          progress={progress}
          size={200}
          color={color}
          text={`${text} (${Math.round(progress)}%)`}
        />
        <div style={{ marginTop: '20px' }}>
          <input 
            type="range" 
            min="0" 
            max="100" 
            value={progress}
            onChange={handleProgressChange}
            style={{ width: '200px' }}
          />
        </div>
      </div>
    </div>
  )
}

export default App
