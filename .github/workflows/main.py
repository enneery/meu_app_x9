import flet as ft
import os
import time
from PIL import Image, ImageDraw

# ==============================================================================
# 📁 1. CONTROLADOR DE PASTAS E ROTAS ABSOLUTAS DO HARD DISKy
# ==============================================================================
PASTA_APP = os.getcwd()
PASTA_ASSETS = os.path.join(PASTA_APP, "assets")
# 🔒 NOVO LOCAL: Pasta de exportação limpa e isolada para salvar a maquiagem!
PASTA_EXPORT = os.path.join(PASTA_APP, "exportacao")

for pasta in [PASTA_ASSETS, PASTA_EXPORT]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Escâner dinâmico para pegar a foto de entrada na pasta assets
caminho_foto_filha = ""
arquivos_pasta = os.listdir(PASTA_ASSETS)
for arq in arquivos_pasta:
    if arq.lower().endswith(('.jpg', '.jpeg', '.png')):
        caminho_foto_filha = os.path.join(PASTA_ASSETS, arq)
        break

# Rota física do novo arquivo maquiado que vai nascer na pasta exportação
caminho_foto_maquiada = os.path.join(PASTA_EXPORT, "foto_maquiada_final.jpg")

cor_pincel_atual = "#FF0000"  
modo_pincel_ativo = False
modo_conta_gotas = False
espessura_pincel = 15

def main(page: ft.Page):
    page.title = "X9 SUPREMO - DOIS LOCAIS DE SALVAMENTO"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    page.padding = 10

    lbl_status_pincel = ft.Text("🎯 MIRA DE PRECISÃO ATIVA", size=13, weight="bold", color="white")
    
    if caminho_foto_filha:
        canvas_desenho = ft.Image(src=caminho_foto_filha, width=350, height=350, fit="contain")
    else:
        canvas_desenho = ft.Text("⚠️ INSIRA UMA FOTO DENTRO DA PASTA ASSETS!", color="red", weight="bold")
        
    visor_sensor = ft.Container(width=350, height=350)

    # ==============================================================================
    # 🎛️ 2. OS MOTORES TURBINADOS DA MAQUIAGEM LÍQUIDA
    # 🔌 MOTOR 1 RECALIBRADO: Força o aviso visual bruto na tela do celular!
    def alternar_modo_central(e):
        global modo_pincel_ativo, modo_conta_gotas
        if not caminho_foto_filha: return
        
        modo_conta_gotas = not modo_conta_gotas
        if modo_conta_gotas:
            modo_pincel_ativo = False
            
        if modo_conta_gotas:
            # 🚀 REBITE VISUAL: Muda o letreiro e bota o botão em Roxo piscando no vidro!
            lbl_status_pincel.value = "🧪 [TOQUE NA FOTO PARA COLETAR COR]"
            btn_centro.bgcolor = "purple"
        else:
            lbl_status_pincel.value = "🎯 MIRA DE PRECISÃO ATIVA"
            btn_centro.bgcolor = "orange"
            
        lbl_status_pincel.update()
        btn_centro.update()
        page.update()

        # 🔌 MOTOR DE MAQUIAGEM MOBILE: Escuta o toque e o arrasto do dedão na tela de vidro!
    def ao_maquiar_smartphone(e: ft.DragUpdateEvent):
        global cor_pincel_atual, modo_pincel_ativo, modo_conta_gotas, caminho_foto_filha
        if not caminho_foto_filha or not os.path.exists(caminho_foto_filha): return
        
        # Só risca a foto se o botão laranja estiver em modo Pincel
        if modo_pincel_ativo:
            try:
                img_aux = Image.open(caminho_foto_filha)
                fator_x = img_aux.width / 350
                fator_y = img_aux.height / 350
                
                # Captura a coordenada exata do arrasto do dedo na tela
                x_real = int(e.local_x * fator_x)
                y_real = int(e.local_y * fator_y)
                
                x_real = max(0, min(img_aux.width - 1, x_real))
                y_real = max(0, min(img_aux.height - 1, y_real))
                
                # Pillow aplica a tinta contínua na cerâmica da foto na RAM
                draw = ImageDraw.Draw(img_aux)
                raio = int(espessura_pincel / 2)
                draw.ellipse([x_real - raio, y_real - raio, x_real + raio, y_real + raio], fill=cor_pincel_atual)
                img_aux.save(caminho_foto_filha)
                
                # Atualiza a lona do celular instantaneamente
                canvas_desenho.src = f"{caminho_foto_filha}?t={time.time()}"
                canvas_desenho.update()
            except Exception as err:
                print(f"Erro no arrasto da maquiagem: {err}")

    # 🧪 GATILHO INDEPENDENTE DO CONTA-GOTAS (Apenas no primeiro toque seco)
    def ao_tocar_conta_gotas(e: ft.TapEvent):
        global cor_pincel_atual, modo_pincel_ativo, modo_conta_gotas, caminho_foto_filha
        if modo_conta_gotas and caminho_foto_filha:
            try:
                img_aux = Image.open(caminho_foto_filha)
                fator_x = img_aux.width / 350
                fator_y = img_aux.height / 350
                x_real = int(e.local_x * fator_x)
                y_real = int(e.local_y * fator_y)
                
                rgb = img_aux.getpixel((max(0, min(img_aux.width-1, x_real)), max(0, min(img_aux.height-1, y_real))))
                cor_pincel_atual = f"#{rgb:02x}{rgb:02x}{rgb:02x}"
                
                modo_conta_gotas = False
                modo_pincel_ativo = True
                
                lbl_status_pincel.value = "🖌️ PINCEL ATIVO (ARRRASTE O DEDO)"
                btn_centro.bgcolor = "orange"
                lbl_status_pincel.update()
                btn_centro.update()
            except Exception as err:
                print(f"Erro na coleta: {err}")

    # ==============================================================================
    # 🧱 3. ALIMENTAÇÃO DA LONA DO SENSOR MÓVEL MULTI-GESTOS
    # ==============================================================================
    # 🔒 REBITE SUPREMO: Separa o toque seco (Conta-gotas) do arrasto contínuo (Pincel/Maquiagem)!
    visor_sensor.content = ft.GestureDetector(
        on_tap_down=ao_tocar_conta_gotas,   # 🧪 Toque rápido ativa o Conta-Gotas
        on_pan_update=ao_maquiar_smartphone, # 🖌️ Arrastar o dedão espalha a tinta na foto!
        drag_interval=10,                    # Melhora a velocidade de resposta na RAM do celular
        content=canvas_desenho
    )

    # ==============================================================================
    # 🚀 TELA 5 - EXPEDIÇÃO DA PRENSA DO PILLOW E MUDANÇA AUTOMÁTICA
    # ==============================================================================
    def acao_salvar_e_avancar_automatico(e):
        global caminho_foto_filha, caminho_foto_maquiada
        if not caminho_foto_filha or not os.path.exists(caminho_foto_filha): return
        
        try:
            # 🔌 REBITE FIS_ICO: Pillow força a gravação real do arquivo no novo local seguro!
            img_final = Image.open(caminho_foto_filha)
            img_final.convert("RGB").save(caminho_foto_maquiada, "JPEG")
            
            # Limpa o chassi da Tela 4 e monta a Tela 5 apontando para o novo bocal
            page.clean()
            
            lbl_inspecao_titulo = ft.Text("🔍 TELA 5 - INSPEÇÃO FINAL DO LOTE", size=15, weight="bold", color="green")
            # Exibe a foto salva diretamente de dentro da nova pasta exportação!
            foto_inspecao_final = ft.Image(src=caminho_foto_maquiada, width=350, height=350, fit="contain")
            
            btn_concluir_tudo = ft.ElevatedButton(
                content=ft.Text("🏁 FINALIZAR EXPEDIÇÃO", size=13, weight="bold"),
                bgcolor="green", width=340, height=45,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
                on_click=lambda _: os.startfile(PASTA_EXPORT) # Abre a nova pasta estalando no Windows!
            )
            
            page.add(ft.Column([
                lbl_inspecao_titulo,
                foto_inspecao_final,
                btn_concluir_tudo
            ], horizontal_alignment="center", spacing=15))
            page.update()
        except Exception as err:
            print(f"Erro na prensa final: {err}")

    # Layout Rodapé Simétrico de 340px
    btn_centro = ft.ElevatedButton(
        content=ft.Row([lbl_status_pincel], alignment="center"), 
        bgcolor="orange", width=340, height=45,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)), 
        on_click=alternar_modo_central
    )

    btn_salvar_automatico = ft.ElevatedButton(
        content=ft.Text("💾 SALVAR E AVANÇAR", size=13, weight="bold"), 
        bgcolor="green", width=340, height=45, 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)), 
        on_click=acao_salvar_e_avancar_automatico
    )

    page.add(ft.Column([
        ft.Text("TELA 4 - ESTUFA DE MAQUIAGEM", size=15, weight="bold", color="#d4af37"),
        btn_centro,
        visor_sensor,
        btn_salvar_automatico
    ], scroll="always", alignment="start", horizontal_alignment="center", spacing=12))
    page.update()

ft.app(target=main)
