function setNewTargetWord() {
    $.ajax({
            url: '/random-word/',
            dataType: 'json',
            success: function (data) {
                $('#target-word').text(`Please swype the word: ${data.word}`);
            }
        }
    );
}
