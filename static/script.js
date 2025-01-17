document.querySelectorAll('.task-item .circle').forEach(circle => {
    circle.addEventListener('click', function () {
        const taskItem = this.closest('.task-item');
        const taskId = taskItem.getAttribute('data-task-id');

        taskItem.classList.toggle('completed');

        fetch(`/complete/${taskId}`)
            .then(response => {
                if (!response.ok) {
                    taskItem.classList.toggle('completed');
                }
            })
            .catch(err => {
                console.error('Failed to update task status:', err);
                taskItem.classList.toggle('completed');
            });
    });
});
