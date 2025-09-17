  **My Clicker Game**
Um jogo de clique incremental (clicker) desenvolvido em Python com Pygame, onde você coleta pontos, compra melhorias e automatiza sua produção.

https://img.shields.io/badge/Python-3.6%252B-blue.svg
https://img.shields.io/badge/Pygame-2.0%252B-green.svg

  **Sobre o Jogo**
My Clicker é um jogo onde você clica para ganhar pontos e com isso comprar melhorias. O jogo inclui atualmente:

Sistema de clique manual para ganhar pontos

Cursores automáticos que geram pontos a cada 2.5 segundos

Objetos diversos para se comprar na loja (geram pontos gradualmente assim como os cursores).

Sistema de economia com preços que aumentam após cada compra

Upgrade secreto para melhorar seu clique manual

Animações visuais dos itens comprados

Sistema de salvamento manual do progresso

  **Como Executar**
*Pré-requisitos:*
Python 3.6 ou superior

Biblioteca Pygame

*Instalação:*
Clone este repositório pelo github ou pelo comando a baixo:

git clone https://github.com/""seu-usuario""/my-clicker.git
cd my-clicker

*Instale as dependências:*

pip install pygame

*Execute o jogo*

  **Controles**
Clique do mouse ou Espaço: Ganha pontos

Botão de Loja: Abre/fecha a loja de melhorias

Botão Salvar (disquete): Salva o progresso do jogo

Botão Carregar (na direita do botão salvar): Carrega o jogo salvo

ESC: Sai do jogo

🛠 Estrutura do Projeto
text
my-clicker-game/
│
├── main.py                 # Arquivo principal do jogo
├── save_game.json          # Arquivo de salvamento (gerado automaticamente)
├── images/                 # Pasta com imagens do jogo
│   ├── cursor.png          # Ícone do cursor
│   ├── spaceship.png       # Ícone da spaceship
│   ├── click_button.png    # Botão de clique
│   └── ...                # Outras imagens
└── README.md              # Este arquivo
  **Funcionalidades**
Sistema de Produção
Clique manual: 1 ponto por clique (3 com upgrade)

Cursores: Produzem 5 pontos a cada 2.5 segundos

Spaceships: Produzem 20 pontos a cada 2.5 segundos

Sistema Econômico
Os preços aumentam após cada compra e também variam com um acréscimo de 5% até 45% a cada 5min.

Cursores: +15% por compra

Spaceships: +25% por compra

  **Personalização**
O jogo foi desenvolvido para ser flexível e permite fácil personalização:

Modifique as imagens na pasta images/ para alterar a aparência

Ajuste os valores de produção e preços no código

Adicione novos tipos de melhorias seguindo o padrão existente

  **Contribuições**
Contribuições são bem-vindas! Sinta-se à vontade para:

Fazer um fork do projeto

Criar uma branch para sua feature

Commit suas mudanças

Push para a branch

Abrir um Pull Request

  **Reportar Problemas**
Encontrou um bug ou tem uma sugestão? Por favor, abra uma issue no GitHub.
