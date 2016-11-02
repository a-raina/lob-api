var limitWord = 10;
$("#text-input").keyup(function () {
    $this = $(this);
    var regex = /\s+/gi;
    var wordcount = jQuery.trim($this.val()).replace(regex, ' ').split(' ').length;
    if (wordcount <= limitWord) {
        chars = $this.val().length;
    } else {
        var text = $(this).val();
        var new_text = text.substr(0, chars);
        $(this).val(new_text);
        wordcount --;
    }
    $("#count-label").html(wordcount);
});