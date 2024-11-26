let commentCount = 0;

// Carregar comentários salvos do Local Storage
function loadComments() {
    const savedComments = JSON.parse(localStorage.getItem('comments')) || [];
    savedComments.forEach(comment => {
        addCommentToList(comment);
    });
    commentCount = savedComments.length;
    document.getElementById('comment-count').innerText = commentCount;
}

// Adicionar um novo comentário à lista
function addComment() {
    const name = document.getElementById('name').value;
    const imageUrl = document.getElementById('image-url').value;
    const commentText = document.getElementById('comment').value;
    const now = new Date();
    const formattedDate = `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;

    if (name && imageUrl && commentText) {
        const newComment = {
            id: Date.now(),
            name: name,
            imageUrl: imageUrl,
            commentText: commentText,
            date: formattedDate
        };
        addCommentToList(newComment);

        // Salvar comentário no Local Storage
        const savedComments = JSON.parse(localStorage.getItem('comments')) || [];
        savedComments.push(newComment);
        localStorage.setItem('comments', JSON.stringify(savedComments));

        commentCount++;
        document.getElementById('comment-count').innerText = commentCount;

        // Limpar campos após adicionar o comentário
        document.getElementById('name').value = '';
        document.getElementById('image-url').value = '';
        document.getElementById('comment').value = '';
    } else {
        alert('Por favor, preencha todos os campos.');
    }
}

// Adicionar um comentário à lista na página
function addCommentToList(comment) {
    const commentList = document.getElementById('comments-list');
    const newComment = document.createElement('div');
    newComment.classList.add('comment');
    newComment.innerHTML = `
        <img src="${comment.imageUrl}" alt="${comment.name}">
        <div class="comment-content">
            <p><strong>${comment.name}</strong> <span class="date-time">(${comment.date})</span></p>
            <p>${comment.commentText}</p>
        </div>
        <button class="remove-button" onclick="removeComment(this)">Remover</button>
    `;
    commentList.appendChild(newComment);
}

// Remover um comentário da lista e do Local Storage
function removeComment(button) {
    const commentList = document.getElementById('comments-list');
    const commentToRemove = button.parentElement;
    commentList.removeChild(commentToRemove);

    // Atualizar Local Storage
    const savedComments = JSON.parse(localStorage.getItem('comments')) || [];
    const updatedComments = savedComments.filter(comment => 
        !(
            comment.name === commentToRemove.querySelector('.comment-content p strong').innerText &&
            comment.imageUrl === commentToRemove.querySelector('img').src &&
            comment.commentText === commentToRemove.querySelector('.comment-content p:nth-child(2)').innerText
        )
    );
    localStorage.setItem('comments', JSON.stringify(updatedComments));

    commentCount--;
    document.getElementById('comment-count').innerText = commentCount;
}

// Função para rolar para o topo da página com animação
function scrollToTop(event) {
    event.preventDefault(); // Evitar o comportamento padrão do link
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Carregar comentários ao carregar a página
window.onload = loadComments;
