function setNewTargetWord() {
    $.ajax({
            url: '/random-word/',
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
    $.ajax({
            url: '/data-collection-swipes/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
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
