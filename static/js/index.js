let currentSolution = null;


function setMode(newMode) {

    mca = document.querySelector(".main-content-area")

    subtitle = document.createElement('div')
    subtitle.setAttribute('class', 'subtitle')

    if (newMode === 'edit') {
        subtitle.innerHTML = 'Edit Mode'

        content = setEditMode()
    } else if (newMode === 'quiz') {
        subtitle.innerHTML = 'Quiz Mode'

        content = setQuizMode()
    }

    mca.replaceChildren(subtitle, content)
}

function setEditMode() {

    const content = document.createElement("div")
    content.setAttribute('class', 'content')

    const inputRow = document.createElement('div')
    inputRow.setAttribute('class', 'input-row')

    const input = document.createElement('input')
    input.setAttribute('class', 'input')
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.querySelector(".save-button").click();
        }
    });
    input.placeholder = 'Enter a Move Sequence'

    const colorSelector = document.createElement('select')
    colorSelector.setAttribute('class', 'selector')
    
    const optionWhite = document.createElement('option')
    optionWhite.setAttribute('value', 'White')
    optionWhite.innerHTML = 'White'
    
    const optionBlack = document.createElement('option')
    optionBlack.setAttribute('value', 'Black')
    optionBlack.innerHTML = 'Black'
    
    const button = document.createElement('button')
    button.setAttribute('class', 'save-button')
    button.addEventListener('click', saveLine)
    button.innerHTML = 'Save Line'
    
    colorSelector.replaceChildren(optionWhite, optionBlack)
    inputRow.replaceChildren(input, colorSelector, button)
    content.replaceChildren(inputRow)

    return content
}


function setQuizMode() {

    const content = document.createElement('div')
    content.setAttribute('class', 'content')

    const informationRow = document.createElement('div')
    informationRow.setAttribute('class', 'information-row')

    const infoText = document.createElement('div')
    infoText.setAttribute('class', 'info-text')
    infoText.innerHTML = 'Information: Color / Moves'

    const infoColor = document.createElement('div')
    infoColor.setAttribute('class', 'info-color')
    infoColor.innerHTML = ''
    
    const infoMoves = document.createElement('div')
    infoMoves.setAttribute('class', 'info-moves')
    infoMoves.innerHTML = ''

    const inputRow = document.createElement('div')
    inputRow.setAttribute('class', 'input-row')

    const input = document.createElement('input')
    input.setAttribute('class', 'input')
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.querySelector(".check-button").click();
        }
    });
    input.placeholder = 'Enter the next Move'

    const button = document.createElement('button')
    button.setAttribute('class', 'check-button')
    button.addEventListener('click', checkMove)
    button.innerHTML = 'Start Quiz'

    inputRow.replaceChildren(input, button)
    informationRow.replaceChildren(infoText, infoColor, infoMoves)
    content.replaceChildren(informationRow, inputRow)

    return content
}

async function getMoveSequence() {
    try {
        const response = await $.ajax({
            url: '/get_move_sequence',
            type: 'GET',
            contentType: 'application/json'
        });

        // Now we can actually return the data to the caller
        return response;
        
    } catch (error) {
        console.error("Error fetching sequence:", error);
        return null; // Return null so the caller can handle the error
    }
}


function saveLine() {
    
    // 1. Get the value
    const input = document.querySelector(".input");
    const inputVal = input.value;

    const color = document.querySelector('.selector').value

    const content = document.querySelector(".content");

    // 2. Clear any previous status messages so they don't stack up
    const existingStatus = document.querySelector(".status-message");
    if (existingStatus) {
        existingStatus.remove();
    }

    // 3. Prepare the new status element (we will fill text/color later)
    const statusDiv = document.createElement("div");
    statusDiv.setAttribute('class', 'status-message');

    $.ajax({
        url: '/save_line',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'line': inputVal, 'color': color }),

        success: function(response) {
            if (response.status === 200) {
                statusDiv.innerText = "Saved line: " + response.line;
                statusDiv.style.color = "#00FF00"; // Bright Green

                input.value = ''
            } else {
                statusDiv.innerText = "Error while saving the line";
                statusDiv.style.color = "#FF0000"; // Red
            }
            // Append result to the main area
            content.appendChild(statusDiv);
        },
        error: function() {
            // This catches network errors (404, 500, etc)
            statusDiv.innerText = "Error while saving the line";
            statusDiv.style.color = "#FF0000";
            content.appendChild(statusDiv);
        }
    });
}

async function checkMove() {
    
    // 1. Get the relevant values
    const button = document.querySelector('.check-button')
    const value = button.innerHTML

    const input = document.querySelector('.input')
    const inputVal = input.value

    const color = document.querySelector('.info-color')
    const moves = document.querySelector('.info-moves')

    // 2. Clear any previous status messages so they don't stack up
    const existingStatus = document.querySelector(".status-message");
    if (existingStatus) {
        existingStatus.remove();
    }

    // 3. Prepare the new status element (we will fill text/color later)
    const statusDiv = document.createElement("div");
    statusDiv.setAttribute('class', 'status-message');

    // 4. Execute logic
    if (value === 'Start Quiz') {
        const response = await getMoveSequence();

        // Safety check: Ensure response exists before reading properties
        if (response && response.status === 200) {
            
            button.innerHTML = 'Check Move';
            color.innerHTML = response.color;
                        
            let limitIndex = (response.breakpoint - 1) * 2; 
            if (response.color === 'black') {
                limitIndex += 1; // Show one extra move (White's move) if it's Black's turn
            }

            // 2. Store the target answer for later check
            currentSolution = response.move_sequence[limitIndex];

            // 3. Slice the array to get only the moves that happened BEFORE
            const movesToShow = response.move_sequence.slice(0, limitIndex);

            // 4. Format them nicely (e.g., "1. e4 e5 2. Nf3")
            let formattedString = "";
            movesToShow.forEach((move, index) => {
                // If index is even (0, 2, 4...), it's White's move -> Add the Number
                if (index % 2 === 0) {
                    const moveNum = (index / 2) + 1;
                    formattedString += moveNum + ". " + move + " ";
                } else {
                    // If index is odd, it's Black's move -> Just add the move
                    formattedString += move + " ";
                }
            });

            moves.innerHTML = formattedString.trim();

        } else {
            console.log("Failed to load sequence.");
        }
    } else if (value === 'Check Move') {

        // Compare user input with the stored global variable
        if (inputVal === currentSolution) {
            statusDiv.innerText = "Correct!"
            statusDiv.style.color = "#00FF00";
            
            // Optional: Reset UI for next round
            button.innerHTML = 'Start Quiz';
            input.value = '';
            checkMove()

        } else {
            statusDiv.innerText = "Wrong. Expected: " + currentSolution;
            statusDiv.style.color = "#FF0000"; // Red
        }
        
        content.appendChild(statusDiv);
    }
}