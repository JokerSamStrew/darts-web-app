import { Board } from "./Board.tsx"
import "./App.css";
import { useRef } from "react";

type BoardRef = {
    current: Board;
    getIds: () => number[];
    setColor: (color: string, colorClass: string) => void;
    toggleSpin: () => void;
    dropColors: () => void;
};

type Board = {
    getIds: () => number[];
    setColor: (color: string, colorClass: string) => void;
    toggleSpin: () => void;
    dropColors: () => void;
};

function randomFromArray<T>(arr: T[]): T | undefined {
    if (!arr?.length) return undefined;
    return arr[Math.floor(Math.random() * arr.length)];
}

let timeoutId: any;

function debounce<T>(fn: (...args: any[]) => T, ms: number): (...args: any[]) => T {
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn(...args), ms);
        return timeoutId;
    };
}

function App() {
    const boardRef = useRef<BoardRef>(null);

    const debounceColorRandomSector = debounce<void>(() => {
        const result_id = randomFromArray(boardRef.current!.getIds());
        boardRef.current!.setColor("#" + result_id, "orange");
        boardRef.current!.toggleSpin();
    }, 5000);

    return (
        <>
            <div onClick={() => {
                if (boardRef.current) {
                    // const result_id = randomFromArray(board_ref.current.getIds());
                    // board_ref.current.setColor("#" + result_id, "orange");
                    boardRef.current!.toggleSpin();
                    boardRef.current!.dropColors();
                    debounceColorRandomSector();
                }
            }}>
                <Board ref={boardRef} />
            </div>
        </>
    );
}

export default App;
