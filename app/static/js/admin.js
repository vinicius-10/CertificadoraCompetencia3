/**
 * Handles sorting interactions on the admin user table.
 *
 * Sorting state is stored in hidden inputs so HTMX requests for filters,
 * reports, and table refreshes all use the same parameters.
 */
document.addEventListener("DOMContentLoaded", () => {
    const sortButtons = document.querySelectorAll(".table-sort-button");
    const sortByInput = document.getElementById("sort-by");
    const sortDirInput = document.getElementById("sort-dir");

    if (!sortButtons.length || !sortByInput || !sortDirInput) {
        return;
    }

    sortButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const sortField = button.dataset.sortField;
            const isCurrentField = sortByInput.value === sortField;
            const nextDirection = isCurrentField && sortDirInput.value === "asc" ? "desc" : "asc";

            sortByInput.value = sortField;
            sortDirInput.value = nextDirection;

            updateSortHeader(sortButtons, button, nextDirection);

            if (window.htmx) {
                htmx.trigger(document.body, "refreshTable");
            }
        });
    });
});


/**
 * Updates the active visual state for the selected sortable table header.
 *
 * @param {NodeListOf<HTMLButtonElement>} sortButtons - Sort header buttons.
 * @param {HTMLButtonElement} activeButton - Header selected by the user.
 * @param {string} sortDirection - Current sort direction, either `asc` or `desc`.
 * @returns {void}
 */
function updateSortHeader(sortButtons, activeButton, sortDirection) {
    sortButtons.forEach((button) => {
        button.classList.remove("is-active");
        button.removeAttribute("data-sort-dir");
    });

    activeButton.classList.add("is-active");
    activeButton.dataset.sortDir = sortDirection;
}
