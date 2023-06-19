from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

def create_cellular_network():
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

    # Adicionando um controlador OpenFlow
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Adicionando uma estação base e uma torre de celular
    bs = net.addHost('bs', ip='192.168.0.1/24', mac='00:00:00:00:00:01')
    tower = net.addSwitch('tower')

    # Adicionando hosts para representar os dispositivos móveis
    mobile1 = net.addHost('mobile1', ip='192.168.0.2/24', mac='00:00:00:00:00:02')
    mobile2 = net.addHost('mobile2', ip='192.168.0.3/24', mac='00:00:00:00:00:03')

    # Adicionando enlaces entre a estação base, a torre de celular e os dispositivos móveis
    net.addLink(bs, tower)
    net.addLink(mobile1, tower)
    net.addLink(mobile2, tower)

    # Iniciando a rede
    net.build()
    c0.start()
    tower.start([c0])

    # Configurando as interfaces da estação base e dos dispositivos móveis
    bs.cmd('ifconfig bs-eth0 0')
    mobile1.cmd('ifconfig mobile1-eth0 0')
    mobile2.cmd('ifconfig mobile2-eth0 0')

    # Ativando o modo promíscuo nas interfaces da estação base e dos dispositivos móveis
    bs.cmd('ip link set bs-eth0 promisc on')
    mobile1.cmd('ip link set mobile1-eth0 promisc on')
    mobile2.cmd('ip link set mobile2-eth0 promisc on')

    # Iniciando a interface de controle do Mininet
    CLI(net)

    # Parando a rede
    net.stop()

if __name__ == '__main__':
    create_cellular_network()
