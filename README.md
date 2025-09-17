My Clicker Game
Um jogo de clique incremental (clicker) desenvolvido em Python com Pygame, onde você coleta pontos, compra melhorias e automatiza sua produção.

https://img.shields.io/badge/Python-3.6%252B-blue.svg
https://img.shields.io/badge/Pygame-2.0%252B-green.svg

🎮 Sobre o Jogo
My Clicker é um jogo incremental onde você começa clicando para ganhar pontos e gradualmente compra melhorias que geram pontos automaticamente. O jogo inclui:

Sistema de clique manual para ganhar pontos

Cursores automáticos que geram pontos a cada 2.5 segundos

Spaceships que produzem ainda mais pontos

Sistema de economia com preços que aumentam após cada compra

Upgrade secreto para melhorar seu clique manual

Animações visuais dos itens comprados

Sistema de salvamento automático do progresso

🚀 Como Executar
Pré-requisitos
Python 3.6 ou superior

Biblioteca Pygame

Instalação
Clone este repositório:

bash
git clone https://github.com/seu-usuario/my-clicker-game.git
cd my-clicker-game
Instale as dependências:

bash
pip install pygame
Execute o jogo:

bash
python main.py
Controles
Clique do mouse ou Espaço: Ganha pontos

Botão de Loja: Abre/fecha a loja de melhorias

Botão Salvar: Salva o progresso do jogo

Botão Carregar: Carrega o jogo salvo

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
💡 Funcionalidades
Sistema de Produção
Clique manual: 1 ponto por clique (3 com upgrade)

Cursores: Produzem 5 pontos a cada 2.5 segundos

Spaceships: Produzem 20 pontos a cada 2.5 segundos

Sistema Econômico
Os preços aumentam após cada compra:

Cursores: +20% por compra

Spaceships: +30% por compra

Easter Egg
Clique no ponto do "i" do título quando tiver exatamente 69 pontos para desbloquear um upgrade secreto!

Salvamento Automático
Seu progresso é salvo automaticamente em save_game.json

Inclui todos os dados importantes: pontos, itens comprados e preços atuais

🎨 Personalização
O jogo foi desenvolvido para ser flexível e permite fácil personalização:

Modifique as imagens na pasta images/ para alterar a aparência

Ajuste os valores de produção e preços no código

Adicione novos tipos de melhorias seguindo o padrão existente

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para:

Fazer um fork do projeto

Criar uma branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abrir um Pull Request

🐛 Reportar Problemas
Encontrou um bug ou tem uma sugestão? Por favor, abra uma issue no GitHub.
