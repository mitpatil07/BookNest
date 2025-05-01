$(document).ready(function () {
    var searchQuery = $("#searchQuery");
    var suggestionsPopup = $("#suggestionsPopup");
    var suggestionsList = $("#suggestionsList");
    var searchUrl = $('#searchUrl').data('url');
    var bookDetailsSection = $("#bookDetails");

    // Triggering the search after clicking the search button
    $("#searchBtn").on("click", function () {
        var query = searchQuery.val();

        if (query.length > 2) {
            $.ajax({
                url: searchUrl,
                data: { 'query': query },
                dataType: 'json',
                success: function (data) {
                    suggestionsList.empty();  // Clear previous suggestions

                    if (data.suggestions.length > 0) {
                        suggestionsPopup.show();  // Show the suggestions popup
                        data.suggestions.forEach(function (suggestion) {
                            suggestionsList.append("<li class='list-group-item list-group-item-action d-flex align-items-center justify-content-between p-3 mb-2 shadow-sm rounded' data-book-id='" + suggestion.id + "' data-book-type='" + suggestion.type + "'>" + suggestion.name + "</li>");
                        });
                    } else {
                        suggestionsPopup.hide();  // Hide the popup if no suggestions
                    }
                },
                error: function (xhr, status, error) {
                    console.log("AJAX error:", status, error);
                }
            });
        } else {
            suggestionsPopup.hide();  // Hide the popup if query is too short or empty
        }
    });

    // Clicking on a suggestion triggers an AJAX request to get detailed book data
    suggestionsList.on('click', 'li', function () {
        var bookId = $(this).data('book-id');  // Get the ID of the clicked suggestion
        var bookType = $(this).data('book-type');  // Get the type of the book (books_data, story_book, or History_book)

        // Make an AJAX request to get more details about the book
        $.ajax({
            url: "{% url 'get_book_details' %}",  // Use the correct URL for fetching book details
            data: { 'book_id': bookId, 'book_type': bookType },
            dataType: 'json',
            success: function (data) {
                // Redirect to the book detail page
                if (data && data.detail_url) {
                    window.location.href = data.detail_url;  // Redirect to the book detail page
                }
            },
            error: function (xhr, status, error) {
                console.log("Error fetching book details:", error);
            }
        });
    });

    // Close the popup when clicking outside
    $(document).on('click', function (e) {
        if (!$(e.target).closest('#searchForm').length) {
            suggestionsPopup.hide();
        }
    });
});





