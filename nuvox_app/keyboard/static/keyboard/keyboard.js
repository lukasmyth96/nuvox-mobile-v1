/*
    The functions in this file are responsible for handling the swipes:
    - fetching predictions
    - displaying suggestions
    - handling clicks on suggestions etc...
 */

function handleSwipe(trace){
    getPrediction(trace);
}


//  ------------------------------------------- AJAX REQUESTS ----------------------------------------------------------


function getPrediction(trace) {

    $.ajax({
            url: '/api/predict/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "trace": trace
            }),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            dataType: 'json',
        }
    ).done(function (data) {
        console.log(data.predicted_words);
    }).fail(function (jqXHR, exception) {
            alert('Oops something went wrong :(');
        }
    )
}
