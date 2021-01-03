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
    setTimeout(function () {
        // 10ms delay to allow browser to repaint first.
        $('#game-over-modal').modal('show');
    }, 10)
}
