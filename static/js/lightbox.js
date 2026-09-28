document.addEventListener('DOMContentLoaded', () => {
    const closeLightbox = () => {
        if (location.hash.startsWith('#img-modal-')) {
            location.replace('#close');
        }
    };

    // Escape key closes the open lightbox
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });

    // Clicking the dark backdrop (not the image itself) closes it
    document.querySelectorAll('.lightbox-modal').forEach((modal) => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeLightbox();
        });
    });
});