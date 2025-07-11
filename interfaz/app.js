// ===== CONFIGURACIÓN INICIAL =====
document.addEventListener('DOMContentLoaded', function() {
  // Selecciona todos los grupos de botones en la página
  document.querySelectorAll('.button-group').forEach(group => {
    initButtonGroup(group);
  });
});

// ===== FUNCIÓN PRINCIPAL =====
function initButtonGroup(buttonGroup) {
  const buttons = buttonGroup.querySelectorAll('.button-analizador');
  
  // 1. Configura el evento click para cada botón
  buttons.forEach(button => {
    button.addEventListener('click', handleButtonClick);
  });
  
  // 2. Recupera la selección guardada (opcional)
  const groupId = buttonGroup.id || 'default';
  const savedSelection = localStorage.getItem(`selectedButton-${groupId}`);
  
  if (savedSelection) {
    const selectedBtn = buttonGroup.querySelector(`[data-tab="${savedSelection}"]`);
    if (selectedBtn) selectedBtn.classList.add('active');
  }
}

// ===== MANEJADOR DE CLIC =====
function handleButtonClick() {
  const buttonGroup = this.closest('.button-group');
  const groupId = buttonGroup.id || 'default';
  const tabId = this.dataset.tab;
  
  // 1. Remover clase 'active' de todos los botones del grupo
  buttonGroup.querySelectorAll('.button-analizador').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // 2. Añadir clase 'active' al botón clickeado
  this.classList.add('active');
  
  // 3. Guardar selección (opcional)
  localStorage.setItem(`selectedButton-${groupId}`, tabId);
  
  // 4. Ejecutar función asociada al botón
  executeTabFunction(tabId);
}

// ===== FUNCIONES POR BOTÓN =====
function executeTabFunction(tabId) {
  switch(tabId) {
    case 'lexico':
      console.log('Ejecutando análisis léxico');
      // Tu código para análisis léxico aquí
      break;
      
    case 'sintactico':
      console.log('Ejecutando análisis sintáctico');
      // Tu código para análisis sintáctico aquí
      break;
      
    case 'semantico':
      console.log('Ejecutando análisis semántico');
      // Tu código para análisis semántico aquí
      break;
      
    default:
      console.warn(`Función no definida para el tab: ${tabId}`);
  }
}

// ===== FUNCIONES ADICIONALES =====
function resetButtonGroup(groupId = 'default') {
  localStorage.removeItem(`selectedButton-${groupId}`);
  document.querySelectorAll('.button-analizador').forEach(btn => {
    btn.classList.remove('active');
  });
}