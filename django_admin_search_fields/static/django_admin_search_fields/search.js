function applyRedBorder(element) {
    element.style.border = '1px solid red';
    setTimeout(() => { element.style.border = '' }, 300);
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('changelist-search');
    if (!form) return

    const searchInput = document.getElementById('searchbar');
    const checkboxes = document.querySelectorAll('#search-fields input[type="checkbox"]');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const query = searchInput.value.trim();

        let selectedOptions = [];
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedOptions.push(checkbox.value);
            }
        });

        let params = new URLSearchParams();

        if (!query) {
            applyRedBorder(searchInput);
            return;
        }
        if (selectedOptions.length < 1) {
            applyRedBorder(document.getElementById('search-fields'))
            return;
        }

        params.append('q', query);

        selectedOptions.forEach(option => {
            params.append('search-fields', option);
        });

        const url = new URL(window.location.href);
        url.search = params.toString();
        window.location.href = url.toString();
    });
});