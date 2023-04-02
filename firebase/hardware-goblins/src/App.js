import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import { app } from './firestore';
import { connectFunctionsEmulator, getFunctions, httpsCallable } from "firebase/functions";
const functions = getFunctions(app, 'us-west2');
// connectFunctionsEmulator(functions, "localhost", 5001)
const sendMqtt = httpsCallable(functions, 'sendMqtt');

function App() {
  const [n, setN] = useState(1);
  const [echo, setEcho] = useState(false);
  const [play, setPlay] = useState(false);
  const [realtime, setRealtime] = useState(true);

  const zeroOne = (bool) => bool ? 1 : 0;
  const boolString = (bool) => bool ? 'true' : 'false';

  let messageString = "[" + n + "," + zeroOne(echo) + "," + zeroOne(play) + "," + zeroOne(realtime) + "]";

  useEffect(() => {
    sendMqtt({message: messageString});
    console.log(messageString);
  }, [n, echo, play, realtime])

  return (
    <div className="App">
      <header className="App-header">
        <img src={'https://oldschool.runescape.wiki/images/Goblin_%28green%29_%28historical_v1%29.png?f9c52?download'} className="App-logo" alt="logo" />
        <p>
          HARDWARE GOBLINS
        </p>
        <div style={{display: 'flex', flexDirection: 'column', gap: 24}}>
          <div>
            <button onClick={() => setN(15)}>Squirrel mode</button>
            <button onClick={() => setN(10)}>Minion</button>
            <button onClick={() => setN(-7)}>Deep voice</button>
            <button onClick={() => setEcho(true)}>Robot</button>
          </div>
          <div>
            Pitch shift: {n}
            <input className='slider' style={{marginLeft: 10}} type={'range'} min={-20} max={20} onChange={(e) => setN(e.target.value)} value={n}></input>
          </div>
          <div>
            <button style={{backgroundColor: (echo ? 'green' : 'red'), color: 'white'}} onClick={() => setEcho(!echo)}>Echo: {boolString(echo)}</button>
            <button style={{backgroundColor: (play ? 'green' : 'red'), color: 'white'}} onClick={() => setPlay(!play)}>Play: {boolString(play)}</button>
            <button style={{backgroundColor: (realtime ? 'green' : 'red'), color: 'white'}} onClick={() => setRealtime(!realtime)}>Realtime: {boolString(realtime)}</button>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
