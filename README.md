# Forza Energia - Sistema de Gestão de Faturas

Sistema web moderno para gestão automatizada de faturas de energia com extração de dados via IA.

## 🚀 Stack Tecnológica

### Frontend
- **Vue.js 3** + Composition API
- **TypeScript**
- **Vite** (build tool)
- **Tailwind CSS** (estilização)
- **Pinia** (state management)
- **Vue Router**
- **Chart.js** (gráficos)

### Backend (Serverless)
- **Python** (Vercel Functions)
- **Google Gemini AI** (extração de dados)
- **Google Sheets API** (armazenamento)
- **Google Drive API** (upload de PDFs)

### Autenticação
- **Supabase** (auth + OAuth Google)

### Deploy
- **Vercel** (hosting + serverless)

## 📁 Estrutura do Projeto

```
forza-energia-web/
├── api/                    # Serverless Functions (Python)
│   ├── extract.py          # Extração via Gemini
│   ├── faturas.py          # CRUD faturas (Sheets)
│   ├── gmail/
│   │   └── baixar.py       # Download de faturas
│   └── requirements.txt
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.vue
│   │   │   └── Navbar.vue
│   │   └── ui/
│   │       ├── Button.vue
│   │       ├── Input.vue
│   │       └── StatsCard.vue
│   ├── views/
│   │   ├── auth/
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── Dashboard.vue
│   │   ├── Faturas.vue
│   │   ├── Upload.vue
│   │   ├── Gmail.vue
│   │   ├── Relatorios.vue
│   │   └── Configuracoes.vue
│   ├── stores/
│   │   ├── auth.ts
│   │   ├── theme.ts
│   │   └── faturas.ts
│   ├── lib/
│   │   ├── supabase.ts
│   │   └── api.ts
│   ├── router/
│   │   └── index.ts
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── public/
│   └── favicon.svg
├── vercel.json
├── package.json
├── tailwind.config.js
├── vite.config.ts
└── tsconfig.json
```

## 🛠️ Instalação

### 1. Instalar dependências
```bash
npm install
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
```

Preencha as variáveis:
- `VITE_SUPABASE_URL` - URL do projeto Supabase
- `VITE_SUPABASE_ANON_KEY` - Chave anônima do Supabase
- `GEMINI_API_KEY` - Chave da API do Google Gemini
- `SHEETS_CREDENTIALS` - JSON das credenciais do Service Account
- `SHEETS_SPREADSHEET_ID` - Nome ou ID da planilha

### 3. Rodar em desenvolvimento
```bash
npm run dev
```

## 🚀 Deploy no Vercel

### 1. Instalar Vercel CLI
```bash
npm i -g vercel
```

### 2. Fazer login
```bash
vercel login
```

### 3. Deploy
```bash
vercel
```

### 4. Configurar variáveis de ambiente no Vercel
No dashboard do Vercel, vá em **Settings > Environment Variables** e adicione todas as variáveis do `.env.example`.

## 📋 Funcionalidades

- ✅ **Dashboard** com métricas e gráficos
- ✅ **Upload de PDFs** com drag & drop
- ✅ **Extração automática** de dados via IA (Gemini)
- ✅ **Listagem de faturas** com filtros e ordenação
- ✅ **Integração Gmail** para download automático
- ✅ **Relatórios** com gráficos interativos
- ✅ **Tema claro/escuro**
- ✅ **Autenticação** com Supabase (email + Google)
- ✅ **Design responsivo**

## 🔧 Configuração do Supabase

1. Crie um projeto no [Supabase](https://supabase.com)
2. Ative autenticação por email e Google OAuth
3. Copie a URL e a chave anônima para o `.env`

## 🔧 Configuração do Google Cloud

1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com)
2. Ative as APIs: Sheets, Drive, Gmail, Generative AI
3. Crie uma Service Account e baixe o JSON
4. Compartilhe a planilha com o email da Service Account
5. Obtenha uma chave da API Gemini

## 📄 Licença

Este projeto é privado e de uso exclusivo da Forza Energia.
