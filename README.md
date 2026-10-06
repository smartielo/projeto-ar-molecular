# Molecular AR

Aplicacao desktop de realidade aumentada para visualizacao e futura manipulacao
de moleculas usando Python, visao computacional e rastreamento de maos. O celular
atua somente como camera; todo o processamento acontece no computador.

> Estado atual: Fase 1 — captura de camera modular com exibicao em tempo real.

## Objetivo

Construir incrementalmente uma base educacional na qual uma molecula 3D real seja
ancorada a um marcador ArUco, observada pela camera de um celular e, em fases
posteriores, manipulada por gestos e validada quimicamente com RDKit.

## Tecnologias planejadas

- Python 3.11+
- OpenCV e NumPy
- OpenCV ArUco (a partir da Fase 2)
- ModernGL e PyGLM (em uma fase posterior de renderizacao 3D)
- MediaPipe (depois da base de AR)
- RDKit (depois da interacao 3D)

As dependencias de fases futuras nao sao instaladas antecipadamente.

## Arquitetura

O fluxo planejado mantem captura, rastreamento, dominio quimico, renderizacao e
interacao desacoplados:

```text
camera -> frame OpenCV -> rastreamento ArUco -> pose da camera
                                             -> renderer 3D -> composicao
hand tracking -> coordenadas 2D -> raio 3D -> plano do marcador -> interacao
chemistry <-> molecule model <-> RDKit
```

Na Fase 1, somente o primeiro bloco (`camera`) e o overlay de diagnostico estao
ativos. `main.py` apenas coordena esses componentes.

## Estrutura de pastas

```text
.
|-- main.py
|-- requirements.txt
|-- camera/
|   |-- camera_config.py
|   `-- camera_source.py
|-- config/
|   `-- settings.py
|-- ui/
|   `-- overlay.py
|-- ar/                 # fases 2 a 5
|-- chemistry/          # fases 6 a 8 e 12 a 13
|-- hand_tracking/      # fases 9 e 10
|-- interaction/        # fase 11
|-- rendering/          # fases 5 a 8
|-- assets/
|   |-- markers/
|   |-- models/
|   `-- textures/
`-- tests/
```

## Instalacao no Windows (PowerShell)

O Python 3.11, 3.12 ou 3.13 convencional e recomendado. Evite uma build
free-threaded enquanto bibliotecas cientificas ainda estiverem sendo validadas
para ela.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se a politica do PowerShell bloquear a ativacao, ela nao e obrigatoria:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Como executar

Camera padrao, sem overlay de FPS:

```powershell
python main.py
```

Selecionar outra camera e exibir FPS:

```powershell
python main.py --camera 1 --show-fps
```

Uma URL de stream tambem e aceita pela abstracao (a disponibilidade e o formato
dependem do aplicativo de camera IP):

```powershell
python main.py --camera "http://192.168.0.10:8080/video" --show-fps
```

Opcoes uteis:

```powershell
python main.py --help
python main.py --camera 0 --width 1280 --height 720 --debug
```

Pressione `Q` ou `Esc` na janela de video para encerrar. A camera e todas as
janelas do OpenCV sao liberadas mesmo quando ocorre uma excecao.

## Configuracao da camera

Os valores padrao ficam em `config/settings.py` e podem ser sobrescritos pela
linha de comando. Os indices `0`, `1` e `2` representam dispositivos enumerados
pelo sistema operacional. DroidCam e Iriun normalmente aparecem como webcam
virtual e, portanto, usam um desses indices.

Para descobrir o indice do celular, feche outros programas que estejam usando a
camera e teste `--camera 0`, depois `1`, `2` etc. O projeto solicita resolucao,
mas o driver pode escolher o modo compativel mais proximo.

## Teste manual da Fase 1

1. Ative o ambiente virtual e instale as dependencias.
2. Conecte uma webcam ou inicie a webcam virtual do celular.
3. Execute `python main.py --camera 0 --show-fps`.
4. Confirme que a imagem se atualiza e que o FPS aparece no canto superior.
5. Pressione `Q`; repita e encerre com `Esc`.
6. Se houver mais de uma camera, repita com `--camera 1`.

Resultado esperado: uma janela chamada `Molecular AR - Camera` mostra o video em
tempo real, opcionalmente com FPS, e fecha sem manter o dispositivo ocupado.

## Limitacoes atuais

- Ainda nao ha deteccao ArUco, calibracao, pose ou renderizacao 3D.
- A Fase 1 nao garante compatibilidade com todo protocolo de camera IP; ela apenas
  aceita uma URL que o backend de video do OpenCV consiga abrir.
- Resolucao e FPS efetivos dependem da camera, do driver e do aplicativo do celular.

## Roadmap

- [x] Camera input
- [x] Smartphone camera via webcam virtual/URL compativel
- [ ] ArUco detection
- [ ] Camera calibration
- [ ] Pose estimation
- [ ] 3D rendering
- [ ] Atom rendering
- [ ] Molecule rendering
- [ ] MediaPipe hand tracking
- [ ] Pinch detection
- [ ] 3D interaction
- [ ] RDKit integration
- [ ] Molecule validation
- [ ] Markerless tracking

## Screenshots

Serao adicionadas depois que a pipeline visual estiver consolidada.

