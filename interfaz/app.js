document.addEventListener('DOMContentLoaded', function () {
  const runButton = document.querySelector('.run-button');
  const codeTextarea = document.querySelector('.code-textarea');
  const outputContent = document.querySelector('.output-content');
  const analysisButtons = document.querySelectorAll('.button-analizador');

  let currentAnalysis = 'lexico'; // Valor por defecto

  // Configurar botones de análisis
  analysisButtons.forEach(button => {
    button.addEventListener('click', function () {
      analysisButtons.forEach(btn => btn.classList.remove('active'));
      this.classList.add('active');
      currentAnalysis = this.dataset.tab;
    });
  });
  runButton.addEventListener('click', async function () {
    const codigo = codeTextarea.value.trim();

    if (!codigo) {
      outputContent.textContent = 'Error: Ingresa código Dart para analizar';
      return;
    }

    outputContent.innerHTML = `<div class="loading">Analizando...</div>`;

    try {
      let resultado;
      switch (currentAnalysis) {
        case 'lexico':
          resultado = await enviarAnalisisAlBackend(codigo, 'lexico');
          outputContent.innerHTML = formatearResultadoLexico(resultado);
          break;
        case 'sintactico':
          outputContent.innerHTML = 'Análisis sintáctico no implementado aún';
          break;
        case 'semantico':
          outputContent.innerHTML = 'Análisis semántico no implementado aún';
          break;
        case 'todo':
          outputContent.innerHTML = 'Análisis completo no implementado aún';
          break;
      }
    } catch (error) {
      outputContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
  });

  async function enviarAnalisisAlBackend(codigo, tipo) {
    try {
      const response = await fetch('http://127.0.0.1:5000/analizar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          codigo: codigo,
          tipo: tipo
        })
      });
      
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
      
      return await response.json();
    } catch (error) {
      throw new Error(`Error al conectar con el servidor: ${error.message}`);
    }
  }

  function formatearResultadoLexico(resultado) {
    if (resultado.status === 'error') {
      return `<div class="error">${resultado.message}</div>`;
    }

    let html = '<div class="resultado-lexico">';
    html += '<h3>Resultado del Análisis Léxico</h3>';
    html += '<table><tr><th>Tipo</th><th>Valor</th><th>Línea</th></tr>';
    
    resultado.tokens.forEach(token => {
      html += `<tr>
          <td>${token.type}</td>
          <td>${token.value}</td>
          <td>${token.lineno}</td>
      </tr>`;
    });
    
    html += '</table>';
    html += `<p class="total-tokens">Total de tokens encontrados: ${resultado.total_tokens}</p>`;
    html += '</div>';
    return html;
  }
});