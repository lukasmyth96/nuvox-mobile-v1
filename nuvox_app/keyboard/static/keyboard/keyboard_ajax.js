function getRandomWord() {
    $.ajax({
            url: '/random-word/',
            dataType: 'json',
            success: function (data) {
                alert(`Following word fetched from server: ${data.word}`);
            }
        }
    );
}
