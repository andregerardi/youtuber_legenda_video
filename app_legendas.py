import streamlit as st
import regex as re
from pytubefix import YouTube
import zipfile36 as zipfile
import os

# Função para processar as legendas
def processa_captions(caption):
    novo_texto = re.sub(r'^\d+\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', '', caption, flags=re.MULTILINE)
    processado = re.sub(r'^\d+$', '', novo_texto, flags=re.MULTILINE)  # Remove números sozinhos
    tex = processado.replace("\n", " ")
    texto_final = " ".join(tex.split())
    return texto_final

# Função para baixar o vídeo e legendas
def baixar_video(url):
    yt = YouTube(url)
    st.subheader("Metadados do vídeo:")
    st.write(f"✔️ Título do vídeo: {yt.title}")
    st.write(f"✔️ Data de publicação: {yt.publish_date}")
    st.write(f"✔️ Total de views do vídeo: {yt.views}")
    
    # Verifica se há legendas no idioma português ('a.pt')
    if 'a.pt' in yt.captions:
        # Processa as legendas
        text = processa_captions(yt.captions['a.pt'].generate_srt_captions())
        st.success("Legendas em português geradas com sucesso!")
    else:
        st.warning("Este vídeo não possui legendas em português. Tentando usar outra legenda.")
        
        # Tenta pegar a legenda no primeiro idioma disponível (se houver)
        if yt.captions:
            caption = next(iter(yt.captions.values()))  # Pega a primeira legenda disponível
            text = processa_captions(caption.generate_srt_captions())
            st.success("Legendas em outro idioma geradas com sucesso!")
        else:
            st.error("Este vídeo não possui legendas disponíveis.")

    # Exibe o texto das legendas
    st.text_area("📝 Legendas", value=text, height=300)
    
    # Criar o arquivo de legendas
    with open("legendas.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # Baixar o vídeo
    ys = yt.streams.get_highest_resolution()
    video_filename = "video.mp4"
    ys.download(filename=video_filename)
    st.success("Vídeo processado com sucesso!")

    # Criar um arquivo zip contendo o vídeo e as legendas
    zip_filename = "video_e_legendas.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(video_filename)
        zipf.write("legendas.txt")

    # Exibir o botão para baixar o arquivo zip
    with open(zip_filename, "rb") as f:
        st.download_button(
            label="Baixar vídeo e Legendas",
            data=f,
            file_name=zip_filename,
            mime="application/zip"
        )

# título
st.title("🤖 YouTuber")
st.markdown("#### ⏯️ Download de vídeos e legendas do YouTube")

# Input do link do vídeo
url = st.text_input("Insira a URL do vídeo do YouTube:")

if st.button("Processar"):
    if url:
        baixar_video(url)
    else:
        st.error("Por favor, insira uma URL válida.")

# Rodapé
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 15px; background-color: #191970;">
    🔗 <a href="https://www.linkedin.com/in/andr%C3%A9-gerardi-ds/" target="_blank" style="color: white;">By André Gerardi</a>
</div>
""", unsafe_allow_html=True)
