#!/bin/bash

# Cores para o terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Iniciando configuração automática do Dog Draw...${NC}"

# 1. Garantir permissão de execução no nó
echo -e "${GREEN}Configurando permissões...${NC}"
chmod +x dog_draw_pkg/dog_draw_pkg/draw_node.py

# 2. Limpar builds antigos (opcional)
# rm -rf build/ install/ log/

# 3. Compilar o pacote
echo -e "${GREEN}Compilando o pacote com colcon...${NC}"
colcon build

# 4. Source do ambiente
echo -e "${GREEN}Configurando ambiente (source)...${NC}"
source install/setup.bash

# 5. Aviso sobre o turtlesim
echo -e "${BLUE}Certifique-se de que o 'ros2 run turtlesim turtlesim_node' está rodando em outro terminal!${NC}"
echo -e "${BLUE}Iniciando o desenho em 3 segundos...${NC}"
sleep 3

# 6. Executar com saída de log visível
echo -e "${GREEN}Iniciando o nó de desenho... Observe os logs abaixo:${NC}"
ros2 run dog_draw_pkg draw_node --ros-args --log-level info
