// Front-end da Minha Coleção.
// Este arquivo já está pronto: a Clara não precisa mexer aqui.
// Ele só conversa com o back-end pelas rotas do contrato (docs/contrato-da-api.md).

const STATUS = {
  quero: "Quero conhecer",
  em_andamento: "Em andamento",
  concluido: "Concluído",
  abandonado: "Abandonado",
};

const $ = (id) => document.getElementById(id);

// ---------------------------------------------------------------------------
// Chamada à API: devolve o JSON ou lança um Error com mensagem legível
// ---------------------------------------------------------------------------
async function api(metodo, caminho, corpo) {
  const opcoes = { method: metodo, headers: {} };
  if (corpo !== undefined) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }
  let resposta;
  try {
    resposta = await fetch(caminho, opcoes);
  } catch {
    throw new Error("Não consegui falar com o back-end. O servidor (uvicorn) está rodando?");
  }
  if (resposta.status === 204) return null;

  let dados = null;
  try { dados = await resposta.json(); } catch { /* resposta sem JSON */ }

  if (!resposta.ok) {
    let msg = `${metodo} ${caminho} respondeu ${resposta.status}`;
    if (resposta.status === 500) msg += " — erro no servidor (talvez essa rota ainda seja um TODO? veja o terminal do uvicorn)";
    else if (resposta.status === 404 && !dados?.detail) msg += " — rota não encontrada (ainda não foi criada?)";
    if (dados?.detail) {
      msg += ": " + (typeof dados.detail === "string" ? dados.detail : JSON.stringify(dados.detail));
    }
    throw new Error(msg);
  }
  return dados;
}

function avisar(mensagem) {
  const el = $("aviso");
  el.textContent = mensagem;
  el.hidden = !mensagem;
}

// ---------------------------------------------------------------------------
// Cartões
// ---------------------------------------------------------------------------
function el(tag, classe, texto) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (texto !== undefined && texto !== null) e.textContent = texto;
  return e;
}

function capa(item) {
  const div = el("div", "capa");
  if (item.imagem_url) {
    const img = document.createElement("img");
    img.src = item.imagem_url;
    img.alt = "";
    img.loading = "lazy";
    div.append(img);
  } else {
    div.textContent = "sem imagem";
  }
  return div;
}

function cartaoBase(item) {
  const cartao = el("article", "cartao");
  const corpo = el("div", "corpo");
  corpo.append(el("h3", null, item.titulo));
  const meta = [item.subtitulo, item.ano].filter(Boolean).join(" · ");
  if (meta) corpo.append(el("p", "meta", meta));
  if (item.descricao) {
    cartao.title = item.descricao.length > 300 ? item.descricao.slice(0, 300) + "…" : item.descricao;
  }
  cartao.append(capa(item), corpo);
  return { cartao, corpo };
}

function cartaoResultado(item) {
  const { cartao, corpo } = cartaoBase(item);
  const acoes = el("div", "acoes");
  const botao = el("button", null, "Adicionar");
  botao.onclick = () => abrirDialogo({ modo: "criar", item });
  acoes.append(botao);
  corpo.append(acoes);
  return cartao;
}

function cartaoColecao(item) {
  const { cartao, corpo } = cartaoBase(item);
  corpo.append(el("span", "etiqueta", STATUS[item.status] || item.status));
  if (item.nota) corpo.append(el("span", "estrelas", "★".repeat(item.nota)));
  if (item.comentario) corpo.append(el("p", "comentario", `“${item.comentario}”`));

  const acoes = el("div", "acoes");
  const editar = el("button", "secundario", "Editar");
  editar.onclick = () => abrirDialogo({ modo: "editar", item });
  const remover = el("button", "perigo", "Remover");
  remover.onclick = () => removerItem(item);
  acoes.append(editar, remover);
  corpo.append(acoes);
  return cartao;
}

function preencher(container, itens, criarCartao, textoVazio) {
  container.replaceChildren();
  if (!itens.length) {
    container.append(el("p", "vazio", textoVazio));
    return;
  }
  for (const item of itens) container.append(criarCartao(item));
}

// ---------------------------------------------------------------------------
// Ações
// ---------------------------------------------------------------------------
async function buscar(evento) {
  evento.preventDefault();
  const termo = $("campo-busca").value.trim();
  if (!termo) return;
  avisar("");
  const resultados = $("resultados");
  resultados.replaceChildren(el("p", "vazio", "Buscando…"));
  try {
    const itens = await api("GET", `/api/buscar?q=${encodeURIComponent(termo)}`);
    preencher(resultados, itens, cartaoResultado, `Nada encontrado para “${termo}”.`);
  } catch (erro) {
    resultados.replaceChildren();
    avisar(erro.message);
  }
}

async function carregarColecao() {
  const status = $("filtro-status").value;
  const caminho = status ? `/api/itens?status=${status}` : "/api/itens";
  try {
    const itens = await api("GET", caminho);
    preencher($("colecao"), itens, cartaoColecao, "Sua lista está vazia. Busque algo e clique em Adicionar.");
  } catch (erro) {
    $("colecao").replaceChildren();
    avisar(erro.message);
  }
}

async function removerItem(item) {
  if (!confirm(`Remover “${item.titulo}” da sua lista?`)) return;
  try {
    await api("DELETE", `/api/itens/${item.id}`);
    avisar("");
    carregarColecao();
  } catch (erro) {
    avisar(erro.message);
  }
}

async function recomendar() {
  const caixa = $("recomendacao");
  caixa.hidden = false;
  caixa.textContent = "Pensando…";
  try {
    const r = await api("GET", "/api/recomendacoes");
    caixa.replaceChildren();
    if (r?.item) caixa.append(el("strong", null, r.item.titulo), el("span", null, " — "));
    caixa.append(el("span", null, r?.motivo || "Sem sugestão por enquanto."));
  } catch (erro) {
    caixa.hidden = true;
    avisar(erro.message);
  }
}

// ---------------------------------------------------------------------------
// Diálogo de adicionar/editar
// ---------------------------------------------------------------------------
let contextoDialogo = null;

function abrirDialogo(contexto) {
  contextoDialogo = contexto;
  const { item, modo } = contexto;
  $("dialogo-titulo").textContent = (modo === "criar" ? "Adicionar: " : "Editar: ") + item.titulo;
  $("campo-status").value = item.status || "quero";
  $("campo-nota").value = item.nota ? String(item.nota) : "";
  $("campo-comentario").value = item.comentario || "";
  $("dialogo").showModal();
}

async function salvarDialogo(evento) {
  evento.preventDefault();
  const { item, modo } = contextoDialogo;
  const nota = $("campo-nota").value;
  const campos = {
    status: $("campo-status").value,
    nota: nota ? Number(nota) : null,
    comentario: $("campo-comentario").value.trim() || null,
  };
  try {
    if (modo === "criar") {
      const { id_externo, titulo, subtitulo, ano, imagem_url, descricao } = item;
      await api("POST", "/api/itens", { id_externo, titulo, subtitulo, ano, imagem_url, descricao, ...campos });
    } else {
      await api("PUT", `/api/itens/${item.id}`, campos);
    }
    $("dialogo").close();
    avisar("");
    carregarColecao();
  } catch (erro) {
    $("dialogo").close();
    avisar(erro.message);
  }
}

// ---------------------------------------------------------------------------
// Início
// ---------------------------------------------------------------------------
async function iniciar() {
  for (const [valor, texto] of Object.entries(STATUS)) {
    $("filtro-status").append(new Option(texto, valor));
    $("campo-status").append(new Option(texto, valor));
  }

  $("form-busca").addEventListener("submit", buscar);
  $("filtro-status").addEventListener("change", carregarColecao);
  $("form-item").addEventListener("submit", salvarDialogo);
  $("botao-cancelar").addEventListener("click", () => $("dialogo").close());
  $("botao-recomendar").addEventListener("click", recomendar);

  try {
    const p = await api("GET", "/api/provedor");
    $("provedor-nome").textContent = `Provedor de dados: ${p.nome}`;
    const credito = $("credito");
    if (p.credito_url) {
      const link = el("a", null, p.credito_texto);
      link.href = p.credito_url;
      link.target = "_blank";
      link.rel = "noopener";
      credito.append(link);
    } else {
      credito.textContent = p.credito_texto;
    }
  } catch (erro) {
    $("provedor-nome").textContent = "";
    avisar(erro.message);
  }

  // O botão de recomendação só aparece se a rota existir no back-end
  try {
    const openapi = await api("GET", "/openapi.json");
    $("botao-recomendar").hidden = !openapi.paths["/api/recomendacoes"];
  } catch { /* sem openapi, sem botão */ }

  carregarColecao();
}

iniciar();
