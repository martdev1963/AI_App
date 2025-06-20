import "react"
import {useState, useEffect} from "react"
import {MCQChallenge} from "../challenge/MCQChallenge.jsx";

{/* ------------------------------------------------------------------------------------------------------
    VID_TIME: 1:02:21 / 2:31:54
    https://app.getrecall.ai/install-extension/
    Syntax below serves as if/else conditional logic...
    {history.length === 0 ? <p>The Mighty HAL says: No challenge history...</p> :
            <div className={"history-list"}></div>}
            to test:
            http://localhost:5173/history
            PARSER OUTPUT:
            4:12:26 PM [vite] (client) hmr update /src/history/HistoryPanel.jsx (x2)
    ------------------------------------------------------------------------------------------------------
*/}

export function HistoryPanel() {

    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect( () => {
        fetchHistory()
    }, [])

    const fetchHistory = async () => {
        setIsLoading(false);
    }

    if (isLoading) {
        return <div className="loading">The Mighty HAL says: Loading history...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchHistory}>Retry</button>
        </div>
    }

    return <div className="history-panel">
        <h2>History</h2>
        {history.length === 0 ? (
            <p>The Mighty HAL says: No challenge history...</p>
            ) : (
            <div className="history-list">
                {history.map((challenge) => (
                        <MCQChallenge
                             challenge={challenge}
                             key={challenge.id}
                             showExplanation
                        />
                ))}
            </div>
        )}
      </div>
  }