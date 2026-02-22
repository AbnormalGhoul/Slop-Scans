import { useState, useEffect } from 'react'
import './App.css'
import { CircularProgressBar } from './CircularProgressBar'
import { detectPage } from './apiCall'
import logo from './assets/react.svg'

function App() {
  const [progress, setProgress] = useState(-1)
  const [color, setColor] = useState('#10b981')
  const [text, setText] = useState("Human")
  const [loading, setLoading] = useState(false)
  const [ai_phrases, setAiPhrases] = useState("")

  const getActiveTabUrl = async (): Promise<string> => {
    return new Promise((resolve, reject) => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message))
          return
        }

        const url = tabs[0]?.url
        if (!url) {
          reject(new Error('No active tab URL found'))
          return
        }

        resolve(url)
      })
    })
  }

  const handleColorChange = (value: number) => {
    if (value == -1) {
      setColor('#e5e7eb') // gray for 0%
    } else if (value >= 0 && value <= 30) {
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


  const handleTextChange = (value: number) => {
    if (value == -1) {
      setText("")
    } else if (value >= 0 && value <= 30) {
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

  // Listen for page changes and call the detection API
  useEffect(() => {
    const callDetectionAPI = async () => {
      try {
        setLoading(true)
        const pageUrl = await getActiveTabUrl()
        const response = await detectPage(pageUrl)
        console.log('Detection API response:', response)
        const score = response.percentage
        const ai_phrases = response.ai_phrases

        setAiPhrases(ai_phrases)
        
        // Convert score to 0-100 range if needed
        let progressValue = score
        if (score <= 1) {
          progressValue = (1-score) * 100  // Convert 0-1 to 0-100
        }
        
        // Clamp value between 0-100
        progressValue = Math.min(100, Math.max(0, progressValue))
        
        setProgress(Math.round(progressValue))
      } catch (error) {
        console.error('Failed to call detection API:', error)
      } finally {
        setLoading(false)
      }
    }

    // Call API when component mounts
    callDetectionAPI()

    // Listen for tab updates (page reload, navigation)
    const handleTabUpdated = (_tabId: number, changeInfo: any) => {
      if (changeInfo.status === 'complete') {
        callDetectionAPI()
      }
    }

    // Listen for active tab changes
    const handleTabActivated = () => {
      callDetectionAPI()
    }

    chrome.tabs.onUpdated.addListener(handleTabUpdated)
    chrome.tabs.onActivated.addListener(handleTabActivated)

    // Cleanup listeners
    return () => {
      chrome.tabs.onUpdated.removeListener(handleTabUpdated)
      chrome.tabs.onActivated.removeListener(handleTabActivated)
    }
  }, [])

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>Slop Scan</h1>
      
      {loading && <p style={{ color: '#3b82f6', fontWeight: 'bold' }}>Analyzing page...</p>}
      
      <div style={{ marginBottom: '40px' }}>
        <CircularProgressBar 
          progress={progress}
          size={200}
          color={color}
          text={`${text} (${Math.round(progress)}%)`}
          imageUrl={logo}
        />

        <p style={{ marginTop: '20px', fontSize: '18px', color: '#374151' }}>
          {ai_phrases}
        </p>
      </div>
    </div>
  )
}

export default App
