/*
    The functions in this file are all related to the data collection game.
 */

//  ------------------------------------------- GAME VARS ------------------------------------------------------------
let targetText;
let gameInProgress = false;
let gameId;
let gameTimer;

//  ------------------------------------------- SWIPE HANDLER ----------------------------------------------------------

function handleSwipe(trace) {
    if (gameInProgress && trace.length > 0) {
        submitSwipe();
        setNewTargetWord();
    }
}

//  ------------------------------------------- GAME FUNCS ------------------------------------------------------------

function resetTimer() {
    let secondsRemaining = 60;
    setCountdown(secondsRemaining);
    gameTimer = setInterval(function(){
      if(secondsRemaining <= 0){
        endGame();
      }
      setCountdown(secondsRemaining);
      secondsRemaining -= 1;
    }, 1000);
}

function setCountdown(secondsRemaining) {
    document.getElementById("countdown").innerHTML = secondsRemaining.toString();
}

function endGame() {
    clearInterval(gameTimer);
    setCountdown(0);
    gameInProgress = false;
    gameId = undefined;
    $('#start-game-button').show();
    $('#end-game-button').hide();
    showEndGameModal();
}

//  ------------------------------------------- LEADERBOARD FUNCS ------------------------------------------------------

function showEndGameModal(leaderboardData) {
    setTimeout(function () {
        // 10ms delay to allow browser to repaint first.
        showLeaderboard();
    }, 10)
}

// Builds the HTML Table out of myList.
function buildHtmlTable(selector, tableData) {
    let columns = addAllColumnHeaders(selector, tableData);

    for (let i = 0; i < tableData.length; i++) {
        let row$ = $('<tr/>');
        for (let colIndex = 0; colIndex < columns.length; colIndex++) {
            let cellValue = tableData[i][columns[colIndex]];
            if (cellValue == null) cellValue = "";
            row$.append($('<td/>').html(cellValue));
        }
        $(selector).append(row$);
    }
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records.
function addAllColumnHeaders(selector, tableData) {
    let columnSet = [];
    let headerTr$ = $('<tr/>');

    for (let i = 0; i < tableData.length; i++) {
        let rowHash = tableData[i];
        for (let key in rowHash) {
            if ($.inArray(key, columnSet) === -1) {
                columnSet.push(key);
                headerTr$.append($('<th/>').html(key));
            }
        }
    }
    $(selector).append(headerTr$);

    return columnSet;
}

//  ------------------------------------------- AJAX REQUESTS ----------------------------------------------------------
function startNewGame() {
    $.ajax({
            url: '/api/games/',
            type: 'POST',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            dataType: 'json',
        }
    ).done(function (data) {
        gameInProgress = true;
        gameId = data.id;

        // Reset timer
        resetTimer();

        // Set the initial target word.
        setNewTargetWord();

        $('#start-game-button').hide();
        $('#end-game-button').show();

        // show the target word element.
        $('#target-word').show();
    })
}


function setNewTargetWord() {
    $.ajax({
            url: '/api/random-word/',
            dataType: 'json'
        }
    ).done(
        function (data) {
            targetText = data.word;
            $('#target-word').text(data.word);
        }
    );
}

function submitSwipe() {
    if (typeof gameId === 'undefined') {
        alert('You must start a game first!');
        return;
    }

    $.ajax({
            url: '/api/data-collection-swipes/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "game": gameId,
                "target_text": targetText,
                "trace": trace,
            }),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            dataType: 'json',
        }
    ).done(function (data) {
        if (data.trace_matches_text === false) {
            alert('Trace was not accurate :(')
        }
    }).fail(function (jqXHR, exception) {
            alert('Oops something went wrong :(');
        }
    )
}

function showLeaderboard() {
    $.ajax({
            url: '/api/leaderboard',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            dataType: 'json',
        }
    ).done(function (data) {
            buildHtmlTable('#leaderboard-table', data)
            $('#game-over-modal').modal('show');
        }
    )
}