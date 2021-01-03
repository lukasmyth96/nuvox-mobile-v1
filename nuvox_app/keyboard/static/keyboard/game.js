// JS functions related to the keyboard game.

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