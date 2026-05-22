# Turtle Draw: Desenho de Cachorro (Bulldog Francês)

Este projeto implementa uma pipeline completa de visão computacional para extrair contornos de uma imagem de um cachorro e reproduzi-los no simulador `turtlesim` do ROS 2.

## Estrutura do Projeto

- `process_dog.py`: Script de processamento de imagem (fora do pacote ROS).
- `dog_draw_pkg/`: Pacote ROS 2 contendo o nó de controle.
  - `draw_node.py`: Nó que lê os pontos e comanda a tartaruga.
- `dog_paths.json`: Arquivo contendo as coordenadas dos contornos extraídos.

## Pipeline de Visão Computacional

A implementação seguiu as restrições técnicas do enunciado:
1. **Carregamento**: OpenCV utilizado apenas para `imread`.
2. **Pré-processamento**: 
   - Conversão para escala de cinza manual via NumPy (`0.299R + 0.587G + 0.114B`).
   - Suavização via Filtro Gaussiano.
3. **Detecção de Bordas**: Implementação manual do operador de **Sobel** para calcular o gradiente de magnitude.
4. **Extração de Contornos**: Algoritmo de busca por vizinho mais próximo para agrupar pontos de borda em caminhos sequenciais.
5. **Mapeamento**: As coordenadas da imagem foram mapeadas para o espaço do Turtlesim (1.0 a 10.0).

## Como Executar

1. Certifique-se de ter o ROS 2 instalado (Humble ou superior recomendado).
2. Instale as dependências de processamento (caso queira reprocessar a imagem):
   ```bash
   pip install numpy opencv-python scipy
   ```
3. Compile o pacote ROS 2:
   ```bash
   cd dog_draw_pkg
   colcon build
   source install/setup.bash
   ```
4. Em um terminal, inicie o Turtlesim:
   ```bash
   ros2 run turtlesim turtlesim_node
   ```
5. Em outro terminal, execute o nó de desenho:
```bash
chmod +x setup.sh
./setup.sh
```

## Justificativa dos Métodos
- **Sobel**: Escolhido por ser um método robusto de detecção de bordas que destaca bem transições de intensidade, essencial para capturar os detalhes da coleira e olhos do cachorro.
- **Vizinho Mais Próximo**: Utilizado para garantir que a tartaruga siga um caminho contínuo, minimizando levantamentos de caneta desnecessários.
