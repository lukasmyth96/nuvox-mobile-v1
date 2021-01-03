// Variables for referencing the canvas and 2d canvas context
let canvas, ctx;

let targetText;

let gameInProgress = false;
let gameId;
let gameTimer;

// Record swipe trace, a sequence of objects containing the x and y coordinates at each time-step.
// Note - coordinates are relative to the canvas.
let trace = [];
let traceStartTime;

// Variables to keep track of the mouse position and left-button status
let mouseX, mouseY, mouseDown = 0;

// Variables to keep track of the touch position
let touchX, touchY;

// Keep track of the old/last position when drawing a line
// We set it to -1 at the start to indicate that we don't have a good value for it yet
let lastX, lastY = -1;

// Draws a line between the specified position on the supplied canvas name
// Parameters are: A canvas context, the x position, the y position, the size of the dot
function drawLine(ctx, x, y, size) {

    // If lastX is not set, set lastX and lastY to the current position
    if (lastX === -1) {
        lastX = x;
        lastY = y;
    }

    // Let's use black by setting RGB values to 0, and 255 alpha (completely opaque)
    const r = 0;
    const g = 0;
    const b = 0;
    const a = 255;

    // Select a fill style
    ctx.strokeStyle = "rgba(" + r + "," + g + "," + b + "," + (a / 255) + ")";

    // Set the line "cap" style to round, so lines at different angles can join into each other
    ctx.lineCap = "round";
    //ctx.lineJoin = "round";

    // Draw a filled line
    ctx.beginPath();

    // First, move to the old (previous) position
    ctx.moveTo(lastX, lastY);

    // Now draw a line to the current touch/pointer position
    ctx.lineTo(x, y);

    // Set the line thickness and draw the line
    ctx.lineWidth = size;
    ctx.stroke();

    ctx.closePath();

    // Update the last position to reference the current position
    lastX = x;
    lastY = y;
}

// Clear the canvas context using the canvas width and height
function clearCanvas(canvas, ctx) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function clearTrace() {
    trace = [];
}

// Update trace with latest mouse position relative to canvas.
function updateMouseTrace() {
    const x = mouseX / canvas.width;
    const y = mouseY / canvas.height;
    const t = getSecondsSinceTraceStart();
    if (isTracePointValid(x, y)) {
         trace.push({x, y, t});
    }
}

// Update trace with latest touch position relative to canvas.
function updateTouchTrace() {
    const x = touchX / canvas.width;
    const y = touchY / canvas.height;
    const t = getSecondsSinceTraceStart();
    if (isTracePointValid(x, y)) {
         trace.push({x, y, t});
    }
}

function isTracePointValid(x, y) {
    return ((0.0 <= x) && (x <= 1.0) && (0.0 <= y) && (y <= 1.0));
}

function getSecondsSinceTraceStart() {
    const currentTime = new Date().getTime();
    return (currentTime - traceStartTime) / 1000;
}

function resetTraceStartTime() {
    traceStartTime = new Date().getTime();
}

// Keep track of the mouse button being pressed and draw a dot at current location
function onMouseDown() {
    mouseDown = 1;
    resetTraceStartTime();
    drawLine(ctx, mouseX, mouseY, 8);
}

// Keep track of the mouse position and draw a dot if mouse button is currently pressed
function onMouseMove(e) {

    // Update the mouse co-ordinates when moved
    getMousePos(e);

    if (mouseDown === 1) {
        updateMouseTrace();

        drawLine(ctx, mouseX, mouseY, 8);
    }
}

// Keep track of the mouse button being released
function onMouseUp() {

    if (gameInProgress) {
        submitSwipe();
        setNewTargetWord();
    }

    mouseDown = 0;
    clearCanvas(canvas, ctx);
    clearTrace();
    // Reset lastX and lastY to -1 to indicate that they are now invalid, since we have lifted the "pen"
    lastX = -1;
    lastY = -1;
}

// Get the current mouse position relative to the top-left of the canvas
function getMousePos(e) {

    if (e.offsetX) {
        mouseX = e.offsetX;
        mouseY = e.offsetY;
    } else if (e.layerX) {
        mouseX = e.layerX;
        mouseY = e.layerY;
    }
}

// Draw something when a touch start is detected
function onTouchStart() {
    resetTraceStartTime();

    // Update the touch co-ordinates
    getTouchPos();

    drawLine(ctx, touchX, touchY, 8);

    // Prevents an additional mousedown event being triggered
    e.preventDefault();
}

function onTouchEnd() {

    if (gameInProgress) {
        submitSwipe();
        setNewTargetWord();
    }

    clearCanvas(canvas, ctx);
    clearTrace();
    // Reset lastX and lastY to -1 to indicate that they are now invalid, since we have lifted the "pen"
    lastX = -1;
    lastY = -1;

}

// Draw something and prevent the default scrolling when touch movement is detected
function onTouchMove(e) {
    // Update the touch co-ordinates
    getTouchPos(e);

    // Add latest position to trace
    updateTouchTrace();

    // During a touchmove event, unlike a mousemove event, we don't need to check if the touch is engaged, since there will always be contact with the screen by definition.
    drawLine(ctx, touchX, touchY, 8);

    // Prevent a scrolling action as a result of this touchmove triggering.
    e.preventDefault();
}

// Get the touch position relative to the top-left of the canvas.
// When we get the raw values of pageX and pageY below, they take into account the scrolling on the page.
// but not the position relative to our target div. We'll adjust them using "target.offsetLeft" and.
// "target.offsetTop" to get the correct values in relation to the top left of the canvas.
function getTouchPos(e) {

    if (e.touches) {
        if (e.touches.length === 1) { // Only deal with one finger
            const touch = e.touches[0]; // Get the information for finger #1
            touchX = touch.pageX - touch.target.offsetLeft;
            touchY = touch.pageY - touch.target.offsetTop;
        }
    }
}

function sketchpad_resize() {
    // isMobile is defined in keyboard.html from Django context.
    if (isMobile) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight * 0.8;
    } else {
        canvas.width = window.innerWidth * 0.4;
        canvas.height = window.innerHeight * 0.8;
    }
}


// Set-up the canvas and add our event handlers after the page has loaded
// Note onBodyLoad is called via the 'onload' attribute of <body> in base.html.
function onBodyLoad() {

    // Get the specific canvas element from the HTML document
    canvas = document.getElementById('sketchpad');

    // If the browser supports the canvas tag, get the 2d drawing context for this canvas
    if (canvas.getContext)
        ctx = canvas.getContext('2d');

    // Check that we have a valid context to draw on/with before adding event handlers
    if (ctx) {

        // First, adjust the canvas size to fit the current screen dimensions
        sketchpad_resize();

        // React to window being resized
        window.addEventListener('resize', sketchpad_resize, false);

        // React to mouse events on the canvas, and mouseup on the entire document
        canvas.addEventListener('mousedown', onMouseDown, false);
        canvas.addEventListener('mousemove', onMouseMove, false);
        window.addEventListener('mouseup', onMouseUp, false);

        // React to touch events on the canvas
        canvas.addEventListener('touchstart', onTouchStart, false);
        canvas.addEventListener('touchend', onTouchEnd, false);
        canvas.addEventListener('touchmove', onTouchMove, false);
    }
}
