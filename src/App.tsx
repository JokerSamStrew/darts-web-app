import { useState, useRef } from "react";
import { Board } from "./Board.tsx"
import "./App.css";



function App() {
    const board_ref = useRef(null);

    return (
        <>
            <div >
                <Board ref={board_ref} />
            </div>
        </>
    );
}

export default App;
