// Sistema de Flashcards interactivo

class FlashcardManager {
    constructor() {
        this.currentCard = null;
        this.cards = [];
        this.currentIndex = 0;
        this.completed = [];
        this.init();
    }
    
    init() {
        this.loadCards();
        this.initEventListeners();
    }
    
    loadCards() {
        // Cargar desde el atributo data de las flashcards
        const flashcardElements = document.querySelectorAll('.flashcard-item');
        this.cards = Array.from(flashcardElements).map(el => ({
            id: el.dataset.id,
            front: el.dataset.front,
            back: el.dataset.back,
            difficulty: el.dataset.difficulty
        }));
    }
    
    initEventListeners() {
        // Flip de flashcards
        document.querySelectorAll('.flashcard').forEach(card => {
            card.addEventListener('click', (e) => {
                this.flipCard(card);
            });
        });
        
        // Botones de navegación
        document.getElementById('prev-card')?.addEventListener('click', () => {
            this.prevCard();
        });
        
        document.getElementById('next-card')?.addEventListener('click', () => {
            this.nextCard();
        });
        
        // Filtros
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterCards(e.target.dataset.filter);
            });
        });
        
        // Marcar como completado
        document.getElementById('mark-complete')?.addEventListener('click', (e) => {
            this.markAsCompleted(e.target.dataset.cardId);
        });
    }
    
    flipCard(card) {
        card.classList.toggle('flipped');
    }
    
    nextCard() {
        if (this.currentIndex < this.cards.length - 1) {
            this.currentIndex++;
            this.showCard(this.currentIndex);
        }
    }
    
    prevCard() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.showCard(this.currentIndex);
        }
    }
    
    showCard(index) {
        const card = this.cards[index];
        const container = document.getElementById('flashcard-container');
        
        if (container && card) {
            container.innerHTML = `
                <div class="flashcard" data-id="${card.id}">
                    <div class="flashcard-inner">
                        <div class="flashcard-front">
                            <h3>${card.front}</h3>
                            <p class="text-muted mt-3">Haz clic para ver la respuesta</p>
                        </div>
                        <div class="flashcard-back">
                            <h4>${card.back}</h4>
                        </div>
                    </div>
                </div>
            `;
            
            // Actualizar contador
            document.getElementById('card-counter').textContent = 
                `${index + 1}/${this.cards.length}`;
        }
    }
    
    filterCards(filter) {
        // Actualizar botones activos
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Filtrar flashcards
        const cards = document.querySelectorAll('.flashcard-item');
        cards.forEach(card => {
            if (filter === 'all' || card.dataset.difficulty === filter) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    markAsCompleted(cardId) {
        if (!this.completed.includes(cardId)) {
            this.completed.push(cardId);
            
            // Actualizar UI
            const card = document.querySelector(`.flashcard-item[data-id="${cardId}"]`);
            if (card) {
                card.classList.add('completed');
            }
            
            // Actualizar contador de progreso
            this.updateProgress();
            
            // Enviar al servidor
            this.saveProgress(cardId);
        }
    }
    
    updateProgress() {
        const total = this.cards.length;
        const completed = this.completed.length;
        const percentage = (completed / total) * 100;
        
        const progressBar = document.getElementById('flashcard-progress');
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
        }
        
        document.getElementById('completed-count').textContent = completed;
        document.getElementById('total-count').textContent = total;
    }
    
    saveProgress(cardId) {
        fetch('/api/flashcard/progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                card_id: cardId,
                completed: true
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Progreso guardado:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    shuffleCards() {
        // Algoritmo Fisher-Yates
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
        this.currentIndex = 0;
        this.showCard(0);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.flashcardManager = new FlashcardManager();
});
