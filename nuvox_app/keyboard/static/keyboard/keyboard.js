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
        console.log(data.predicted_words);
        const textBox = document.getElementById('text-box');
        textBox.value += ` ${data.predicted_words[0]} `;  // pre and post spaces are important!

    }).fail(function (jqXHR, exception) {
            alert('Oops something went wrong :(');
        }
    )
}
