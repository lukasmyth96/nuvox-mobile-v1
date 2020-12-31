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
        gameId = data.id;

        // Set the initial target word.
        setNewTargetWord();

        // hide the start game button.
        $('#start-game-button').hide();

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
            $('#target-word').text(`Please swype the word: ${data.word}`);
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
        if (data.trace_matches_text === true) {
            alert('Thanks :)')
        } else {
            alert('Trace was not accurate :(')
        }
    })
        .fail(function (jqXHR, exception) {
                alert('Oops something went wrong :(');
            }
        )
}
