import { useState, useRef } from "react";
import { Board } from "./Board.tsx"
import "./App.css";

function randomFromArray(arr) {
    if (!arr?.length) return undefined;
    return arr[Math.floor(Math.random() * arr.length)];
}

let tId;

function debounce(fn, ms) {
    return (...args) => {
        clearTimeout(tId);
        tId = setTimeout(() => fn(...args), ms);
    };
}

function App() {
    const board_ref = useRef(null);

    const debounceColorRandomSector = debounce(() => {
        const result_id = randomFromArray(board_ref.current.getIds());
        board_ref.current.setColor("#" + result_id, "orange");
        board_ref.current.toggleSpin();
    }, 5000);

    return (
        <>
            <div onClick={() => {
                if (board_ref.current) {
                    // const result_id = randomFromArray(board_ref.current.getIds());
                    // board_ref.current.setColor("#" + result_id, "orange");
                    board_ref.current.toggleSpin();
                    board_ref.current.dropColors();
                    debounceColorRandomSector();
                }
            }}>
                <Board ref={board_ref} />
            </div>
        </>
    );
}

export default App;
