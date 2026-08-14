# Setup — perfil terminal Kali

Guia rápido pra colocar tudo no ar. Tempo estimado: ~15 min.

## 0. Pré-requisito: o "repo especial"

No GitHub, um repositório com **o mesmo nome do seu usuário** vira o perfil.
Como seu usuário é `Daniel16Bit`, crie um repo público chamado **`Daniel16Bit`**
com um README inicial. É nele que tudo isto vai morar.

> Se o seu usuário for outro, troque **todas** as ocorrências de `Daniel16Bit`
> nos arquivos (README.md, workflows, URLs). Um find-and-replace resolve.

## 1. Suba os arquivos

Copie para a raiz do repo, mantendo a estrutura:

```
Daniel16Bit/
├── README.md
├── projects.json
├── banner-dark.svg          (já gerado; a Action regenera depois)
├── banner-light.svg
├── logos/                   (coloque aqui os PNG/SVG dos projetos)
└── .github/
    ├── scripts/
    │   ├── generate_banner.py
    │   ├── generate_projects.py
    │   └── fetch_data.py
    └── workflows/
        ├── banner.yml
        ├── projects.yml
        └── snake.yml
```

```bash
git clone https://github.com/Daniel16Bit/Daniel16Bit.git
cd Daniel16Bit
# copie os arquivos aqui
git add .
git commit -m "perfil terminal kali"
git push
```

## 2. Personalize (o essencial)

- **Banner:** abra `.github/scripts/generate_banner.py` e edite o dicionário
  `CONFIG` no topo — nome, cargo, stack, e-mail, comandos do terminal. Tudo num
  lugar só. Depois rode `python3 .github/scripts/generate_banner.py .` local, ou
  deixe a Action fazer.
- **Projetos:** edite `projects.json`. Cada item é um card. `repo` no formato
  `usuario/repo`. `logo` é o nome do arquivo dentro de `logos/` (deixe `""` pra
  usar o monograma). Reordenar o array reordena os cards.
- **README:** já vem com seus contatos (LinkedIn `mdaniel-main`, GitHub
  `@Daniel16Bit`, Instagram `@daniel8bit`, e-mail `mdaniel.main@gmail.com`).
  Confira só se algum link mudou.

## 3. Ative as Actions

Na aba **Actions** do repo, habilite os workflows. Depois, em
**Settings → Actions → General → Workflow permissions**, marque
**Read and write permissions** (as Actions precisam commitar de volta).

Rode cada workflow uma vez manualmente (**Actions → [workflow] → Run workflow**):
1. **Generate Snake Animation** — cria a branch `output` com a cobrinha.
2. **Generate Projects Panel** — cria a branch `projects` com o painel.
3. **Generate Banner** — regenera os SVGs do banner no `main`.

Pronto. Daí em diante:
- Snake atualiza sozinha a cada 12h.
- Projetos atualizam a cada 6h (estrelas, linguagens, "updated Xd ago").
- Banner só regenera quando você editar o script.

## Como funciona (resumo)

Nada é "terminal de verdade" — é tudo **SVG desenhado por Python** pra parecer um.
As Actions rodam os scripts na nuvem, geram os SVGs e commitam em branches
separadas (`projects`, `output`); o README aponta pra esses arquivos via
`raw.githubusercontent.com`. A tag `<picture>` troca dark/light conforme o tema
do GitHub de quem visita.

## Ajustes rápidos

- **Cores:** dicionário `THEMES` no topo de cada script `generate_*.py`. A
  paleta atual é azul/escuro (`#38BDF8` de destaque sobre `#060A14`). Trocar a
  cor de destaque nos dois scripts + no `snake.yml` muda o visual inteiro.
- **Tamanho do banner:** `W, H` em `generate_banner.py`.
- **Cores da snake:** parâmetros `color_snake`/`color_dots` em `snake.yml`
  (use `%23` no lugar de `#` no `color_snake`).
- **Stats não aparecem?** O `github-readme-stats` público às vezes bate rate
  limit. Dá pra subir sua própria instância na Vercel (repo
  `anuraghazra/github-readme-stats`) e trocar a URL.
