const SIZE = 128;
const CELL = 4;
const WHITE = "#ffffff";
const COLORS = ["#111111", "#ff5f57", "#f5a623", "#ffd60a", "#4cc764", "#5aa2ff", "#9b6dff", "#8b5a2b"];

const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");

let grid = [];
let tool = "pen";
let color = COLORS[0];
let undoStack = [];
let redoStack = [];
let drawing = false;
let last = null;

function setText(id, text) {
	const el = document.getElementById(id);
	if (el) el.textContent = text;
}

function blankGrid() {
	const g = [];
	for (let r = 0; r < SIZE; r++) g.push(new Array(SIZE).fill(WHITE));
	return g;
}

function copyGrid(g) {
	return g.map(row => [...row]);
}

function paint(r, c, col) {
	grid[r][c] = col;
	ctx.fillStyle = col;
	ctx.fillRect(c * CELL, r * CELL, CELL, CELL);
}

function drawAll() {
	for (let r = 0; r < SIZE; r++)
		for (let c = 0; c < SIZE; c++)
			paint(r, c, grid[r][c]);
}

function dot(r, c) {
	const size = tool === "eraser" ? 2 : 2;
	const col = tool === "eraser" ? WHITE : color;
	for (let i = 0; i < size; i++)
		for (let j = 0; j < size; j++) {
			const rr = r + i, cc = c + j;
			if (rr < SIZE && cc < SIZE) paint(rr, cc, col);
		}
}

function lineTo(r, c) {
	const steps = Math.max(Math.abs(r - last.r), Math.abs(c - last.c), 1);
	for (let i = 1; i <= steps; i++) {
		const rr = Math.round(last.r + (r - last.r) * i / steps);
		const cc = Math.round(last.c + (c - last.c) * i / steps);
		dot(rr, cc);
	}
	last = { r, c };
}

function fill(startR, startC) {
	const target = grid[startR][startC];
	if (target === color) return null;

	const stack = [[startR, startC]];
	let count = 0;
	let maxStack = 1;
	paint(startR, startC, color);

	while (stack.length > 0) {
		const [r, c] = stack.pop();
		count++;
		const neighbours = [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]];
		for (const [nr, nc] of neighbours) {
			if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && grid[nr][nc] === target) {
				paint(nr, nc, color);
				stack.push([nr, nc]);
			}
		}
		maxStack = Math.max(maxStack, stack.length);
	}
	return { count, maxStack };
}

function save() {
	undoStack.push(copyGrid(grid));
	redoStack = [];
	update();
}

function undo() {
	if (undoStack.length === 0) return;
	redoStack.push(copyGrid(grid));
	grid = undoStack.pop();
	drawAll();
	log("Undo", "blue");
	update();
}

function redo() {
	if (redoStack.length === 0) return;
	undoStack.push(copyGrid(grid));
	grid = redoStack.pop();
	drawAll();
	log("Redo", "blue");
	update();
}

function cellAt(e) {
	const rect = canvas.getBoundingClientRect();
	const c = Math.floor((e.clientX - rect.left) / rect.width * SIZE);
	const r = Math.floor((e.clientY - rect.top) / rect.height * SIZE);
	return { r: Math.max(0, Math.min(SIZE - 1, r)), c: Math.max(0, Math.min(SIZE - 1, c)) };
}

function clearCanvas() {
	if (grid.every(row => row.every(cell => cell === WHITE))) return;
	save();
	drawing = false;
	grid = blankGrid();
	ctx.fillStyle = WHITE;
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	log("Cleared", "red");
}

canvas.addEventListener("pointerdown", e => {
	const { r, c } = cellAt(e);
	if (tool === "fill") {
		const before = copyGrid(grid);
		const result = fill(r, c);
		if (!result) return;
		undoStack.push(before);
		redoStack = [];
		setText("fill-n", result.count + " cells");
		setText("stack-n", result.maxStack);
		log("Fill: " + result.count + " cells, max stack " + result.maxStack, "green");
		update();
		return;
	}
	save();
	drawing = true;
	last = { r, c };
	canvas.setPointerCapture(e.pointerId);
	dot(r, c);
});

canvas.addEventListener("pointermove", e => {
	if (!drawing) return;
	const { r, c } = cellAt(e);
	lineTo(r, c);
});

canvas.addEventListener("pointerup", () => {
	if (drawing) log(tool === "pen" ? "Pen stroke" : "Erased", tool === "pen" ? "" : "red");
	drawing = false;
});

function log(text, cls) {
	const list = document.getElementById("log");
	if (!list) return;
	const li = document.createElement("li");
	li.textContent = text;
	if (cls) li.className = cls;
	list.prepend(li);
	if (list.children.length > 6) list.lastChild.remove();
}

function update() {
	setText("undo-n", undoStack.length);
	setText("redo-n", redoStack.length);
	setText("undo-bar", "█".repeat(Math.min(undoStack.length, 20)));
	setText("redo-bar", "█".repeat(Math.min(redoStack.length, 20)));
	document.getElementById("undo").disabled = undoStack.length === 0;
	document.getElementById("redo").disabled = redoStack.length === 0;
}

function selectTool(name) {
	tool = name;
	document.querySelectorAll(".tool").forEach(b => b.classList.toggle("on", b.dataset.tool === name));
}

function selectColor(col) {
	color = col;
	document.querySelectorAll(".swatch").forEach(s => s.classList.toggle("on", s.dataset.color === col));
	if (tool === "eraser") selectTool("pen");
}

function box(r1, c1, r2, c2) {
	for (let c = c1; c <= c2; c++) { paint(r1, c, "#111111"); paint(r2, c, "#111111"); }
	for (let r = r1; r <= r2; r++) { paint(r, c1, "#111111"); paint(r, c2, "#111111"); }
}

document.querySelectorAll(".tool").forEach(b => b.addEventListener("click", () => selectTool(b.dataset.tool)));
document.getElementById("undo").addEventListener("click", undo);
document.getElementById("redo").addEventListener("click", redo);
document.getElementById("clear").addEventListener("click", clearCanvas);

COLORS.forEach(col => {
	const b = document.createElement("button");
	b.className = "swatch" + (col === color ? " on" : "");
	b.dataset.color = col;
	b.style.background = col;
	b.setAttribute("aria-label", "Colour " + col);
	b.addEventListener("click", () => selectColor(col));
	document.getElementById("swatches").appendChild(b);
});

document.addEventListener("keydown", e => {
	if (e.ctrlKey && e.key === "z") { e.preventDefault(); undo(); }
	if (e.ctrlKey && e.key === "y") { e.preventDefault(); redo(); }
});

grid = blankGrid();
drawAll();
box(34, 74, 104, 112);
box(84, 22, 112, 54);
update();
log("Canvas ready: " + SIZE + " x " + SIZE + " grid");
