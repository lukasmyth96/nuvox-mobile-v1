// JS functions related to the keyboard game.

function resetTimer() {
    let secondsRemaining = 10;
    setCountdown(secondsRemaining);
    const downloadTimer = setInterval(function(){
      if(secondsRemaining <= 0){
        clearInterval(downloadTimer);
        onGameOver();
      }
      setCountdown(secondsRemaining);
      secondsRemaining -= 1;
    }, 1000);
}

function setCountdown(secondsRemaining) {
    document.getElementById("countdown").innerHTML = secondsRemaining.toString();
}

function onGameOver() {
    gameInProgress = false;
    gameId = undefined;
    alert('Game Over!');
}
