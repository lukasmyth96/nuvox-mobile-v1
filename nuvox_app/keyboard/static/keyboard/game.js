// JS functions related to the keyboard game.

function resetTimer() {
    let secondsRemaining = 10;
    const downloadTimer = setInterval(function(){
      if(secondsRemaining <= 0){
        clearInterval(downloadTimer);
        document.getElementById("countdown").innerHTML = "Finished";
      } else {
        document.getElementById("countdown").innerHTML = secondsRemaining.toString();
      }
      secondsRemaining -= 1;
    }, 1000);
}
