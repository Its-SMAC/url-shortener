const form = document.getElementById("shortenForm");
const formDiv = document.querySelector(".form");
const resultadoDiv = document.querySelector(".resultado");
const urlInput = document.getElementById("urlInput");
const urlCurto = document.getElementById("urlCurto");
const copiarBtn = document.getElementById("copiarBtn");
const novoBtn = document.getElementById("novoBtn");

// 2. SUBMIT DO FORM
form.addEventListener("submit", async (e) => {
  e.preventDefault(); // Impede reload da página

  // Pega o URL que user escreveu
  const url = urlInput.value;

  try {
    // Envia para backend
    const response = await fetch(
      "https://url-shortener-kvin.onrender.com/shorten",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
      }
    );

    // Converte resposta para JSON
    const data = await response.json();

    // Se der erro
    if (!response.ok) {
      alert("Erro: " + data.erro);
      return;
    }

    // SUCESSO! Mostra resultado
    urlCurto.value = data.url_curto;
    formDiv.style.display = "none";
    resultadoDiv.style.display = "block";
  } catch (error) {
    alert("Erro ao conectar com servidor!");
    console.error(error);
  }
});

// 3. BOTÃO COPIAR
copiarBtn.addEventListener("click", () => {
  // Seleciona o texto
  urlCurto.select();

  // Copia para clipboard
  navigator.clipboard
    .writeText(urlCurto.value)
    .then(() => {
      // Feedback visual
      const textoOriginal = copiarBtn.textContent;
      copiarBtn.textContent = "Copiado! ✓";

      // Volta ao normal após 2 segundos
      setTimeout(() => {
        copiarBtn.textContent = textoOriginal;
      }, 2000);
    })
    .catch((err) => {
      alert("Erro ao copiar!");
    });
});

// 4. BOTÃO NOVO (RESET)
novoBtn.addEventListener("click", () => {
  // Limpa o input
  urlInput.value = "";

  // Limpa o resultado
  urlCurto.value = "";

  // Esconde resultado, mostra form
  resultadoDiv.style.display = "none";
  formDiv.style.display = "block";

  // Foca no input (cursor aparece lá)
  urlInput.focus();
});
