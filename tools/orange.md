# Orange Data Mining

[Orange Web Site](https://orangedatamining.com/)

## Guia de Instalação

Este vídeo dá uma visão geral sobre o Orange e sua instalação:

<iframe width="560" height="315" src="https://www.youtube.com/embed/MY7oIiLt71Y?si=nRzupaK34RZVSMkc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### Windows

Baixe e execute o instalador padrão. Observe duas coisas fundamentais:
1. Ele pode demorar bastante para instalar. Tem um estágio que ele pára a barra de progresso e vai parecer travado -- espere bastante, ele provavelmente não travou.
2. Há uma sub-instalação do miniconda (que você deve fazer) que pode confundir um pouco. Se tiver dúvidas, assista o vídeo:

<iframe width="560" height="315" src="https://www.youtube.com/embed/24uz-Qidu_s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

### Linux

No Linux eu segui a instalação da versão PIP do site:

~~~
pip3 install PyQt5 PyQtWebEngine
pip3 install orange3
~~~

Para executar, eu também segui as orientações do site:

~~~
python3 -m Orange.canvas
~~~

#### Tratando problemas no Linux

Não tive mais problemas na versão recente. Apenas se você tiver problemas nesta instalação você pode seguir a linha:

A sequência abaixo é antiga, então pode não funcionar mais.

1. Instalar como sudo:

~~~
sudo -H pip3 install orange3
~~~

2. Instalar outras dependências adicionais não instaladas ou instaladas em versões incompatíveis:

Dependências adicionais que o pip não instalou:

**PySide2**

~~~
sudo -H pip3 install PySide2
~~~

**PyQt5 na versão correta**

Uma das versões que instalei apresentou inconsistência, foi necessário instalar a PyQt 5.14. Talvez sejam necessários estes dois comandos antes de mudar a versão do PyQt5.

~~~
sudo -H apt update && sudo -H apt autoclean

sudo -H apt update && sudo -H apt install -y --no-install-recommends python3-pip python3-setuptools
~~~

Depois instalei especificando a versão:

~~~
sudo -H pip3 install pyqt5==5.14
~~~

Executando se instalar como sudo:
~~~
sudo -H python3 -m Orange.canvas
~~~