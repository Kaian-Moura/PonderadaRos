#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import json
import time
import os
import threading

class DogDrawNode(Node):
    def __init__(self, paths):
        super().__init__('dog_draw_node')
        self.paths = paths
        
        # Clientes para serviços do turtlesim
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        
        # Aguardar serviços
        self.get_logger().info('Aguardando serviços do turtlesim...')
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando serviço de teleporte...')
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando serviço de caneta...')
            
        # Iniciar a thread de desenho para não bloquear o executor do ROS
        self.drawing_thread = threading.Thread(target=self.run_drawing)
        self.drawing_thread.start()

    def set_pen(self, r, g, b, width, off):
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = off
        # Chamada síncrona dentro de uma thread separada é segura
        future = self.pen_client.call_async(req)
        # Em uma thread separada, podemos esperar pelo resultado se necessário
        # Mas para o turtlesim, disparar e seguir costuma funcionar para o desenho

    def teleport(self, x, y, theta):
        req = TeleportAbsolute.Request()
        req.x = float(x)
        req.y = float(y)
        req.theta = float(theta)
        self.teleport_client.call_async(req)

    def run_drawing(self):
        try:
            self.get_logger().info('Iniciando o desenho do Bulldog Francês...')
            
            for path_idx, path in enumerate(self.paths):
                if not path: continue
                
                # Levantar a caneta e ir para o início do caminho
                self.set_pen(0, 0, 0, 0, 1) # Pen off
                time.sleep(0.1) # Pequeno delay para garantir que o serviço foi processado
                
                self.teleport(path[0][0], path[0][1], 0.0)
                time.sleep(0.1)
                
                # Abaixar a caneta
                self.set_pen(255, 255, 255, 2, 0) # Pen on, cor branca (ou ajuste conforme preferir)
                time.sleep(0.1)
                
                # Percorrer os pontos
                num_points = len(path)
                self.get_logger().info(f'Desenhando caminho {path_idx + 1}/{len(self.paths)} ({num_points} pontos)')
                
                for i, point in enumerate(path[1:]):
                    self.teleport(point[0], point[1], 0.0)
                    # O delay controla a velocidade do desenho
                    time.sleep(0.01)
                    
            self.get_logger().info('Desenho concluído com sucesso!')
            
        except Exception as e:
            self.get_logger().error(f'Erro durante o desenho: {e}')
        
        # Encerrar o nó após o término
        # rclpy.shutdown() # Pode ser agressivo, melhor deixar o main lidar

def main(args=None):
    rclpy.init(args=args)
    
    # Tentar localizar o arquivo JSON
    json_path = 'dog_paths_v2.json'
    if not os.path.exists(json_path):
        # Tenta no diretório onde o script está
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', '..', 'dog_paths_v2.json')
        
    if not os.path.exists(json_path):
        print(f"ERRO: Arquivo {json_path} não encontrado!")
        return

    try:
        with open(json_path, 'r') as f:
            paths = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar caminhos: {e}")
        return

    node = DogDrawNode(paths)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
