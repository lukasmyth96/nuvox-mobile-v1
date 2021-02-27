/*
    The functions in this file are responsible for handling the swipes:
    - fetching predictions
    - displaying suggestions
    - handling clicks on suggestions etc...
 */

function handleSwipe(trace){
    const textBox = document.getElementById('text-box');
    const prompt = textBox.value;
    if (trace.length > 0) {
        getPrediction(prompt, trace);
    } else {
        console.log("Skipping prediction request as trace is empty...")
    }
}


//  ------------------------------------------- AJAX REQUESTS ----------------------------------------------------------


function getPrediction(prompt, trace) {

    $.ajax({
            url: '/api/predict/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "prompt": prompt,
                "trace": trace
            }),
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            },
            dataType: 'json',
        }
    ).done(function (data) {
        // Update text box.
        const textBox = document.getElementById('text-box');
        const topPredictedWord = data.predicted_words[0];
        if (topPredictedWord !== undefined) {
            textBox.value += topPredictedWord;
        }

        // Update suggestions.
        for (let idx = 1; idx < 4; idx++) {
            let suggestion = data.predicted_words;
            let suggestionButton = document.getElementById(`suggestion=${idx}`);
            suggestionButton.value = "";
            if (suggestion !== undefined) {
                suggestionButton.value = suggestion;
            }
        }

    }).fail(function (jqXHR, exception) {
            alert('Oops something went wrong :(');
        }
    )
}
