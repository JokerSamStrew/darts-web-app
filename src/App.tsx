import { useState, useRef } from "react";
import { Board } from "./Board.tsx"
import "./App.css";

function randomFromArray(arr) {
    if (!arr?.length) return undefined;
    return arr[Math.floor(Math.random() * arr.length)];
}

function App() {
    const board_ref = useRef(null);

    return (
        <>
            <div onClick={() => {
                if (board_ref.current) {
                    board_ref.current.toggleSpin();
                    const result_id = randomFromArray(board_ref.current.getIds());
                    console.log(result_id);
                    board_ref.current.setColor("#" + result_id, "orange");
                }
            }}>
                <Board ref={board_ref} />
            </div>
        </>
    );
}

export default App;
