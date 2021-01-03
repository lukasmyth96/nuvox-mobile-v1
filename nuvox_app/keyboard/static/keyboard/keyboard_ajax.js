// Ajax functions

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
            $('#game-over-modal').modal('show');
        }
    )
}