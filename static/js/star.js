function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-star-form]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const button = form.querySelector('[data-star-button]');
            const label = form.querySelector('[data-star-label]');
            const count = form.querySelector('[data-star-count]');

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (!response.ok) {
                    form.submit();
                    return;
                }

                const data = await response.json();

                label.textContent = data.starred ? 'Unstar' : 'Star';
                count.textContent = data.count;
                button.classList.toggle('is-starred', data.starred);
            } catch (error) {
                form.submit();
            }
        });
    });
});