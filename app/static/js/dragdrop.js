// Sistema de Drag & Drop para ejercicios de ordenación

class DragDropManager {
    constructor() {
        this.userOrder = [];
        this.draggedElement = null;
        this.init();
    }
    
    init() {
        this.initDraggables();
        this.initDropZones();
    }
    
    initDraggables() {
        document.querySelectorAll('.draggable').forEach(item => {
            item.setAttribute('draggable', 'true');
            
            item.addEventListener('dragstart', (e) => {
                this.dragStart(e);
            });
            
            item.addEventListener('dragend', (e) => {
                this.dragEnd(e);
            });
            
            item.addEventListener('drag', (e) => {
                this.drag(e);
            });
        });
    }
    
    initDropZones() {
        const dropZones = document.querySelectorAll('.drop-zone');
        
        dropZones.forEach(zone => {
            zone.addEventListener('dragover', (e) => {
                this.dragOver(e);
            });
            
            zone.addEventListener('dragleave', (e) => {
                this.dragLeave(e);
            });
            
            zone.addEventListener('drop', (e) => {
                this.drop(e);
            });
        });
    }
    
    dragStart(e) {
        this.draggedElement = e.target;
        e.dataTransfer.setData('text/plain', e.target.outerHTML);
        e.dataTransfer.setData('element-type', e.target.dataset.element);
        e.target.classList.add('dragging');
        
        // Crear una imagen personalizada para el drag
        const dragIcon = e.target.cloneNode(true);
        dragIcon.style.width = '200px';
        dragIcon.style.opacity = '0.5';
        dragIcon.style.position = 'absolute';
        dragIcon.style.top = '-1000px';
        document.body.appendChild(dragIcon);
        e.dataTransfer.setDragImage(dragIcon, 0, 0);
        
        setTimeout(() => {
            document.body.removeChild(dragIcon);
        }, 0);
    }
    
    dragEnd(e) {
        e.target.classList.remove('dragging');
        this.draggedElement = null;
    }
    
    drag(e) {
        // Opcional: actualizar posición
    }
    
    dragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('drag-over');
    }
    
    dragLeave(e) {
        e.currentTarget.classList.remove('drag-over');
    }
    
    drop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
        
        const elementHTML = e.dataTransfer.getData('text/plain');
        const elementType = e.dataTransfer.getData('element-type');
        
        if (elementType && !this.userOrder.includes(elementType)) {
            this.userOrder.push(elementType);
            
            // Crear elemento visual
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = elementHTML;
            const element = tempDiv.firstChild;
            
            element.classList.remove('draggable', 'btn-outline-primary');
            element.classList.add('btn-success', 'disabled');
            element.setAttribute('draggable', 'false');
            element.style.cursor = 'default';
            
            e.currentTarget.appendChild(element);
            
            // Actualizar contador de orden
            this.updateOrderCounter();
        }
    }
    
    reset() {
        this.userOrder = [];
        document.querySelectorAll('.drop-zone').forEach(zone => {
            zone.innerHTML = '';
        });
        
        // Restaurar elementos disponibles
        this.restoreAvailableElements();
    }
    
    restoreAvailableElements() {
        // Esta función debe ser implementada según cada ejercicio
        console.log('Restaurando elementos...');
    }
    
    updateOrderCounter() {
        const counter = document.getElementById('order-counter');
        if (counter) {
            const total = document.querySelectorAll('.draggable').length;
            counter.textContent = `${this.userOrder.length}/${total}`;
        }
    }
    
    getOrder() {
        return this.userOrder;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.dragDropManager = new DragDropManager();
});
