import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot Bubble Style", page_icon="💬")
st.title("🤖 AI Chatbot Bubble Style")
st.markdown("---")

# --- Konfigurasi API ---
# !!! PERHATIAN: MENYIMPAN API KEY LANGSUNG DI KODE SANGAT TIDAK AMAN UNTUK PRODUKSI ATAU REPO PUBLIK !!!
# Ini hanya untuk tujuan demonstrasi atau pengujian super cepat dan singkat.
OPENROUTER_API_KEY = "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" # GANTI DENGAN API KEY ASLI KAMU!

if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY_HERE": # Tambahkan validasi sederhana
    st.error("Harap masukkan OpenRouter API Key Anda di dalam kode app.py.")
    st.stop()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-7b-instruct:free"

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Tambahkan System Message di sini sebagai pesan pertama
    st.session_state.messages.append(
        {"role": "system", "content": """Anda adalah AI Chatbot yang sangat ramah, membantu, dan cerdas.
        Tugas utama Anda adalah:
        1. Memberikan respons yang **selalu relevan dan langsung menjawab pertanyaan pengguna**.
        2. Menggunakan **bahasa Indonesia yang baik dan benar**, tanpa typo atau kesalahan tata bahasa.
        3. Memahami konteks percakapan untuk memberikan jawaban yang koheren.
        4. Jika pertanyaan ambigu, jangan ragu untuk meminta klarifikasi.
        5. Berikan jawaban yang ringkas namun informatif.
        """}
    )

# Tampilkan pesan dari riwayat chat (pastikan system message tidak ditampilkan)
for message in st.session_state.messages:
    # Hanya tampilkan pesan 'user' dan 'assistant'
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

# Fungsi untuk mendapatkan respons dari AI
def get_ai_response(messages_history):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    # Format pesan sesuai kebutuhan OpenRouter API
    api_messages = [{"role": m["role"], "content": m["content"]} for m in messages_history]

    payload = {
        "model": MODEL_NAME,
        "messages": api_messages,
        "stream": False
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Akan memunculkan error untuk status kode 4xx/5xx
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error koneksi ke OpenRouter API: {e}")
        return "Maaf, terjadi kesalahan saat menghubungi AI. Silakan coba lagi nanti."
    except KeyError:
        st.error("Format respons dari OpenRouter API tidak sesuai.")
        return "Maaf, AI memberikan respons yang tidak terduga. Silakan coba lagi."

# Tampilkan pesan dari riwayat chat
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]: 
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

# Input pengguna dan logika respons AI
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Tampilkan pesan pengguna
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Dapatkan respons dari AI
    with st.spinner("AI sedang berpikir..."):
        ai_response = get_ai_response(st.session_state.messages)

    # Tampilkan respons AI
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Tombol untuk menghapus riwayat chat
if st.button("Hapus Chat"):
    st.session_state.messages = []
    st.rerun() # Muat ulang aplikasi untuk membersihkan tampilan